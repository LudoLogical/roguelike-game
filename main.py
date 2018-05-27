import pygame, math, random, constants
from controls import keyboard, mouse
from objects.player import Player
from img import images
from rooms import rooms
from logic import matrices
pygame.init()

ctx = pygame.display.set_mode((constants.gameW,constants.gameH))
pygame.display.set_caption("Roguelike")
clock = pygame.time.Clock()

curFloor = []
curRoom = rooms[0]

player = Player(170,240,constants.playerW,constants.playerH,
                    constants.black,[images.player1,images.player2],50,[4,4])

def close():
    pygame.quit()
    quit()

def listen():
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                close()
            else:
                keyboard.listen(event)
                mouse.listen()

def validatePos(nextFloor,yPos,xPos):
    validPos = False
    if not yPos == 0:
        if not nextFloor[yPos-1][xPos] == None:
            validPos = True
    if not xPos == 0:
        if not nextFloor[yPos][xPos-1] == None:
            validPos = True
    if not yPos == constants.gridLength-1:
        if not nextFloor[yPos+1][xPos] == None:
            validPos = True
    if not xPos == constants.gridLength-1:
        if not nextFloor[yPos][xPos+1] == None:
            validPos = True
    return validPos

def startFloor():
    nextRooms = []
    nextFloor = [[None,None,None,None,None],
                [None,None,None,None,None],
                [None,None,None,None,None],
                [None,None,None,None,None],
                [None,None,None,None,None]]
    numRooms = 8 + random.randint(0,4)
    for i in range(numRooms):
        nextRooms.append(rooms[random.randint(0,0)]) # first n rooms are normal
    nextRooms.append(rooms[0 + random.randint(0,0)]) # shop
    nextRooms.append(rooms[0 + random.randint(0,0)]) # dishwasher
    nextRooms.append(rooms[0 + random.randint(0,0)]) # risk
    nextRooms.append(rooms[0 + random.randint(0,0)]) # boss

    for i in range(len(nextRooms)):
        while True:
            pos = math.floor(random.randint(0,(constants.gridLength**2)-1))
            if nextFloor[math.floor(pos/constants.gridLength)][pos%constants.gridLength] == None:
                nextFloor[math.floor(pos/constants.gridLength)][pos%constants.gridLength] = nextRooms[i]
                break

    for y in range(5):
        out = ""
        for x in range(5):
            if not nextFloor[y][x] == None:
                out = out + "y "
            else:
                out = out + "n "
        print(out)

    for i in range(constants.gridLength**2):
        yPos = math.floor(i/constants.gridLength)
        xPos = i%constants.gridLength
        if not nextFloor[yPos][xPos] == None: # Only do if there is a room here
                while True:
                    print("LOOP VALIDATE")
                    if not validatePos(nextFloor,yPos,xPos):
                     # Move the room so it will have an adjacent room
                        temp = nextFloor[yPos][xPos]
                        nextFloor[yPos][xPos] = None
                        nextPos = yPos*constants.gridLength + xPos + 1
                        while True:
                            print("LOOP REASSIGN")
                            nextPos = nextPos % (constants.gridLength**2)
                            yPos, xPos = math.floor(nextPos/constants.gridLength), nextPos%constants.gridLength
                            if nextFloor[yPos][xPos] == None:
                                nextFloor[yPos][xPos] = temp
                                break
                            else:
                                nextPos += 1
                                print("NextPos: ", nextPos)
                    else: # Pos is valid finally
                        break



    testFloor = [[None,None,None,None,None],
                [None,None,None,None,None],
                [None,None,None,None,None],
                [None,None,None,None,None],
                [None,None,None,None,None]]
    validX, validY = 0, 0
    for y in range(constants.gridLength):
        out = ""
        for x in range(constants.gridLength):
            if not nextFloor[y][x] == None:
                testFloor[y][x] = 'y'
                validX, validY = x, y
                out = out + "y "
            else:
                testFloor[y][x] = 'n'
                out = out + "n "
        print(out)

    matrices.bucketFill(testFloor,validX,validY) #bucketFill is x,y
    for y in range(constants.gridLength):
        for x in range(constants.gridLength):
            if testFloor[y][x] == 'y':
                return startFloor()

    return nextFloor

def main():
    while True:
        listen()

        # Reset BG
        ctx.blit(images.bg,(0,0))

        # Update All Entities
        for d in curRoom["doors"]:
            d.go(ctx)
        for i in curRoom["items"]:
            i.go(ctx)
        for e in curRoom["enemies"]:
            e.go(ctx, curRoom)
        player.go(ctx, curRoom)

        # Update Window
        pygame.display.update()
        clock.tick(60)

testArray = startFloor()
for y in range(5):
    out = ""
    for x in range(5):
        if not testArray[y][x] == None:
            out = out + "y "
        else:
            out = out + "n "
    print(out)

# for y in range(5):
#     out = ""
#     for x in range(5):
#         out = out + testArray[y][x] + ' '
#     print(out)

main()
