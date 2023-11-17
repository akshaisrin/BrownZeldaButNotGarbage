import pygame
import os
from Room import *
from Constants import *

class Biome(Room):
    
    def __init__(self, name:str, file_path:str):
        super().__init__(0, 0, 0)
        self.name = name
        self.file_path = file_path
        
    def render(self, screen:pygame.display):
        img = pygame.image.load(os.path.join("Assets/biomes", self.file_path))
        image = pygame.transform.scale(img, (screen_width, screen_height - 100))
        screen.blit(image, (0, -100))