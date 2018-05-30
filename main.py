import pygame, math, random, constants, generator
from controls import keyboard, mouse
from objects.rect import Rect
from objects.enemy import Enemy
from objects.player import Player
from img import images
from logic import collisions

from pygame.locals import *
flags = DOUBLEBUF

pygame.init()

ctx = pygame.display.set_mode((constants.gameW,constants.gameH), flags)
ctx.set_alpha(None)
pygame.display.set_caption("Roguelike")
clock = pygame.time.Clock()

curFloor = []
curRoom = {}
curPos = []

player = Player(170,240,constants.playerW,constants.playerH,
                    constants.black,[images.player1,images.player2],10,[5,5],15)

def listen(running):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        else:
            keyboard.listen(event)
            mouse.listen()
    return running

def enemyCheck(room):
    allEnemiesDead = 1
    for e in room["enemies"]:
        if e.hp > 0:
            allEnemiesDead = 0
            break
    return allEnemiesDead

def getProjectile(projectile,bullets):
    if projectile != None:
        bullets.append(projectile)
    return None

def trySpawn(enemy, room):
    if enemy.hp > 0 and enemy.name == "peep":
        if random.randint(0,450) == 0:
            bunnySpawn = Enemy("bunny")
            bunnySpawn.x, bunnySpawn.y = (constants.gameW-bunnySpawn.w)/2, (constants.gameH-bunnySpawn.h)/2
            bunnySpawn.x += random.randint(0,300)-150
            bunnySpawn.y += random.randint(0,300)-150
            room["enemies"].append(bunnySpawn)

def main(curFloor, curRoom, curPos):

    enemiesCleared = 0
    bullets = []
    running = True

    while running:
        running = listen(running)

        # Reset BG
        ctx.blit(images.backgrounds[curRoom["type"]],(0,0))

        # Update All Entities
        projectile = None

        for d in curRoom["doors"]:
            d.go(ctx, enemiesCleared)
        for i in curRoom["items"]:
            i.go(ctx, player)
        for b in bullets:
            b.go(ctx, curRoom, player)
            if b.removeFlag:
                bullets.remove(b)
        for e in curRoom["enemies"]:
            projectile = e.go(ctx, curRoom, player)
            projectile = getProjectile(projectile, bullets)
            trySpawn(e,curRoom)

        projectile = player.go(ctx, curRoom)
        projectile = getProjectile(projectile, bullets)

        location = 50
        for i in range(math.floor(player.hp/2)):
            ctx.blit(images.peach,(location,15))
            location += 20
        if player.hp%2 == 1:
            ctx.blit(images.halfPeach,(location,15))

        location = 85
        ctx.blit(images.foodStamp,(location,35))

        muli = pygame.font.Font("fonts/muli.ttf",15)

        stamps = muli.render(str(player.stamps),True,constants.black)
        stampsRECT = stamps.get_rect()
        stampsRECT.right = location + 20
        stampsRECT.top = 35
        ctx.blit(stamps,stampsRECT)

        fps = muli.render(str(round(clock.get_fps(),1)),True,constants.black)
        ctx.blit(fps,(840,575))

        if enemiesCleared:
            for c in curRoom["doors"]:
                key = c.name
                if collisions.rectangles(player,constants.clearZones[key]):
                    if key == "w":
                        curPos[0] -= 1
                        player.y = constants.gameH - 110 - constants.playerH - 20
                    elif key == "a":
                        curPos[1] -= 1
                        player.x = constants.gameW - 110 - constants.playerW - 20
                    elif key == "s":
                        curPos[0] += 1
                        player.y = 10 + 20
                    elif key == "d":
                        curPos[1] += 1
                        player.x = 110 + 20
                    curRoom = curFloor[curPos[0]][curPos[1]]
                    bullets = []
                    enemiesCleared = 0
        else:
            enemiesCleared = enemyCheck(curRoom)

        # Update Window
        pygame.display.update()
        clock.tick(60)
    pygame.quit()

curFloor = generator.newFloor()
for y in range(constants.gridLength):
    for x in range(constants.gridLength):
        if not curFloor[y][x] == None:
            curRoom = curFloor[y][x]
            curPos = [y,x]
main(curFloor, curRoom, curPos)
