import pygame
from Player2 import *
import math

class Projectile:

    def __init__(self,damage:float, x_pos:float, y_pos:float, height:int, width:int, img:pygame.image):
        self.damage=damage
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.height=height
        self.width=width
        self.img=img
        self.img=pygame.transform.scale(self.img, (self.height, self.width))
        self.projectile_rectangle=self.img.get_rect()
        self.projectile_rectangle.topleft = (x_pos, y_pos)
        
        self.shoot_coords=(0,0)
        self.rot_img = pygame.transform.rotate(self.img,0)
    
    # This function rotates the projectile in the direction of the player

    def rotate_towards_player(self, player:Player2):
        angle = 360-math.atan2(player.player_rectangle.y-300,player.player_rectangle.x-400)*180/math.pi
        self.rot_img = pygame.transform.rotate(self.img,angle)
        self.projectile_rectangle=self.rot_img.get_rect(center=(self.projectile_rectangle.x, self.projectile_rectangle.y))

    # This function renders the projectile on th escreen at its current coordinates

    def render(self, x:float, y:float, screen:pygame.display):
        
        self.projectile_rectangle.x = x
        self.projectile_rectangle.y = y
        screen.blit(self.rot_img, self.projectile_rectangle)


    