from enum import Enum
import json
import pygame
import esper
from src.ecs.components.c_changing_text import CChangingText
from src.ecs.components.c_move_up import CMoveUp
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.engine.service_locator import ServiceLocator

class TextAlignment(Enum):
    LEFT = 0,
    RIGHT = 1
    CENTER = 2

def create_text(world:esper.World, txt:str, size:int, 
                color:pygame.Color, pos:pygame.Vector2, alignment:TextAlignment) -> int:
    font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", size)
    text_entity = world.create_entity()

    world.add_component(text_entity, CSurface.from_text(txt, font, color))
    txt_s = world.component_for_entity(text_entity, CSurface)

    # De acuerdo al alineamiento, determia el origine de la superficie
    origin = pygame.Vector2(0, 0)
    if alignment is TextAlignment.RIGHT:
        origin.x -= txt_s.area.right
    elif alignment is TextAlignment.CENTER:
        origin.x -= txt_s.area.centerx

    world.add_component(text_entity,
                        CTransform(pos + origin))
    return text_entity

def create_text_move_up(world:esper.World, txt:str, size:int, 
                color:pygame.Color, pos:pygame.Vector2, alignment:TextAlignment) -> int:
    
    with open("assets/cfg/window.json", encoding="utf-8") as window_file:
            window_cfg = json.load(window_file)
    pos_ini = pygame.Vector2(pos.x, pos.y + window_cfg["size"]["h"])
    vel = pygame.Vector2(0,-50)
    entity = create_text(world, txt, size, color, pos_ini, alignment)
    world.add_component(entity, CMoveUp(pos.y))
    world.add_component(entity, CVelocity(vel))
    return entity

def create_text_dinamic(world:esper.World, txt:str, size:int, 
                color:pygame.Color, pos:pygame.Vector2, alignment:TextAlignment) -> int:
    font = ServiceLocator.fonts_service.get("assets/fnt/PressStart2P.ttf", size)
    text_entity = world.create_entity()

    world.add_component(text_entity, CSurface.from_text(txt, font, color))
    world.add_component(text_entity, CChangingText(txt, font, pos.x))
    txt_s = world.component_for_entity(text_entity, CSurface)

    # De acuerdo al alineamiento, determia el origine de la superficie
    origin = pygame.Vector2(0, 0)
    if alignment is TextAlignment.RIGHT:
        origin.x -= txt_s.area.right
    elif alignment is TextAlignment.CENTER:
        origin.x -= txt_s.area.centerx

    world.add_component(text_entity,
                        CTransform(pos + origin))
    return text_entity