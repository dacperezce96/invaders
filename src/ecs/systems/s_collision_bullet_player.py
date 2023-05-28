import esper
import pygame
from typing import Callable, List

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_bullet_enemy import CTagBulletEnemy
from src.ecs.components.tags.c_tag_enemie import CTagEnemie
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_collision_bullet_player(world:esper.World, explosion_dict:dict, create_explosion:Callable[[esper.World, dict, pygame.Vector2], None]):
    bullets = world.get_components(CSurface, CTransform, CTagBulletEnemy)
    enemies = world.get_components(CSurface, CTransform, CTagPlayer)
    cb_s:CSurface
    cb_t:CTransform
    ce_s:CSurface
    ce_t:CTransform
    points = 0
    for bullet_entity, (cb_s, cb_t, c_b) in bullets:
        bull_rect = CSurface.get_area_relative(cb_s.area, cb_t.pos)
        for enemy_entety, (ce_s, ce_t, c_e) in enemies:
            enemy_rect = CSurface.get_area_relative(ce_s.area, ce_t.pos)
            if bull_rect.colliderect(enemy_rect):
                points = -1                          
                world.delete_entity(bullet_entity)                             
                world.delete_entity(enemy_entety)
                create_explosion(world, explosion_dict, ce_t.pos)
    return points