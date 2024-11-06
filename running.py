while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Paddle movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.left -= PADDLE_SPEED
    if keys[pygame.K_RIGHT] and paddle.right < SCREEN_WIDTH:
        paddle.right += PADDLE_SPEED

    # Ball movement
    ball.x += ball_speed[0]
    ball.y += ball_speed[1]

    # Ball collision with walls
    if ball.left <= 0 or ball.right >= SCREEN_WIDTH:
        ball_speed[0] = -ball_speed[0]
    if ball.top <= 0:
        ball_speed[1] = -ball_speed[1]

    # Ball collision with paddle
    if ball.colliderect(paddle):
        hit_sound.play()
        # Adjust ball direction based on hit location on paddle
        offset = (ball.centerx - paddle.centerx) / (PADDLE_WIDTH // 2)
        ball_speed[0] = BALL_SPEED_X * offset
        ball_speed[1] = -abs(ball_speed[1])

    # Ball collision with bricks
    hit_index = ball.collidelist(bricks)
    if hit_index != -1:
        brick = bricks.pop(hit_index)
        break_sound.play()
        ball_speed[1] = -ball_speed[1]
        score += 10
        if random.random() < 0.2:  # Random chance of a powerup
            powerup = pygame.Rect(brick.x, brick.y, POWERUP_SIZE, POWERUP_SIZE)
            powerups.append((powerup, random.choice(powerup_types)))
