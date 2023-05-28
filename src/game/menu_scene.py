import pygame
import json
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_move_up import CMoveUp
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_move_up import system_move_up
from src.ecs.systems.s_movement import system_movement
from src.ecs.systems.s_star_loop import system_star_loop

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_interface import TextAlignment, create_text, create_text_move_up
from src.create.prefab_creator import create_sprite, create_star
from src.ecs.components.c_input_command import CInputCommand, CommandPhase 
import src.engine.game_engine
from src.engine.service_locator import ServiceLocator

class MenuScene(Scene):
    def __init__(self, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)               
        self.color_title = pygame.Color(engine._interface_cfg['title_text_color']['r'], engine._interface_cfg['title_text_color']['g'], engine._interface_cfg['title_text_color']['b']) 
        self.color_normal = pygame.Color(engine._interface_cfg['normal_text_color']['r'], engine._interface_cfg['normal_text_color']['g'], engine._interface_cfg['normal_text_color']['b'])
        self.color_high = pygame.Color(engine._interface_cfg['high_score_color']['r'], engine._interface_cfg['high_score_color']['g'], engine._interface_cfg['high_score_color']['b'])
        self.interface = engine._interface_cfg
        self.size_text = 7
        self.window = engine._window_cfg
        self.change = False
        self.now = False

    def do_create(self):
        create_star(self.ecs_world)
        create_text_move_up(self.ecs_world, "1UP", self.size_text, 
                    self.color_title, pygame.Vector2(42, 10), TextAlignment.CENTER)
        create_text_move_up(self.ecs_world, "HI-SCORE", self.size_text, 
                    self.color_title, pygame.Vector2(118, 10), TextAlignment.CENTER)
        create_text_move_up(self.ecs_world, "00", self.size_text, 
                    self.color_normal, pygame.Vector2(65, 19), TextAlignment.RIGHT)
        create_text_move_up(self.ecs_world, str(self.interface["high_score_max_value"]), self.size_text, 
                    self.color_high, pygame.Vector2(140, 19), TextAlignment.RIGHT)
        logo_surface = ServiceLocator.images_service.get("assets/img/invaders_logo_title.png")
        size = logo_surface.get_size()
        pos = pygame.Vector2(self.window["size"]["w"]/2 - size[0]/2, 45 + self.window["size"]["h"])
        logo_enity = create_sprite(self.ecs_world, pos, pygame.Vector2(0,-50), logo_surface)
        self.ecs_world.add_component(logo_enity, CMoveUp(45))
        instruction_entity = create_text_move_up(self.ecs_world, "PRESS Z TO START", self.size_text, 
                    self.color_title, pygame.Vector2(self.window["size"]["w"]/2, 120), TextAlignment.CENTER)
        self.ecs_world.add_component(instruction_entity, CBlink(1 , 0))
        create_text_move_up(self.ecs_world, "©2023 - MISO - Uniandes", self.size_text, 
                    self.color_normal, pygame.Vector2(self.window["size"]["w"]/2, 200), TextAlignment.CENTER)
        start_game_action = self.ecs_world.create_entity()
        self.ecs_world.add_component(start_game_action,
                                     CInputCommand("START_GAME", pygame.K_z))
        
    def do_action(self, action: CInputCommand):
        if action.name == "START_GAME":
            if action.phase == CommandPhase.START:
                if self.change:
                    self.switch_scene("LEVEL_01")
                else:
                    self.now = True

        
    def do_update(self, delta_time: float):        
        system_movement(self.ecs_world, delta_time)
        system_blink(self.ecs_world, delta_time)
        system_star_loop(self.ecs_world, self.window["size"]["h"])
        self.change = system_move_up(self.ecs_world, self.now)

    def do_clean(self):
        self.change = False
        self.now = False  