running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:  # Pause menu
                pause_menu(screen)

        # Handle input
        keys = pygame.key.get_pressed()
        paddle.move(keys)
        ball.move()

        # Check collisions
        if ball.check_paddle_collision(paddle):
            hit_sound.play()

        #particles = []  # Initialize particles


        # Check brick collisions and update score
        if ball.check_brick_collision(bricks, power_ups, particles):
            break_sound.play()
            score += 10  # Increment score for each brick hit



        # Check if all bricks are cleared
        if all(not brick.visible for brick in bricks):  # All bricks cleared
            current_level += 1
            if current_level > TOTAL_LEVELS:
                you_win_screen(screen, score)
                running = False
            else:
                level_config = LEVEL_CONFIG[current_level]
                bricks = create_brick_grid(level_config["rows"], level_config["theme"])
                ball.reset_speed()
                ball.reset_position()

                pygame.mixer.music.load(level_config["music"])
                pygame.mixer.music.play(-1)



        # Check if ball falls below paddle
        if ball.y - ball.radius > SCREEN_HEIGHT:  # Ball fell below paddle
            lives -= 1
            if lives == 0:
                game_over_screen(screen, score)
                running = False  # End the game
            else:
                ball.reset_position()
                ball.reset_speed()

        # Draw everything
        apply_theme(level_config["theme"], paddle, ball, bricks, screen)
        draw_ui(screen, score, lives, current_level, current_ui_font, current_ui_font_color, current_ui_bg_color)
        paddle.draw(screen)
        ball.draw(screen)
        for brick in bricks:
            brick.draw(screen)

        # Update and draw power-ups
        for power_up in power_ups[:]:
            if power_up.active:
                power_up.move()

                # Check if power-up falls below the screen
                if power_up.y > SCREEN_HEIGHT:
                    power_up.active = False  # Mark as inactive when off-screen

                power_up.draw(screen)

                if power_up.check_collision(paddle):
                    powerup_sound.play()
                    if power_up.type == "expand":
                        paddle.width += 40
                    elif power_up.type == "shrink":
                        paddle.width = max(40, paddle.width - 40)
                    elif power_up.type == "slow":
                        ball.dx *= 0.9
                        ball.dy *= 0.9
                    elif power_up.type == "fast":
                        ball.dx *= 1.1
                        ball.dy *= 1.1
                    power_up_timers[power_up.type] = FPS * 5
                    power_up.active = False

        # Safely remove inactive power-ups
        power_ups[:] = [power_up for power_up in power_ups if power_up.active]

        # Safely remove inactive power-ups
        power_ups[:] = [power_up for power_up in power_ups if power_up.active]

        # Reset power-up effects after duration
        for effect, timer in power_up_timers.items():
            if timer > 0:
                power_up_timers[effect] -= 1
                if power_up_timers[effect] == 0:
                    if effect in ["expand", "shrink"]:
                        paddle.width = INITIAL_PADDLE_WIDTH
                    elif effect in ["slow", "fast"]:
                        ball.dx, ball.dy = INITIAL_BALL_SPEED

        for particle in particles[:]:
            particle.update()
            particle.draw(screen)
            if particle.lifetime <= 0:
                particles.remove(particle)

        #print("Number of particles:", len(particles))  # Check if particles exist


        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
