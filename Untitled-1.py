import pygame
import random
import math
import sys
from pygame import mixer

#initialize the pygame  
pygame.init()
screen = pygame.display.set_mode((1530,800))
background = pygame.image.load("walle.png")
homepagebg= pygame.image.load("bg.jpeg")
mixer.init()
game = mixer.Sound("tenebrax.wav")
game.set_volume(0.2)
game.play(-1)

#title and icon
pygame.display.set_caption("beast incarnate")
icon = pygame.image.load("space.png")
pygame.display.set_icon(icon)

#player
playerImg = pygame.image.load("spaceship (2).png")
playerX = 740
playerY = 680
playerX_change = 0
#change
playerY_change = 0

#enemy

enemyImg = pygame.image.load("RE (1).png")
enemyX = random.randint(0,1530)
enemyY = random.randint(50,150)
enemyX_change = 7
enemyY_change = 40

#bullet
bulletImg = pygame.image.load("bullet (1).png")
bulletX = 0
bulletY = 0
bulletX_change = 0
bulletY_change = 20
bullet_state="ready"

score=0

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y):
    screen.blit(enemyImg,(x,y))
    
def fire_bullet(x,y):
    global bullet_state
    bullet_state= "fire"
    screen.blit(bulletImg,(x+16,y-30))
def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt((math.pow(enemyX-bulletX,2))+math.pow(enemyY-bulletY,2))
    if distance < 27:
        return True
    else:
        return False

clock = pygame.time.Clock()
vishesh = True
Played = True
shoot= mixer.Sound("1a.wav")
shoot.set_volume(1)

#GAME LOOP
text = pygame.font.SysFont('Chiller',120)
text3 = pygame.font.SysFont('Chiller',60)
text2 = pygame.font.SysFont('Arial',30)
gameover = text.render("!! GAME OVER !!", False, 'red')
start = text.render("START",False,'red')
start_hover = text.render("START",False,'blue')
startrect = start.get_rect(center = (750,400))
mainscreen = True
while True:
    #rgb
    screen.fill((0,0,0))
    #background
    screen.blit(background,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if mainscreen == True:
            if (event.type == pygame.MOUSEBUTTONDOWN):
                if startrect.collidepoint(event.pos):
                    mainscreen = False
        if vishesh == True and mainscreen == False:
            if event.type == pygame.KEYDOWN:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a):   
                    playerX_change =-10
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    playerX_change = 10
                    # change
                if event.key == pygame.K_SPACE:
                    
                    if bullet_state is "ready":
                        shoot.play()
                        bulletX = playerX
                        fire_bullet(bulletX,bulletY)
                

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_a or event.key == pygame.K_d or event.key == pygame.K_w or event.key == pygame.K_s or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    playerX_change = 0
                    # change
                    # playerY_change = 0
    if mainscreen == True:
        screen.fill('black')
        if startrect.collidepoint(pygame.mouse.get_pos()):
            screen.blit(start_hover,startrect)
        else:
            screen.blit(start,startrect)

    else:
        if vishesh == True:
            with open('highscore.txt','r') as h:
                n = h.read()
            lasthighscore = text2.render(f'HighScore: {n}',False,'white')
            screen.blit(lasthighscore, (1300,5))
            playerX += playerX_change
            
            if playerX <=0:
                playerX=0
            elif playerX >=1466:
                playerX=1466
                
            enemyX+=enemyX_change
            if enemyX <=0:
                enemyX_change=6
                enemyY+=enemyY_change
            elif enemyX >=1466:
                enemyX_change=-6
                enemyY+=enemyY_change

            #bullet movement
            if bulletY<=0:
                bulletY=680
                bullet_state="ready"
            if bullet_state is "fire":
                fire_bullet(bulletX,bulletY)
                bulletY -= bulletY_change 
            #collision
            collision=isCollision(enemyX,enemyY,bulletX,bulletY)   
            if collision:
                bulletY = 680
                bullet_state = "ready"
                score+=1
            if enemyY>=620:
                vishesh = False
            Score = text2.render(f'Score: {score}',False,'white')
            screen.blit(Score, (1380,750))
            player(playerX,playerY)
            enemy(enemyX,enemyY)
        else:
            game.stop()
            shoot.stop()

            if Played == True:
                endgame = mixer.Sound('Dhoom.wav')
                endgame.set_volume(0.3)
                endgame.play(-1)
                Played = False
            screen.fill('black')
            with open('highscore.txt','r') as h:
                n = h.read()
            if score >= int(n):
                with open('highscore.txt','w') as x:
                    x.write(str(score))
                newhighscore = text3.render('NEW HIGH SC0RE', False, 'white')
                screen.blit(newhighscore,(500,150))
            screen.blit(gameover, (460,250))
            endscore = text3.render(f"YOUR SCORE: {score}", False, 'white')
            screen.blit(endscore, (620,350))

        
    pygame.display.update()
    clock.tick(60)
    
    
    