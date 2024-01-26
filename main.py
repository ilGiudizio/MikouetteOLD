import pygame
from pygame.locals import *
import fafvn

pygame.init()

fafvn.NAME_FONT = pygame.font.SysFont("comicsansms", 35)
fafvn.SAY_FONT = pygame.font.SysFont("comicsansms", 30)

fafvn.Scene.load("chapter1.json")

jotaro = fafvn.Chara("Jotaro", initPos=(660, 20), color=(240, 132, 19))
miku = fafvn.Chara("Miku", color=(0, 255, 255))
print(fafvn.charaZBuffer)

charaTextBox = fafvn.UIElement("./Assets/UI/CharaTextBox.png")

### GAME LOOP ###
keepRunning = True

while keepRunning:
    for event in pygame.event.get():
        if event.type == QUIT:
            keepRunning = False
        if event.type == K_SPACE:
            fafvn.Scene.advance()

    fafvn.Scene.update()
    #miku.say("Hello ! I'm the number one princess in the world ! Seeeekaaaaaaidee ichiban ooohiiimeee saaamaaaaaaaaaaaaaaaaa !")
    jotaro.say("Yare yare daze.")
    pygame.display.flip()