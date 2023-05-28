import math
import random
import pygame
import esper

from src.create.prefab_creator import create_sprite, create_square
from src.create.prefab_creator_interface import TextAlignment, create_text_dinamic
from src.ecs.components.c_animation import CAnimation
from src.ecs.components.c_input_command import CInputCommand
from src.ecs.components.c_surface import CSurface
from src.ecs.components.tags.c_tag_ball import CTagBall
from src.ecs.components.tags.c_tag_block import CTagBlock
from src.ecs.components.tags.c_tag_bullet import CTagBullet
from src.ecs.components.tags.c_tag_bullet_enemy import CTagBulletEnemy
from src.ecs.components.tags.c_tag_enemie import CTagEnemie
from src.ecs.components.tags.c_tag_explosion import CTagExplosion
from src.ecs.components.tags.c_tag_paddle import CTagPaddle
from src.ecs.components.tags.c_tag_player import CTagPlayer
from src.engine.service_locator import ServiceLocator

def create_paddle(world:esper.World, paddle_cfg:dict, player_start_cfg:dict):
    surf = ServiceLocator.images_service.get(paddle_cfg["image"])
    pos = pygame.Vector2(player_start_cfg["pos"]["x"], player_start_cfg["pos"]["y"])
    vel = pygame.Vector2(0,0)
    paddle_ent = create_sprite(world, pos, vel, surf)
    world.add_component(paddle_ent, CTagPaddle())    
    return paddle_ent

def create_player(world:esper.World, player_cfg:dict, player_start_cfg:dict):
    surf = ServiceLocator.images_service.get(player_cfg["image"])
    area = surf.get_rect()
    pos = pygame.Vector2(player_start_cfg["pos"]["x"] - area.centerx, player_start_cfg["pos"]["y"])
    vel = pygame.Vector2(0,0)
    player_ent = create_sprite(world, pos, vel, surf)
    world.add_component(player_ent, CTagPlayer())    
    return player_ent

def create_bullet(world:esper.World, bullet_cfg:dict, pos:pygame.Vector2):
    components = world.get_component(CTagBullet)
    if len(components) < 1:
        vel = pygame.Vector2(0,-(bullet_cfg["velocity"]))
        color = pygame.Color(bullet_cfg["color"]["r"], bullet_cfg["color"]["g"], bullet_cfg["color"]["b"])
        bullet_ent = create_square(world, pygame.Vector2(1,3), color, pos, vel)
        world.add_component(bullet_ent, CTagBullet())   
        ServiceLocator.sounds_service.play("assets/snd/player_shoot.ogg") 
        return bullet_ent

def create_bullet_enemy(world:esper.World, pos:pygame.Vector2):
    vel = pygame.Vector2(0, 80)
    color = pygame.Color(255, 255, 255)
    bullet_ent = create_square(world, pygame.Vector2(1,3), color, pos, vel)
    world.add_component(bullet_ent, CTagBulletEnemy())   
    ServiceLocator.sounds_service.play("assets/snd/laser.ogg") 
    return bullet_ent
    
def create_vida(world:esper.World):
    pos = pygame.Vector2(160,27)
    surf = ServiceLocator.images_service.get("assets/img/invaders_life.png")
    area = surf.get_rect()
    pos = pygame.Vector2(pos.x - area.centerx, pos.y - area.bottom)
    vel = None
    vidas = []
    for i in range(3):
        pos_new = pygame.Vector2(pos.x+(i*10), pos.y)
        player_ent = create_sprite(world, pos_new, vel, surf)
        surf_c = world.component_for_entity(player_ent, CSurface)
        vidas.append(surf_c) 
    return vidas

def  create_explosion(world:esper.World, explosion_dict:dict, pos:pygame.Vector2):
    explosion_surface = ServiceLocator.images_service.get(explosion_dict["image"])
    vel = None
    explosion_entity = create_sprite(world, pos, vel, explosion_surface)
    world.add_component(explosion_entity, CAnimation(explosion_dict["animations"]))
    world.add_component(explosion_entity, CTagExplosion())
    ServiceLocator.sounds_service.play(explosion_dict["sound"])
    
def create_level_flag(world:esper.World):
    pos = pygame.Vector2(200,27)
    surf = ServiceLocator.images_service.get("assets/img/invaders_level_flag.png")
    area = surf.get_rect()
    pos = pygame.Vector2(pos.x - area.centerx, pos.y - area.bottom)
    vel = None
    vidas = []
    for i in range(5):
        pos_new = pygame.Vector2(pos.x+(i*5), pos.y)
        player_ent = create_sprite(world, pos_new, vel, surf)
        surf_c = world.component_for_entity(player_ent, CSurface)
        vidas.append(surf_c) 
    text_ent = create_text_dinamic(world, "01", 7, 
                    pygame.Color(255,255,255), pygame.Vector2(pos.x + 25, 19), TextAlignment.RIGHT)
    surf_c = world.component_for_entity(text_ent, CSurface)
    vidas.append(surf_c)
    return vidas, text_ent

def create_enemies(world:esper.World, level_dict:dict, enemies_dict:dict, nivel:str):
    nivel = level_dict["levels"][nivel]
    pos = pygame.Vector2(49, 37)
    dis_x = 18
    dis_y = 12
    enemies_enities = []
    for i in range(6):
        for j in range(10):
            tipo = nivel[i][j]
            if tipo != "N":
                enemies_enities.append(create_enemy(world, enemies_dict, nivel[i][j], 
                         pygame.Vector2(pos.x + (dis_x*j), pos.y + (dis_y*i))))
    return enemies_enities


def create_enemy(world:esper.World, enemies_dict:dict, tipo:str, pos:pygame.Vector2) -> int:
    enemie_surf = ServiceLocator.images_service.get(enemies_dict[tipo]["image"])
    size = enemie_surf.get_size()
    size = (size[0]/enemies_dict[tipo]["animations"]["number_frames"], size[1])
    pos = pygame.Vector2(pos.x -(size[0]/2), pos.y-(size[0]/2))
    vel = None
    enemie_entity = create_sprite(world, pos, vel, enemie_surf)
    world.add_component(enemie_entity, CTagEnemie(tipo, pygame.Vector2(pos.x, pos.y), enemies_dict[tipo]["points"]))
    world.add_component(enemie_entity, CAnimation(enemies_dict[tipo]["animations"]))
    return enemie_entity


def create_ball(world:esper.World, ball_cfg:dict, ball_start_cfg:pygame.Vector2) -> int:
    surf = ServiceLocator.images_service.get(ball_cfg["image"])
    pos = pygame.Vector2(ball_start_cfg["pos"]["x"], ball_start_cfg["pos"]["y"])
    vel = pygame.Vector2(0,0)
    start_speed = ball_cfg["velocity"]
    random_angle = (math.pi + (math.pi * 0.25)) + (random.random() * math.pi / 2)
    random_angle = math.pi/2
    vel.x = start_speed*math.cos(random_angle)
    vel.y = start_speed*math.sin(random_angle)

    ball_ent = create_sprite(world, pos, vel, surf)
    world.add_component(ball_ent, CTagBall())    
    return ball_ent

def create_play_field(world:esper.World, blocks_field:dict, block_types:dict):
    for element in blocks_field:
        b_type = element["type"]
        pos = pygame.Vector2(element["pos"]["x"], 
                             element["pos"]["y"])
        create_block(world, b_type, block_types[b_type], pos)

def create_block(world:esper.World, type:str, block_info:dict, pos:pygame.Vector2):
    surf = ServiceLocator.images_service.get(block_info["image"])
    block_ent = create_sprite(world, pos, None, surf)
    world.add_component(block_ent, CTagBlock(type))

def create_game_input(world:esper.World):
    quit_to_menu_action = world.create_entity()
    world.add_component(quit_to_menu_action,
                        CInputCommand("QUIT_TO_MENU", 
                                      pygame.K_ESCAPE))
    left_action = world.create_entity()
    world.add_component(left_action,
                        CInputCommand("LEFT", 
                                      pygame.K_LEFT))
    right_action = world.create_entity()
    world.add_component(right_action,
                        CInputCommand("RIGHT", 
                                      pygame.K_RIGHT))
    
    pause_action = world.create_entity()
    world.add_component(pause_action,
                        CInputCommand("PAUSE", 
                                      pygame.K_p))
    
    shoot_action = world.create_entity()
    world.add_component(shoot_action,
                        CInputCommand("SHOOT", 
                                      pygame.K_z))
    