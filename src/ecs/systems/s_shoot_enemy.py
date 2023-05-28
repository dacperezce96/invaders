import esper
import pygame
import random
from src.create.prefab_creator_game import create_bullet_enemy

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemie import CTagEnemie

def system_shoot_enemy(world:esper.World, nivel:int):
    components = world.get_components(CSurface, CTransform, CTagEnemie)
    c_t:CTransform
    dificultad = ((nivel-1)%10)*100
    enemigos = len(components)
    factor = -(80/45)*enemigos + 102
    for entity, (c_s, c_t, c_b) in components:        
        ran = random.randint(0,1000-dificultad)
        width = c_s.area.width/2 
        if ran < factor:
            pos = c_t.pos
            create_bullet_enemy(world, pygame.Vector2(pos.x+width, pos.y))