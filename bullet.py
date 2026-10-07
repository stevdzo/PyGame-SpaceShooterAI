import pygame
import math
from gameObject import GameObject


class Bullet(GameObject):
    def __init__(self, x, y, angle, speed=600, size=6):
        super().__init__("Bullet", x, y, size, size, sprite=None)

        self.angle = angle
        self.speed = speed
        self.damage = 20

        self.vel = pygame.Vector2(math.cos(angle), math.sin(angle)) * self.speed

    def update(self, dt):
        self.pos += self.vel * dt

    def draw(self, surface):
        pygame.draw.circle(surface, (255, 255, 0), (int(self.pos.x), int(self.pos.y)), int(self.size.x / 2))

    def get_damage(self):
        return self.damage
