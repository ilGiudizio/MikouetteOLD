import pygame
from pygame.locals import *
import fafvn

pygame.init()

fafvn.NAME_FONT = pygame.font.SysFont("comicsansms", 35)
fafvn.SAY_FONT = pygame.font.SysFont("comicsansms", 30)

fafvn.Scene.load("chapter1")

print(fafvn.charaZBuffer)

charaTextBox = fafvn.UIElement("./Assets/UI/CharaTextBox.png")

### GAME LOOP ###
keepRunning = True

while keepRunning:
    for event in pygame.event.get():
        if event.type == QUIT:
            keepRunning = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                fafvn.Scene.advance()

    fafvn.Scene.update()
    pygame.display.flip()