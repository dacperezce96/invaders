import esper

from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_surface import CSurface

def system_blink(world: esper.World, delta_time):
    components = world.get_components(CBlink, CSurface)
    for entity, (c_b, c_s) in components:
        c_b.time += delta_time
        if c_b.time > c_b.delta:
            c_b.time = 0
        if c_b.time > c_b.delta/2:
            c_s.visible = True
        else:
            c_s.visible = False 