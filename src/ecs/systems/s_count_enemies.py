import esper
from src.ecs.components.tags.c_tag_enemie import CTagEnemie

def system_count_enemies(world:esper.World):
    componets = world.get_component(CTagEnemie)
    return len(componets)