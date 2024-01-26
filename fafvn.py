import pygame
import os
import os.path
import json

#print(pygame.font.get_fonts())

SCREENSIZE = (1280, 720)

NAME_FONT = None
SAY_FONT = None

window = pygame.display.set_mode(SCREENSIZE)

SCREEN_RECT = window.get_rect()

uiDebug = dict()

charaZBuffer = list()    # Stores what's drawn, in which order
uiZBuffer = list()
textBuffer = list() # Stores every text drawn on screen


class Scene():
    bg = None
    data = list()
    speechBuffer = list() # Stores all the speaches in the chapter
    speech_index = 0
    lineBuffer = list() # Stores all the lines of the current speech
    line_index = 0
    
    def load(chapter : str):
        with open(f"./Story/{chapter}") as chapterFile:
            Scene.data = json.load(chapterFile)
        
        Scene.speechBuffer = Scene.data["script"]
        
        Scene.bg = pygame.image.load(Scene.data["bg"]).convert()
        window.blit(Scene.bg, (0, 0))
    
    def advance():
        Scene.advance = True
    
    def update():     
        # The background is always drawn first
        window.blit(Scene.bg, (0, 0))
        
        # Then the characters
        for chara in charaZBuffer:
            window.blit(chara.sprite, chara.pos)
        
        # Then the UI
        UI.update()

class UIBox():
    name = str()
    size = tuple()
    box = None
    center = None
    pos = None
    
    def __init__(self, name : str, size : tuple, pos  = (0, 0), color = (255, 0, 0, 50), centered = 0) -> None:
        self.name = name
        self.size = size
        self.box = pygame.Surface(size).convert_alpha()
        self.box.fill(color)
        tmp_pos = self.box.get_rect()
        
        match centered:
            case 0:
                self.pos = pos
            case 1:
                self.pos = self.box.get_rect(center = (SCREEN_RECT.centerx, tmp_pos.centery))
            case 2:
                self.pos = self.box.get_rect(center = (tmp_pos.centerx, SCREEN_RECT.centery))
            case 3:
                self.pos = self.box.get_rect(center = SCREEN_RECT.center)
        
        if not centered:
            self.pos = pos
        else:
            self.pos = self.pos.move(pos[0], pos[1])
            self.pos = (self.pos.x, self.pos.y)
        self.center = self.box.get_rect().center
        
        uiDebug[self.name] = self
    
    def center(parent, child : pygame.Surface):
        return child.get_rect(center = parent.center).move(parent.pos)
        

class UI():
    debug = False
    
    boxCharaName = UIBox("BoxCharaName", (181, 39), (140, 532))
    boxCharaText = UIBox("BoxCharaText", (920, 86), (0, 590), centered=1)
    
    def update():
        # Ui is always drawn last, but before text
        for elt in uiZBuffer:
            elt.update()
        # Then, text is drawn
        for text in textBuffer:
            window.blit(text[0][0], text[0][1]) # The character's name
            window.blit(text[1][0], text[1][1])   # What the character says
            textBuffer.remove(text)
        
        # If Debug mode is on, draws the UI Boxes
        if UI.debug:
            for key in uiDebug.keys():
                window.blit(uiDebug[key].box, uiDebug[key].pos)
        

class UIElement():
    sprite = None
    pos = None
    rot = 0.0
    size = 1
    
    def __init__(self, sprite : str, initPos = (0, 0)) -> None:
        self.sprite = pygame.transform.rotozoom(pygame.image.load(sprite).convert_alpha(), self.rot, self.size)
        self.pos = self.sprite.get_rect().move(initPos)
        uiZBuffer.append(self)
    
    def update(self):
        window.blit(self.sprite, self.pos)
    
    def move(self, dx : int, dy : int):
        self.pos = self.pos.move(dx, dy)

class Chara():
    charaFolder = "./Assets/Chara/"
    name = str()
    expression = dict()
    sprite = None
    pos = None
    size = 0.2
    rot = 0.0
    color = tuple()
    
    def __init__(self, name : str, initPos = (80, 20), color = (255, 255, 255)) -> None:
        self.name = name
        self.expression = {sprite.split('.')[0].split("_")[1] : f"{self.charaFolder}{name}/{sprite}" for sprite in os.listdir(self.charaFolder + name)}
        self.color = color
        
        self.sprite = pygame.transform.rotozoom(pygame.image.load(self.expression["normal"]).convert_alpha(), self.rot, self.size)
        self.pos = self.sprite.get_rect().move(initPos)
        
        charaZBuffer.append(self)
        
        self.update()
    
    def __repr__(self):
        return self.name
    
    def update(self):
        window.blit(self.sprite, self.pos)
    
    def set_expression(self, expression : str):
        self.sprite = pygame.transform.rotozoom(pygame.image.load(self.expression[expression]).convert_alpha(), self.rot, self.size)
        self.update()
    
    def move(self, dx : int, dy : int):
        self.pos = self.pos.move(dx, dy)
    
    def say(self, phrase : str):
        text_box = TextWrapper.render_text_list(TextWrapper.wrap_text(phrase, SAY_FONT, UI.boxCharaText.size[0]), SAY_FONT, self.color)
        chara_name = NAME_FONT.render(self.name, True, self.color)
        # Structure : ((chara_name, pos), (text_box, pos))
        textBuffer.append(((chara_name, UIBox.center(UI.boxCharaName, chara_name)), (text_box, (180, 592))))

class TextWrapper():
    def wrap_text(text, font, width):
        """Wrap text to fit inside a given width when rendered.

        :param text: The text to be wrapped.
        :param font: The font the text will be rendered in.
        :param width: The width to wrap to.

        """
        text_lines = text.replace('\t', '    ').split('\n')
        if width is None or width == 0:
            return text_lines

        wrapped_lines = []
        for line in text_lines:
            line = line.rstrip() + ' '
            if line == ' ':
                wrapped_lines.append(line)
                continue

            # Get the leftmost space ignoring leading whitespace
            start = len(line) - len(line.lstrip())
            start = line.index(' ', start)
            while start + 1 < len(line):
                # Get the next potential splitting point
                next = line.index(' ', start + 1)
                if font.size(line[:next])[0] <= width:
                    start = next
                else:
                    wrapped_lines.append(line[:start])
                    line = line[start+1:]
                    start = line.index(' ')
            line = line[:-1]
            if line:
                wrapped_lines.append(line)
        return wrapped_lines


    def render_text_list(lines, font, colour=(255, 255, 255)):
        """Draw multiline text to a single surface with a transparent background.

        Draw multiple lines of text in the given font onto a single surface
        with no background colour, and return the result.

        :param lines: The lines of text to render.
        :param font: The font to render in.
        :param colour: The colour to render the font in, default is white.

        """
        rendered = [font.render(line, True, colour).convert_alpha()
                    for line in lines]

        line_height = font.get_linesize()
        width = max(line.get_width() for line in rendered)
        tops = [int(round(i * line_height)) for i in range(len(rendered))]
        height = tops[-1] + font.get_height()

        surface = pygame.Surface((width, height)).convert_alpha()
        surface.fill((0, 0, 0, 0))
        for y, line in zip(tops, rendered):
            surface.blit(line, (0, y))

        return surface