import pygame


class GameObject:
    def __init__(self, name="unnamed", x=0, y=0, w=30, h=30, sprite=None):
        self.name = name
        self.pos = pygame.Vector2(x, y)
        self.size = pygame.Vector2(w, h)
        self.angle = 0
        self.sprite = sprite
        self.radius = (w+h)/4
        self.alive = True

    def update(self, dt):
        pass

    def draw(self, surface):
        if self.sprite:
            self.sprite.draw(surface, self.pos, self.size, self.angle)
        else:
            pygame.draw.circle(surface, (255, 255, 0), (int(self.pos.x), int(self.pos.y)), int(self.size.x / 2))

    def clamp_to_screen(self, width, height):
        pass

    def is_colliding(self, other):
        distance = (self.pos - other.pos).length()
        return distance < (self.radius + other.radius)
