# Ball out of bounds
        if ball.bottom >= SCREEN_HEIGHT:
            lives -= 1
            ball.x, ball.y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
            if lives == 0:
                game_over = True

        # Handle powerup falling
        for powerup in powerups[:]:
            powerup[0].y += 3
            if powerup[0].colliderect(paddle):
                powerup_sound.play()
                powerup_type = powerup[1]
                if powerup_type == "expand":
                    paddle.width += 20
                elif powerup_type == "shrink":
                    paddle.width = max(paddle.width - 20, 50)
                elif powerup_type == "slow":
                    ball_speed[0] = max(1, ball_speed[0] - 1)
                    ball_speed[1] = max(1, ball_speed[1] - 1)
                elif powerup_type == "fast":
                    ball_speed[0] += 1
                    ball_speed[1] += 1
                powerups.remove(powerup)

        # Next level if all bricks are cleared
        if not bricks:
            level += 1
            ball_speed[0] += 1 if ball_speed[0] > 0 else -1
            ball_speed[1] = abs(ball_speed[1]) + 1
            ball.x, ball.y = SCREEN_WIDTH // 2 - BALL_RADIUS, SCREEN_HEIGHT // 2
            bricks = create_bricks()

        # Draw everything
        draw_objects()
    else:
        display_game_over()

    clock.tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
