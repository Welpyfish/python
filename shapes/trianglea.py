import pygame

WHITE =     (255, 255, 255)
BLUE =      (  0,   0, 255)
GREEN =     (  0, 255,   0)
RED =       (255,   0,   0)
TEXTCOLOR = (  0,   0,  0)
(width, height) = (1000, 1000)
background_color = WHITE
running = True

def main():
    global running, screen

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("wiiliam")
    screen.fill(background_color)
    pygame.display.update()

    while running:
        ev = pygame.event.get()

        for event in ev:

            if event.type == pygame.MOUSEBUTTONUP:
                drawCircle()
                pygame.display.update()

            if event.type == pygame.QUIT:
                running = False

def getPos():
    pos = pygame.mouse.get_pos()
    return (pos)

def drawCircle():
    pos=getPos()
    pos1=(pos[0]-15, pos[1])
    pos2=(pos[0]+5, pos[1]+10)
    pos3=(pos[0]+5, pos[1]-10)
    pygame.draw.polygon(screen,(0,0,255),(pos1,pos2,pos3), 3)


if __name__ == '__main__':
    main()