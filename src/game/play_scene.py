import json
import pygame
from src.create.prefab_creator import create_square, create_star
from src.ecs.components.c_blink import CBlink
from src.ecs.components.c_changing_text import CChangingText
from src.ecs.components.tags.c_tag_guia import CTagGuia
from src.ecs.systems.s_animation import system_animation
from src.ecs.systems.s_blink import system_blink
from src.ecs.systems.s_collision_bullet_enemy import system_collision_bullet_enemy
from src.ecs.systems.s_collision_bullet_player import system_collision_bullet_player
from src.ecs.systems.s_count_enemies import system_count_enemies
from src.ecs.systems.s_count_level import system_count_flags
from src.ecs.systems.s_count_vidas import system_count_vidas
from src.ecs.systems.s_limit_bullet import system_limit_bullet
from src.ecs.systems.s_limit_bullets_enemy import system_limit_bullet_en
from src.ecs.systems.s_move_enemies import system_move_enemies
from src.ecs.systems.s_player_limit import system_limit_player
from src.ecs.systems.s_shoot_enemy import system_shoot_enemy
from src.ecs.systems.s_star_loop import system_star_loop

from src.engine.scenes.scene import Scene
from src.create.prefab_creator_game import create_bullet, create_enemies, create_explosion, create_game_input, create_level_flag, create_player, create_vida
from src.create.prefab_creator_interface import TextAlignment, create_text, create_text_dinamic
from src.ecs.components.c_input_command import CInputCommand, CommandPhase
from src.ecs.components.c_surface import CSurface
from src.ecs.components.c_transform import CTransform 
from src.ecs.components.c_velocity import CVelocity
from src.ecs.systems.s_movement import system_movement
import src.engine.game_engine
from src.engine.service_locator import ServiceLocator

class PlayScene(Scene):
    def __init__(self, level_path:str, engine:'src.engine.game_engine.GameEngine') -> None:
        super().__init__(engine)
        with open(level_path) as level_file:
            self.level_cfg = json.load(level_file)
        with open("assets/cfg/player.json") as player_file:
            self.player_cfg = json.load(player_file)
        with open("assets/cfg/enemies.json") as enemies_file:
            self.enemies_cfg = json.load(enemies_file)
        with open("assets/cfg/explosion_enemy.json") as explo_ene:
            self.explo_ene_cfg = json.load(explo_ene)
        with open("assets/cfg/explosion_player.json") as explo_play:
            self.explo_play_cfg = json.load(explo_play)
                      
        self.color_title = pygame.Color(engine._interface_cfg['title_text_color']['r'], engine._interface_cfg['title_text_color']['g'], engine._interface_cfg['title_text_color']['b']) 
        self.color_normal = pygame.Color(engine._interface_cfg['normal_text_color']['r'], engine._interface_cfg['normal_text_color']['g'], engine._interface_cfg['normal_text_color']['b'])
        self.color_high = pygame.Color(engine._interface_cfg['high_score_color']['r'], engine._interface_cfg['high_score_color']['g'], engine._interface_cfg['high_score_color']['b'])
        self.high_score = engine._interface_cfg['high_score_max_value']
        self.size_text = 7
        self.score = 0
        self.window = engine._window_cfg
        self.screen = engine.screen
        self.interface = engine._interface_cfg
        self._paused = False
        self.crear_enemigos = True
        self.time_start = 0
        self.nivel = 1
        self.vidas = 4
        self.enemies_ents = []
        self.time_shoot = 0
        self.dead = False
        self.dead_time = 0

    def do_create(self):
        sound = ServiceLocator.sounds_service.play("assets/snd/game_start.ogg")
        guia_entity = create_square(self.ecs_world, pygame.Vector2(1,1),
                      pygame.Color(0,0,0),
                      pygame.Vector2(0,0),
                      pygame.Vector2(15,0))
        self.ecs_world.add_component(guia_entity, CTagGuia())        
        create_star(self.ecs_world)
        create_text(self.ecs_world, "1UP", self.size_text, 
                    self.color_title, pygame.Vector2(42, 10), TextAlignment.CENTER)
        create_text(self.ecs_world, "HI-SCORE", self.size_text, 
                    self.color_title, pygame.Vector2(118, 10), TextAlignment.CENTER)
        score_ent = create_text_dinamic(self.ecs_world, "00", self.size_text, 
                    self.color_normal, pygame.Vector2(65, 19), TextAlignment.RIGHT)
        self.text_score = self.ecs_world.component_for_entity(score_ent, CChangingText)
        high_ent = create_text_dinamic(self.ecs_world, str(self.interface["high_score_max_value"]), self.size_text, 
                    self.color_high, pygame.Vector2(140, 19), TextAlignment.RIGHT)        
        self.text_high = self.ecs_world.component_for_entity(high_ent, CChangingText)
        player_ent = create_player(self.ecs_world, 
                                   self.player_cfg, 
                                   self.level_cfg["player_start"])
        self._p_v = self.ecs_world.component_for_entity(player_ent, CVelocity)
        self._p_t = self.ecs_world.component_for_entity(player_ent, CTransform)
        self._p_s = self.ecs_world.component_for_entity(player_ent, CSurface)
                
        paused_text_ent = create_text(self.ecs_world, "PAUSED", self.size_text, 
                    self.color_title, pygame.Vector2(self.window["size"]["w"]/2, self.window["size"]["h"]/2), 
                    TextAlignment.CENTER)
        self.p_txt_s = self.ecs_world.component_for_entity(paused_text_ent, CSurface)
        self.p_txt_s.visible = self._paused

        paused_text_ent = create_text(self.ecs_world, "GAME OVER", self.size_text, 
                    self.color_normal, pygame.Vector2(self.window["size"]["w"]/2, self.window["size"]["h"]/2), 
                    TextAlignment.CENTER)
        self.game_over_txt_s = self.ecs_world.component_for_entity(paused_text_ent, CSurface)
        self.game_over_txt_s.visible = False

        paused_text_ent = create_text(self.ecs_world, "NEXT LEVEL", self.size_text, 
                    self.color_normal, pygame.Vector2(self.window["size"]["w"]/2, self.window["size"]["h"]/2), 
                    TextAlignment.CENTER)
        self.next_level_txt_s = self.ecs_world.component_for_entity(paused_text_ent, CSurface)
        self.next_level_txt_s.visible = False

        start_text_ent = create_text(self.ecs_world, "GAME START", self.size_text, 
                    self.color_normal, pygame.Vector2(self.window["size"]["w"]/2, self.window["size"]["h"]/2), 
                    TextAlignment.CENTER)
        
        self.start_text_surf = self.ecs_world.component_for_entity(start_text_ent, CSurface)

        self.vidas_render = create_vida(self.ecs_world)

        self.flags, self.flag_ent = create_level_flag(self.ecs_world)
        

        self._paused = False
        create_game_input(self.ecs_world)
    
    def do_update(self, delta_time: float):
        system_count_vidas(self.ecs_world, self.vidas_render, self.vidas)
        system_count_flags(self.ecs_world, self.flags, self.nivel, self.flag_ent)
        self.time_start += delta_time
        self.text_score.text = str(self.score)
        if self.time_start > 3:
            if self.crear_enemigos:
                self.crear_enemigos = False
                self.enemies_ents = create_enemies(self.ecs_world, self.level_cfg, self.enemies_cfg, str((self.nivel-1)%5))
            self.start_text_surf.visible = False
            self.next_level_txt_s.visible = False
        if self.score > self.interface["high_score_max_value"]:
            self.interface["high_score_max_value"] = self.score
            self.text_high.text = str(self.interface["high_score_max_value"])
        system_limit_player(self.ecs_world, self.window)
        system_limit_bullet(self.ecs_world, self.screen)
        system_limit_bullet_en(self.ecs_world, self.screen)
        if not self._paused:
            if not self.dead:
                self.time_shoot += delta_time
                if self.time_shoot > 1.5:
                    self.time_shoot = 0
                    system_shoot_enemy(self.ecs_world, self.nivel)
            system_move_enemies(self.ecs_world, self.enemies_ents)
            system_movement(self.ecs_world, delta_time)
            system_blink(self.ecs_world, delta_time)
            system_star_loop(self.ecs_world, self.window["size"]["h"])
            muerte = system_collision_bullet_player(self.ecs_world, self.explo_play_cfg, create_explosion)                
            self.vidas += muerte
            if muerte == -1:
                self.dead = True
                if self.vidas < 1:
                    self.game_over_txt_s.visible = True
                    quit_to_menu_action = self.ecs_world.create_entity()
                    ServiceLocator.sounds_service.play("assets/snd/game_over.ogg")
                    self.ecs_world.add_component(quit_to_menu_action,
                        CInputCommand("QUIT_TO_MENU", 
                                      pygame.K_z))
            if self.dead and self.vidas > 0:
                self.dead_time += delta_time
                if self.dead_time > 3:
                    self.dead = False
                    self.dead_time = 0
                    player_ent = create_player(self.ecs_world, 
                                   self.player_cfg, 
                                   self.level_cfg["player_start"])
                    self._p_v = self.ecs_world.component_for_entity(player_ent, CVelocity)
                    self._p_t = self.ecs_world.component_for_entity(player_ent, CTransform)
                    self._p_s = self.ecs_world.component_for_entity(player_ent, CSurface)

            self.score += system_collision_bullet_enemy(self.ecs_world, self.explo_ene_cfg, create_explosion, self.enemies_ents)
            if not self.crear_enemigos:
                if system_count_enemies(self.ecs_world) < 1:
                    self.crear_enemigos = True
                    self.next_level_txt_s.visible = True
                    self.nivel += 1
                    self.time_start = 0
            system_animation(self.ecs_world, delta_time)

    def do_clean(self):
        self._paused = False
        self.score = 0
        self.time_start = 0
        self.vidas = 4
        self.nivel = 1
        self.crear_enemigos = True
        self.enemies_ents = []
        self.dead = False

    def do_action(self, action: CInputCommand):
        if action.name == "LEFT":
            if action.phase == CommandPhase.START:
                self._p_v.vel.x -= self.player_cfg["velocity"]
            elif action.phase == CommandPhase.END:
                self._p_v.vel.x += self.player_cfg["velocity"]
        elif action.name == "RIGHT":
            if action.phase == CommandPhase.START:
                self._p_v.vel.x += self.player_cfg["velocity"]
            elif action.phase == CommandPhase.END:
                self._p_v.vel.x -= self.player_cfg["velocity"]
        elif action.name == "SHOOT":
            if action.phase == CommandPhase.START:
                player_rect = CSurface.get_area_relative(self._p_s.area, self._p_t.pos)
                if not self.crear_enemigos and not self.dead and not self._paused:
                    create_bullet(self.ecs_world, self.player_cfg["bullet"], pygame.Vector2(player_rect.center[0],player_rect.center[1]))

        if action.name == "QUIT_TO_MENU" and action.phase == CommandPhase.START:
            self.switch_scene("MENU_SCENE")
        
        if action.name == "PAUSE" and action.phase == CommandPhase.START:
            if self.time_start > 3:
                self._paused = not self._paused
                if self._paused:
                    ServiceLocator.sounds_service.play("assets/snd/game_paused.ogg")
                self.p_txt_s.visible = self._paused
