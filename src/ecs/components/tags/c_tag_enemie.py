import pygame

class CTagEnemie:
    def __init__(self, b_type:str, pos:pygame.Vector2, puntos:int) -> None:
        self.b_type = b_type
        self.pos = pos
        self.puntos = puntos