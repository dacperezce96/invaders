import  pygame
import esper
from src.ecs.components.c_transform import CTransform
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_player import CTagPlayer

def system_limit_player(world:esper.World, screen:dict):
    componets = world.get_components(CTransform, CSurface, CTagPlayer)
    c_t:CTransform
    c_s:CSurface
    for entity, (c_t, c_s, c_p) in componets:
        cuad_rect = CSurface.get_area_relative(c_s.area, c_t.pos)
        size = cuad_rect.size
        if c_t.pos.x <= 20:
            c_t.pos.x = 20
        if cuad_rect.right >= screen["size"]["w"]-20:
            c_t.pos.x = screen["size"]["w"]-20 - size[0] 