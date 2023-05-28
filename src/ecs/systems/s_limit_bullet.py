import esper
import pygame

from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform
from src.ecs.components.tags.c_tag_bullet import CTagBullet

def system_limit_bullet(world:esper.World, screen:pygame.Surface):
    screen_rect = screen.get_rect()
    components = world.get_components(CSurface, CTransform, CTagBullet)
    c_s:CSurface
    c_t:CTransform
    for entity_bullet, (c_s, c_t, c_b) in components:        
        bull_rect = c_s.area.copy()
        bull_rect.topleft = c_t.pos
        if not bull_rect.colliderect(screen_rect):            
            world.delete_entity(entity_bullet)   