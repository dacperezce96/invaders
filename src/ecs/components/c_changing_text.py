import pygame

class CChangingText:
    def __init__(self, text:str, font:pygame.font.Font, pos_x:int) -> None:
        self.font = font
        self.text = text
        self.pos_x =pos_x