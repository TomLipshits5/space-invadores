import pygame
from pygame import mixer
import random
import math

# initialize pygame

pygame.init()

# open game window
screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load("space_background.jpg")
mixer.music.load("background.wav")
mixer.music.play(-1)

# title and icon
pygame.display.set_caption("Space Invaders")
spaceship_icon = pygame.image.load("spaceship.png")
pygame.display.set_icon(spaceship_icon)

# player
player_img = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 0

# score
score_value = 0
font = pygame.font.Font('ARCADE.TTF', 32)
over_font = pygame.font.Font('ARCADE.TTF', 85)
textX = 10
textY = 10

def game_over():
    end_text = over_font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(end_text, (215,250))

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def player(x, y):
    screen.blit(player_img, (x, y))


# enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for i in range(num_of_enemies):
    enemy_img.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(40, 150))
    enemyX_change.append(2)
    enemyY_change.append(40)


def enemy(x, y, i):
    screen.blit(enemy_img[i], (x, y))


# bullet
bullet_img = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletY_change = 5
bullet_state = "ready"


def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet_img, (x + 16, y + 10))


# colition
def iscolition(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False



# game main loop
running = True
while running:

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        # Quit function
        if event.type == pygame.QUIT:
            running = False

        # if key is pressed check if right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound = mixer.Sound('laser.wav')
                    bullet_sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or pygame.K_RIGHT:
                playerX_change = 0

    # palyer movment
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    if playerX >= 735:
        playerX = 735

    # enemy movment
    for i in range(num_of_enemies):

        #game over
        if enemyY[i] > 460:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break


        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2
            enemyY[i] += enemyY_change[i]

        if enemyX[i] >= 735:
            enemyX_change[i] = -2
            enemyY[i] += enemyY_change[i]

        # cilition
        colition = iscolition(enemyX[i], enemyY[i], bulletX, bulletY)
        if colition:
            colition_sound = mixer.Sound('explosion.wav')
            colition_sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(40, 150)

        enemy(enemyX[i], enemyY[i], i)

    # bullet movment
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    show_score(textX, textY)
    player(playerX, playerY)
    pygame.display.update()
