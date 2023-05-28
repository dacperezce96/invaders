import pygame
import esper
import json
import random
from src.ecs.components.c_blink import CBlink

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_velocity import CVelocity
from src.ecs.components.tags.c_tag_star import CTagStar

def create_square(world: esper.World, size:pygame.Vector2, color:pygame.Color,
                  pos: pygame.Vector2, vel: pygame.Vector2) -> int:
    square_entity = world.create_entity()
    world.add_component(square_entity, CSurface(size, color))
    world.add_component(square_entity, CTransform(pos))
    if vel is not None:
        world.add_component(square_entity, CVelocity(vel))
    return square_entity

def create_sprite(world: esper.World, pos: pygame.Vector2, vel: pygame.Vector2,
                  surface: pygame.Surface) -> int:
    sprite_entity = world.create_entity()
    world.add_component(sprite_entity, CSurface.from_surface(surface))
    world.add_component(sprite_entity, CTransform(pos))
    if vel is not None:
        world.add_component(sprite_entity, CVelocity(vel))
    return sprite_entity

def create_star(world: esper.World):
    with open("assets/cfg/starfield.json", encoding="utf-8") as start_file:
        star_cfg = json.load(start_file)
    with open("assets/cfg/window.json", encoding="utf-8") as window_file:
        window_cfg = json.load(window_file)
    colors = star_cfg["star_colors"]
    vel_max = star_cfg["vertical_speed"]["max"]
    vel_min = star_cfg["vertical_speed"]["min"]
    blink_min = star_cfg["blink_rate"]["min"]
    blink_max = star_cfg["blink_rate"]["max"]

    for i in range (star_cfg["number_of_stars"]):
        pos_x = (i+1) * (window_cfg["size"]["w"]/(star_cfg["number_of_stars"]+1))
        pos_y = random.randint(0, window_cfg["size"]["h"])
        color = random.choice(colors)
        color_py = pygame.Color(color["r"], color["g"], color["b"])
        vel = random.uniform(vel_min, vel_max)
        rate = random.uniform(blink_min, blink_max)
        entity = create_square(world, pygame.Vector2(1,1), color_py, pygame.Vector2(pos_x,pos_y),pygame.Vector2(0,vel))
        world.add_component(entity, CBlink(rate*2, 0))
        world.add_component(entity, CTagStar())