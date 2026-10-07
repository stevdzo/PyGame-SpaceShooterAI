import pygame
import math


class Sprite:
    def __init__(self, image_path):
        self.original = pygame.image.load(image_path).convert_alpha()

    def draw(self, surface, position, size, angle):
        scaled = pygame.transform.scale(self.original, (int(size.x), int(size.y)))
        rotated = pygame.transform.rotate(scaled, -math.degrees(angle))
        rect = rotated.get_rect(center=(position.x, position.y))

        surface.blit(rotated, rect)
