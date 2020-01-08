import pygame
from math import hypot
from random import randint

def fit(x, y):
    global width, height, char_size

    # Check x
    if x > width - char_size:
        x = width - char_size
    if x < 0:
        x = 0

    # Check y
    if y > height - char_size:
        y = height - char_size
    if y < 0:
        y = 0
    return x, y

# Initialization
pygame.init()

# Screen initialization
width, height, char_size = 500, 800, 64
screen = pygame.display.set_mode((width, height))

# Load attacker and defender sprites, background, bullet
attacker = pygame.image.load('attacker.png')
defender = pygame.image.load('defender.png')
background = pygame.image.load('background.jpg').convert()
bullet = pygame.image.load('bullet.png')

# Load font
font = pygame.font.Font('freesansbold.ttf', 32)

# Attacker and defender positions
num_enemies = 6
a_speeds, d_speed, b_speed = [20] * num_enemies, 10, 30
aXs = [randint(100, 300) for i in range(num_enemies)] 
aYs = [randint(100, 300) for i in range(num_enemies)]
dX, dY = 200, 650

# Bullet
b_state = 'ready'
bX, bY = 0, 0

# Score
score = 0

running = True
while running:
    pygame.time.delay(40)

    # Draw background
    screen.blit(background, (-20, -20))

    # Check quit button
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Check keys
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        dX -= d_speed 
    if keys[pygame.K_RIGHT]:
        dX += d_speed
    if keys[pygame.K_SPACE] and b_state == 'ready':
        b_state = 'fire'
        bX, bY = dX, dY

    # Limit values to fit screen
    dX, dY = fit(dX, dY)

    for i in range(num_enemies):
        # Attacker movements
        aXs[i] += a_speeds[i]
        if aXs[i] > width - char_size or aXs[i] < 0:
            a_speeds[i] *= -1
            aYs[i] += char_size // 2

    # Bullet movement
    if b_state == 'fire':
        screen.blit(bullet, (bX, bY))
        bY -= b_speed
        if bY < 0:
            bX, bY = 0, 0
            b_state = 'ready'

    # Check collision
    for i in range(num_enemies):
        if hypot(aXs[i] - bX, aYs[i] - bY) < 27:
            aXs[i] = randint(100, 300)
            aYs[i] = randint(100, 300)
            a_speeds[i] = 20
            bX, bY = 0, 0
            b_state = 'ready'
            score += 1
            break

    # Check game over
    for y in aYs:
        if y > 650:
            num_enemies = 0
            break

    # Draw defender and attackers
    for i in range(num_enemies):
        screen.blit(attacker, (aXs[i], aYs[i]))
    screen.blit(defender, (dX, dY))

    # Score text display
    score_text = font.render('Score: ' + str(score), True, (50, 150, 59))
    screen.blit(score_text, (10, 20))
    pygame.display.update()

pygame.quit()
