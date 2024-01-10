from pygame import *
import os
from Room import *
from Constants import *
from Biome import *
from Player2 import *
from Obstacles import *
from Monster import *
from TestMonsterMedium import *
from TestMonster import *
from Kohli import *
from CricketNPC import *
from Exit import *

class Overworld(Room):
    
    def __init__(self):
        super().__init__(0, 0, 0)
        
        # intialize all biomes with their respective obstacles
        self.room1 = Biome("room1", "room1.png", [], [("USE ARROW KEYS TO MOVE AROUND.", (screen_width - 612) // 2, 235), ("PRESS SPACE TO ATTACK.", (screen_width - 421) // 2, 535)], False)
        self.obstacle1 = Obstacles("test_object1.png", 0, 0, screen_width, 290)
        self.obstacle2 = Obstacles("test_object1.png", 0, 500, screen_width, 300)
        self.obstacle3 = Obstacles("test_object1.png", 0, 0, 50, screen_height)
        self.room1.add_obstacles([self.obstacle1, self.obstacle2, self.obstacle3])
        
        exit = Exit(-100, 380, self.room1, "left", 100, 100)
        self.room2 = Biome("room2", "room2.png", [exit], [("THE FIRST INGREDIENT IS IN THE EDEN GARDENS.", 15, 235), ("UNFORTUNATELY, THE INDIAN CRICKET TEAM IS VALIANTLY DEFENDING IT.", 15, 535)], False)
        self.obstacle4 = Obstacles("test_object1.png", 0, 0, 925, 290)
        self.obstacle5 = Obstacles("test_object1.png", 1200, 0, 400, screen_height)
        self.obstacle6 = Obstacles("test_object1.png", 0, 0, screen_width, 200)
        self.room2.add_obstacles([self.obstacle2, self.obstacle4, self.obstacle5, self.obstacle6])
        
        self.cricketroom1 = Biome("cricketroom1", "cricketroom1.png", [Exit(1000, 895, self.room2, "down", 100, 100)], [], False)
        self.obstacle7 = Obstacles("test_object1.png", 0, 0, 705, 150)
        self.obstacle8 = Obstacles("test_object1.png", 935, 0, screen_width-935, 150)
        self.obstacle9 = Obstacles("test_object1.png", screen_width-150, 0, 150, screen_height)
        self.obstacle10 = Obstacles("test_object1.png", screen_width-340, screen_height-155, 340, 155)
        self.obstacle11 = Obstacles("test_object1.png", 0, 290, 600, 200)
        self.obstacle12 = Obstacles("test_object1.png", 0, screen_height-155, 905, 155)
        self.cricketroom1.add_obstacles([self.obstacle7, self.obstacle8, self.obstacle9, self.obstacle10, self.obstacle11, self.obstacle12])
        
        self.cricketroom2 = Biome("cricketroom2", "cricketroom2.png", [Exit(800, 895, self.cricketroom1, "down", 100, 100)], [], False)
        self.obstacle13 = Obstacles("test_object1.png", 0, 0, screen_width, 150)
        self.obstacle14 = Obstacles("test_object1.png", 950, screen_height-150, screen_width-950, 150)
        self.obstacle15 = Obstacles("test_object1.png", 0, screen_height-160, 700, 160)
        self.obstacle16 = Obstacles("test_object1.png", 0, 0, 150, screen_height)
        self.cricketroom2.add_obstacles([self.obstacle13, self.obstacle9, self.obstacle14, self.obstacle15, self.obstacle16])
        
        self.cricketroom3 = Biome("cricketroom3", "cricketroom3.png", [Exit(1550, 200, self.cricketroom1, "right", 100, 100), Exit(1550, 600, self.cricketroom1, "right", 100, 100)], [], False)
        self.obstacle17 = Obstacles("test_object1.png", 0, screen_height-150, screen_width, 150)
        self.obstacle18 = Obstacles("test_object1.png", screen_width-600, 290, 600, 200)
        self.cricketroom3.add_obstacles([self.obstacle7, self.obstacle8, self.obstacle17, self.obstacle16, self.obstacle18])
        
        self.cricketroom4 = Biome("cricketroom4", "cricketroom4.png", [Exit(800, 895, self.cricketroom3, "down", 100, 100)], [], False)
        self.cricketroom4.add_obstacles([self.obstacle7, self.obstacle8, self.obstacle9, self.obstacle14, self.obstacle15, self.obstacle16])
        
        self.cricketroom5 = Biome("cricketroom5", "cricketroom2.png", [Exit(800, 895, self.cricketroom4, "down", 100, 100)], [], False)
        self.cricketroom5.add_obstacles([self.obstacle13, self.obstacle9, self.obstacle14, self.obstacle15, self.obstacle16])
        
        self.room1.add_exits([Exit(1550, 380, self.room2, "right", 100, 100)])
        self.room2.add_exits([Exit(1000, 180, self.cricketroom1, "up", 70, 30)])
        self.cricketroom1.add_exits([Exit(800, -95, self.cricketroom2, "up", 100, 100), Exit(-95, 200, self.cricketroom3, "left", 100, 100), Exit(-95, 600, self.cricketroom3, "left", 100, 100)])
        self.cricketroom3.add_exits([Exit(800, -95, self.cricketroom4, "up", 100, 100)])
        self.cricketroom4.add_exits([Exit(800, -95, self.cricketroom5, "up", 100, 100)])
        
        # set font
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        
        # create a monster
        monster1=Kohli(10.0, 9.0, "Kohli", 800, 100)
        self.cricketroom4.add_monsters([monster1])

        npc_cricker_player_1=CricketNPC(10.0, 9.0, "NPC Cricket Player 1", 935, 150, "shoot and follow path")
        npc_cricker_player_1.path_coords=[(npc_cricker_player_1.start_pos_x, npc_cricker_player_1.start_pos_y), 
                                          (npc_cricker_player_1.start_pos_x+450, npc_cricker_player_1.start_pos_y), 
                                          (npc_cricker_player_1.start_pos_x+450, npc_cricker_player_1.start_pos_y+450), 
                                          (npc_cricker_player_1.start_pos_x, npc_cricker_player_1.start_pos_y+450)]
        self.cricketroom1.add_monsters([npc_cricker_player_1])


        npc_cricker_player_2=CricketNPC(10.0, 9.0, "NPC Cricket Player 2", 700, 500, "hit")
        self.cricketroom1.add_monsters([npc_cricker_player_2])

        npc_cricker_player_3=CricketNPC(10.0, 9.0, "NPC Cricket Player 3", 180, 150, "shoot and patrol")
        npc_cricker_player_3.patrol_direction="x"
        npc_cricker_player_3.patrol_distance=1220
        self.cricketroom2.add_monsters([npc_cricker_player_3])

        npc_cricker_player_4=CricketNPC(10.0, 9.0, "NPC Cricket Player 4", 700, 150, "hit")
        self.cricketroom2.add_monsters([npc_cricker_player_4])

        npc_cricker_player_5=CricketNPC(10.0, 9.0, "NPC Cricket Player 5", 250, 150, "shoot and patrol")
        npc_cricker_player_5.patrol_direction="y"
        npc_cricker_player_5.patrol_distance=520
        self.cricketroom2.add_monsters([npc_cricker_player_5])

        npc_cricker_player_6=CricketNPC(10.0, 9.0, "NPC Cricket Player 6", 690, 150, "shoot and follow path")
        npc_cricker_player_6.path_coords=[(npc_cricker_player_6.start_pos_x, npc_cricker_player_6.start_pos_y), 
                                          (npc_cricker_player_6.start_pos_x-520, npc_cricker_player_6.start_pos_y), 
                                          (npc_cricker_player_6.start_pos_x-520, npc_cricker_player_6.start_pos_y+470), 
                                          (npc_cricker_player_6.start_pos_x, npc_cricker_player_6.start_pos_y+470)]
        self.cricketroom3.add_monsters([npc_cricker_player_6])

        npc_cricker_player_7=CricketNPC(10.0, 9.0, "NPC Cricket Player 7", 190, 600, "hit")
        self.cricketroom3.add_monsters([npc_cricker_player_7])




    def game_over(self, screen:pygame.display):
        img = pygame.image.load(os.path.join("Assets", "game_over_screen.jpg"))
        image = pygame.transform.scale(img, (screen_width, screen_height))
        screen.blit(image, (0, 0))
        pygame.display.update()
        
    def going_to_dungeon(self, player:Player2, biome:Biome, screen:pygame.display):
        if biome.dungeon:
            if (player.player_rectangle.topleft[0] < biome.dungeon_x + 10 and player.player_rectangle.topleft[0] > biome.dungeon_x - 10) and (player.player_rectangle.topleft[1] < biome.dungeon_y + 10 and player.player_rectangle.topleft[1] > biome.dungeon_y - 10):
                image = self.dungeon.get_image()
                screen.fill((0, 0, 0))
                pygame.display.update()
                pygame.time.wait(500)
                for i in range(30, 1, -2):
                    screen.blit(image, (int((screen_width - screen_width/i)/2), 0), (int((screen_width - screen_width/i)/2), 0, int(screen_width/i), screen_height))
                    pygame.display.update()
                    pygame.time.wait(100)
                # player.player_rectangle.topleft(dungeon_x_pos, dungeon_y_pos)
                player.player_rectangle.topleft = (1200, 250)
                return self.dungeon
        return None
    
    def going_to_next_biome(self, player:Player2, biome:Biome, curr_screen_x_pos:int, curr_screen_y_pos:int, screen:pygame.display):    
        curr_biome = biome
        for exit in curr_biome.exits:
            if (player.player_rectangle.topleft[0] < exit.x + exit.width and player.player_rectangle.topleft[0] > exit.x - exit.width) and (player.player_rectangle.topleft[1] < exit.y + exit.height and player.player_rectangle.topleft[1] > exit.y - exit.height):
                # moving down or up
                if (exit.player_direction == "down" or exit.player_direction == "up"):
                    if exit.player_direction == "down":
                        change = -100
                        y_pos = screen_height
                    else:
                        change = 100
                        y_pos = -1 * screen_height
                    count = screen_height
                    while count > 0:
                        curr_screen_y_pos += change
                        curr_biome.render(curr_screen_x_pos, curr_screen_y_pos, player, screen)
                        y_pos += change
                        exit.next_room.render(curr_screen_x_pos, y_pos, player, screen)
                        new_y = player.player_rectangle.topleft[1] + change
                        if new_y < 0:
                            new_y = player.player_rectangle[3] + 20
                        if new_y > screen_height:
                            new_y = screen_height - 10
                        player.player_rectangle.topleft = (player.player_rectangle.topleft[0], new_y)
                        player.render(player.player_rectangle.topleft[0], player.player_rectangle.topleft[1], screen)
                        count -= 100
                        pygame.display.update()
                        pygame.time.wait(10)
                    if curr_biome == self.cricketroom1 and exit.player_direction == "down":
                        player.player_rectangle.topleft = (player.player_rectangle.topleft[0], 220)
                        player.render(player.player_rectangle.topleft[0], player.player_rectangle.topleft[1], screen)
                        pygame.display.update()
                # moving left or right
                else:
                    if exit.player_direction == "right":
                        change = -100
                        x_pos = screen_width
                    else:
                        change = 100
                        x_pos = -1 * screen_width
                    count = screen_width
                    while count > 0:
                        curr_screen_x_pos += change
                        curr_biome.render(curr_screen_x_pos, curr_screen_y_pos, player, screen)
                        x_pos += change
                        exit.next_room.render(x_pos, curr_screen_y_pos, player, screen)
                        new_x = player.player_rectangle.topleft[0] + change
                        if new_x < 0:
                            new_x = 10
                        if new_x > screen_width - player.player_rectangle[2]:
                            new_x = screen_width - player.player_rectangle[2] - 50
                        player.player_rectangle.topleft = (new_x, player.player_rectangle.topleft[1])
                        player.render(player.player_rectangle.topleft[0], player.player_rectangle.topleft[1], screen)
                        count -= 100
                        pygame.display.update()
                        pygame.time.wait(20)
                exit.next_room.render(0, 0, player, screen)
                return exit.next_room
        return None
    
    def obstacles_in_biome(self, player:Player2, biome:Biome):
        obstacle_rects = biome.obstacles_rect
        for obstacle_rect in obstacle_rects:
            if player.player_rectangle.colliderect(obstacle_rect):
                if player.direction == "left":
                    x_pos = obstacle_rect[0] + obstacle_rect[2]
                    player.player_rectangle.topleft = (x_pos, player.player_rectangle.topleft[1])
                elif player.direction == "right":
                    x_pos = obstacle_rect[0] - player.player_rectangle[2]
                    player.player_rectangle.topleft = (x_pos, player.player_rectangle.topleft[1])
                elif player.direction == "up":
                    y_pos = obstacle_rect[1] + obstacle_rect[3]
                    player.player_rectangle.topleft = (player.player_rectangle.topleft[0], y_pos)
                else:
                    y_pos = obstacle_rect[1] - player.player_rectangle[3]
                    player.player_rectangle.topleft = (player.player_rectangle.topleft[0], y_pos)
    
    def monster_attack(self, curr_biome:Biome, player:Player2, screen:pygame.display):
        monsters = curr_biome.monsters
        mon_alive = 0

        for m in monsters:
            if m.alive:
                
                mon_alive+=1

                # If the player isn't attacking and they touch monster, they should take damage

                if player.player_rectangle.colliderect(m.monster_rectangle) and not player.attacking:

                    # Kohli has more cooldowns, so the player cannot take damage if the Kohli is in a cooldown

                    if isinstance(m, Kohli):
                        if not m.in_cooldown:
                            
                            # Calculating the time between attacks again as a cooldown

                            now = pygame.time.get_ticks()
                            if now - m.last_damage >= m.attack_cooldown or m.first_time_attacking:
                                m.last_damage = now
                                player.get_attacked(m.current_attack_damage, screen)
                                m.first_time_attacking=False
                    else:

                        # Same cooldown logic if not Kohli

                        now = pygame.time.get_ticks()
                        if now -m.last_damage >= m.attack_cooldown or m.first_time_attacking:
                            m.last_damage = now
                            player.get_attacked(m.current_attack_damage, screen)
                            m.first_time_attacking=False
                    
                # Projectile is realigned and player takes damage if player gets hit by projectile

                if player.player_rectangle.colliderect(m.projectile.projectile_rectangle) and m.stop_moving:
                    m.realign_projectile()
                    m.current_attack_damage=m.projectile.damage
                    player.get_attacked(m.current_attack_damage, screen)
                    m.stop_moving=False    
                
                
            return False, monsters
        else:
            return True, monsters
        
    def display_text(self, words_startx_starty:list, curr_biome:Biome, player:Player2, text_index:int, previous_text:list, screen:pygame.display):
        """
        start_y = 100 + text_index * 50
        size = self.font.size(words)
        start_x = (screen_width - size[0]) // 2
        """
        words = words_startx_starty[0]
        start_x = words_startx_starty[1]
        start_y = words_startx_starty[2]
        for i in range(1, len(words) + 1):
            curr_biome.render(0, 0, player, screen)
            for t in previous_text:
                screen.blit(t[0], t[1])
                pygame.display.update()
            text = self.font.render(words[0:i], True, (0, 0, 0))
            text_rect = text.get_rect()
            text_rect = (start_x, start_y)
            screen.blit(text, text_rect)
            pygame.display.update()
            pygame.time.wait(1)
        return (text, text_rect)        