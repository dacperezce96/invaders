import esper
import pygame
from typing import Callable, List

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_enemie import CTagEnemie

def system_collision_bullet_enemy(world:esper.World, explosion_dict:dict, create_explosion:Callable[[esper.World, dict, pygame.Vector2], None], ene_ent:List[int]):
    bullets = world.get_components(CSurface, CTransform, CTagBullet)
    enemies = world.get_components(CSurface, CTransform, CTagEnemie)
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
                points += c_e.puntos                            
                world.delete_entity(bullet_entity)                             
                world.delete_entity(enemy_entety)
                ene_ent.remove(enemy_entety)
                create_explosion(world, explosion_dict, ce_t.pos)
    return points