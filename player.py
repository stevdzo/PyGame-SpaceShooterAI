import globals
from gameObject import GameObject
import pygame
import math


class Player(GameObject):
    def __init__(self, name, x, y, w, h, sprite):
        super().__init__(name, x, y, w, h, sprite=sprite)
        self.speed = 400
        self.STOP_RADIUS = 10
        self.shoot_cooldown = 0.2
        self.shoot_timer = 0

    def update(self, dt):
        self.clamp_to_screen(globals.WIDTH, globals.HEIGHT)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_pos = pygame.Vector2(mouse_x, mouse_y)

        self.shoot_timer -= dt

        to_mouse = mouse_pos - self.pos
        distance = to_mouse.length()

        if distance > self.STOP_RADIUS:
            self.angle = math.atan2(to_mouse.y, to_mouse.x)

        keys = pygame.key.get_pressed()

        forward = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))
        # right = pygame.Vector2(-forward.y, forward.x)

        velocity = pygame.Vector2(0, 0)

        if keys[pygame.K_w]:
            velocity += forward
        if keys[pygame.K_s]:
            velocity -= forward
        # if keys[pygame.K_a]:
        #     velocity -= right
        # if keys[pygame.K_d]:
        #     velocity += right

        if velocity.length() > 0:
            velocity = velocity.normalize()

        if distance > self.STOP_RADIUS:
            self.pos += velocity * self.speed * dt

    def draw(self, surface):
        super().draw(surface)

    def get_name(self):
        return self.name

    def clamp_to_screen(self, width, height):
        self.pos.x = max(self.radius, min(width - self.radius, self.pos.x))
        self.pos.y = max(self.radius, min(height - self.radius, self.pos.y))

    def shoot(self):
        mouse_buttons = pygame.mouse.get_pressed()

        if mouse_buttons[0] and self.shoot_timer <= 0:
            self.shoot_timer = self.shoot_cooldown

            forward = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))
            spawn_pos = self.pos + forward * (self.size.x / 2)

            return {
                "pos": spawn_pos,
                "angle": self.angle
            }

        return None
