from MediumBoss import *
import os
import Constants
from Bugle import *
from CSPKid import *

class Puri(MediumBoss):

    def __init__(self, attack_power:float, test_monster_name:str, start_pos_x:float, start_pos_y:float):

        img=pygame.image.load(os.path.join("Assets", "Puri.png"))
        super().__init__(attack_power, 50, img, "Mr. Puri", start_pos_x, start_pos_y, 200, 125, ["charge_and_hit", "shoot_attack"], "missile.png", 100, 75)
        self.test_monster_name=test_monster_name
        self.bugle=Bugle(self.monster_rectangle.centerx+30, self.monster_rectangle.centery+30, 110, 50)
        self.projectile = Projectile(1, self.bugle.bugle_rectangle.centerx, self.bugle.bugle_rectangle.centery, 75, 100, pygame.image.load(os.path.join("Assets", "missile.png")))
        self.sound_wave_proj=False
        self.not_spawned=True
        self.current_attack="shoot"
        self.reset_csp_mob()
        
        self.shoot_attack_cooldown_count=4000
        self.first_time_in_room=True
        self.last_csp_mob = pygame.time.get_ticks()
        self.render_csp_mob=False

        self.normal_cooldown_count=3500
        self.normal_cooldown_timer = pygame.time.get_ticks()
        self.in_normal_cooldown=False

        self.csp_speech_bubble=pygame.image.load(os.path.join("Assets", "csp_kids_speech_bubble.png"))
        self.csp_speech_bubble=pygame.transform.scale(self.csp_speech_bubble, (150, 50))
        
    def attack(self, player, screen):
        # self.bugle.rotate_towards_player_and_render(player, self.monster_rectangle, screen)
        # #self.walk_towards_player_and_shoot(player, Constants.puri_speed, Constants.puri_projectile_speed, screen, True)
        # #self.sound_wave(player, Constants.puri_speed, Constants.puri_projectile_speed, screen)
        # #self.walk_and_rapid_fire(player, Constants.puri_speed, Constants.puri_projectile_speed, screen)
        # #self.move_towards_player(player, Constants.puri_speed, screen)
        # self.spawn_csp_kids_and_attack(player, screen)

        
        if self.current_attack=="shoot":
            if self.first_time_in_room:
                self.shoot_attack_cooldown_count+=4000
                self.first_time_in_room=False
            self.bugle.rotate_towards_player_and_render(player, self.monster_rectangle, screen)
            self.walk_and_rapid_fire(player, Constants.puri_speed, Constants.puri_projectile_speed, screen)

            now = pygame.time.get_ticks()
            
            if now - self.last_csp_mob>= self.shoot_attack_cooldown_count:
                self.current_attack="csp_mob"
                self.render_csp_mob=True

        elif self.in_normal_cooldown:
            normal_cooldown_over=self.check_normal_cooldown()
            if normal_cooldown_over:
                self.current_attack="shoot"
                now = pygame.time.get_ticks()
                self.last_csp_mob=now
                self.in_normal_cooldown=False

        elif self.current_attack=="csp_mob":
            screen.blit(self.csp_speech_bubble, (self.monster_rectangle.topright[0]-20, self.monster_rectangle.topright[1]+5))
            if self.render_csp_mob:
                self.reset_csp_mob()
                self.render_csp_mob=False
            self.spawn_csp_kids_and_attack(player, screen)
            if self.check_if_all_csp_kids_dead():
                self.in_normal_cooldown=True
                self.normal_cooldown_timer=pygame.time.get_ticks()
                #self.current_attack="shoot"
                #now = pygame.time.get_ticks()
                #self.last_csp_mob=now
        

    def check_normal_cooldown(self):
        now = pygame.time.get_ticks()
        if now - self.normal_cooldown_timer >= self.normal_cooldown_count:
            self.normal_cooldown=False
            return True
        return False
    
    def realign_projectile(self):
        self.projectile.projectile_rectangle.x,self.projectile.projectile_rectangle.y=self.bugle.bugle_rectangle.center

        #self.projectile.projectile_rectangle.x=self.bugle.bugle_rectangle.topright.x
        #self.projectile.projectile_rectangle.y=self.bugle.bugle_rectangle.topright.y
    
    def walk_and_rapid_fire(self, player, speed, projectile_speed, screen):
        self.current_attack_damage=1
        self.rapid_fire(projectile_speed, player, screen)        
        if not self.stop_moving:
            self.move_towards_player(player, speed, screen)

    def sound_wave(self, player, speed, projectile_speed, screen):
        if not self.sound_wave_proj:
            self.projectile = Projectile(1, self.bugle.bugle_rectangle.centerx, self.bugle.bugle_rectangle.centery, 250, 75, pygame.image.load(os.path.join("Assets", "sonic_wave.png")))
            self.sound_wave_proj=True
        self.rapid_fire(projectile_speed, player, screen)        
        if not self.stop_moving:
            self.move_towards_player(player, speed, screen)

    def reset_csp_mob(self):
        self.csp_kids=[CSP_Kid(1, 1, self.monster_rectangle.centerx-100, self.monster_rectangle.centery, "walk", True), 
                        CSP_Kid(1, 1, self.monster_rectangle.centerx+100, self.monster_rectangle.centery, "walk", True),
                        CSP_Kid(1, 1, self.monster_rectangle.centerx, self.monster_rectangle.centery-100, "walk", True),
                        CSP_Kid(1, 1, self.monster_rectangle.centerx, self.monster_rectangle.centery+100, "walk", True),
                        CSP_Kid(1, 1, self.monster_rectangle.centerx+100, self.monster_rectangle.centery+100, "walk", True),
                        CSP_Kid(1, 1, self.monster_rectangle.centerx-100, self.monster_rectangle.centery+100, "walk", True),
                        CSP_Kid(1, 1, self.monster_rectangle.centerx-100, self.monster_rectangle.centery+100, "walk", True), 
                        CSP_Kid(1, 1, self.monster_rectangle.centerx+100, self.monster_rectangle.centery-100, "walk", True)]

    def rapid_fire(self, projectile_speed, player, screen):
        
        self.stop_moving=False    

        # Checks to see if projectile is at edge of screen

        if self.projectile.projectile_rectangle.x<=0 or self.projectile.projectile_rectangle.x>=Constants.screen_width or self.projectile.projectile_rectangle.y<=0 or self.projectile.projectile_rectangle.y>=Constants.screen_height or self.first_time_shooting or self.projectile.projectile_rectangle.colliderect(player.player_rectangle):
            
            # If stop moving is false, the monster can stop shooting and continue patrolling/following its path

            

            # Sets the projectile's new end destination as the player's updated location
            
            
            self.realign_projectile()
            self.projectile.shoot_coords=(player.player_rectangle.x, player.player_rectangle.y)

            # Calculates the time interval between when it last shot a projectile as an shooting cooldown to make it easier for player

            self.projectile.rotate_towards_player(player)
            self.shoot_straight(projectile_speed, screen)
            self.first_time_shooting=False
        
        else:
            self.shoot_straight(projectile_speed, screen)

    def shoot_straight(self, speed, screen):

        self.current_attack_damage=1
        
        # Distance formula stuff to calculate movement vectors for projectile

        distance = [self.projectile.shoot_coords[0] - self.bugle.bugle_rectangle.centerx, self.projectile.shoot_coords[1] - self.bugle.bugle_rectangle.centery]
        norm = math.sqrt(distance[0] ** 2 + distance[1] ** 2)
        direction = [distance[0] / norm, distance[1 ] / norm]
        movement_vector = [direction[0] * speed, direction[1] * speed]
        self.projectile.projectile_rectangle.move_ip(movement_vector[0], movement_vector[1])
        self.projectile.render(self.projectile.projectile_rectangle.x, self.projectile.projectile_rectangle.y, screen)

    def spawn_csp_kids_and_attack(self, player, screen):
        
        for csp_kid in self.csp_kids:
            if csp_kid.alive:
                csp_kid.attack(player, screen)
                csp_kid.render(csp_kid.monster_rectangle.x, csp_kid.monster_rectangle.y, csp_kid.height, csp_kid.width, screen)
                csp_kid.check_player_collision(player, screen)
            
    def check_if_all_csp_kids_dead(self):
        for csp_kid in self.csp_kids:
            if csp_kid.alive:
                return False
        return True
     


            
    # Overrided render function to handle bugle placement
        
    def render(self, x_pos:float, y_pos:float, height:int, width:int, screen:pygame.display) -> None:
        
        image = pygame.transform.scale(self.img, (width, height))
        self.monster_rectangle = image.get_rect()
        self.monster_rectangle.topleft = (x_pos, y_pos)
        #pygame.draw.rect(screen, (0,255,0), self.monster_rectangle)
        screen.blit(image, self.monster_rectangle)
        self.bugle.render(self.monster_rectangle, screen)