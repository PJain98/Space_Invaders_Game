import pygame
import random
import math
from pygame import mixer

# Initialize the window
pygame.init()
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('background.jpg')

# Background sound
mixer.music.load('background.wav')
mixer.music.play(-1)  # -1 so that sound play on loop

# Player
playerImg = pygame.image.load('space-invaders.png')
playerX = 370
playerY = 480
playerX_change = 0  # to change cursor left or right based on inputs

# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(30, 150))
    enemyX_change.append(0.3)  # to change cursor left or right based on inputs
    enemyY_change.append(40)

# Bullet
## Ready- You can't see the bullet on the screen
## Fire- The bullet is currrently moving
bulletImg = pygame.image.load('bullet.png')
bulletX = 0
bulletY = 480
bulletX_change = 0  # to change cursor left or right based on inputs
bulletY_change = 0.7
bullet_state = "ready"

###Score
score_value = 0
font = pygame.font.Font("freesansbold.ttf",32)

textX = 10
textY = 10

#Game Over Text
over_font = pygame.font.Font("freesansbold.ttf",64)


def show_score(x,y):
    score = font.render("Score : " + str(score_value),True, (255,255,255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER",True, (255,0,0))
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))


# Creating Enemy
def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletImg, (x + 36, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 25:
        return True
    else:
        return False


running = True
while running:
    # RGB
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    # playerX+=0.1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # if keystroke is pressed check weather it is left or right
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.35
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.35
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    # Adding sound while firing bullet
                    bullet_Sound = mixer.Sound("laser.wav")
                    bullet_Sound.play()
                    bulletX = playerX  # current coordinate of x axis
                    fire_bullet(bulletX, bulletY)
                # fire_bullet(playerX,bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 720:
        playerX = 720

    # Enemy Movement
    for i in range(num_of_enemies):

        ## Game Over
        if enemyY[i]>480:
            for j in range(num_of_enemies):
                enemyY[j]=2000
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 0.2
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.2
            enemyY[i] += enemyY_change[i]

        # Collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_Sound = mixer.Sound("explosion.wav")
            collision_Sound.play()
            bulletY = 480
            bullet_state = 'ready'
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(30, 150)

        enemy(enemyX[i], enemyY[i],i)

    # Bullet Movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = 'ready'

    if bullet_state == 'fire':
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()
