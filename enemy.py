import math
import random
import pygame
import globals
from enemyState import State
from gameObject import GameObject


class Enemy(GameObject):
    def __init__(self, name, x, y, w, h, sprite, target, heal_target):
        super().__init__(name, x, y, w, h, sprite=sprite)
        self.target = target
        self.heal_target = heal_target
        self.health = 100.0
        self.pursue_radius = 500
        self.flee_radius = 200
        self.slow_radius = 60
        self.max_speed = 100
        self.max_force = 200
        self.state = State.WANDER
        self.wander_dir = pygame.Vector2(1, 0)
        self.wander_timer = 0
        self.flee_timer = 0
        self.flee_timer_threshold = 2
        self.vel = pygame.Vector2(0, 0)
        self.acc = pygame.Vector2(0, 0)
        self.fov_angle = math.radians(90)
        self.STOP_RADIUS = 25

    def update(self, dt):
        self.clamp_to_screen(globals.WIDTH, globals.HEIGHT)
        if self.state == State.WANDER:
            self.update_wander(dt)

        elif self.state == State.PURSUE:
            self.update_pursue(dt)

        elif self.state == State.FLEE:
            self.update_flee(dt)

        elif self.state == State.ARRIVE:
            self.update_arrive(dt)

        self.vel += self.acc * dt

        if self.vel.length() > self.max_speed:
            self.vel = self.vel.normalize() * self.max_speed

        self.pos += self.vel * dt

        if self.vel.length() > 0:
            self.angle = math.atan2(self.vel.y, self.vel.x)

        self.acc *= 0

    def update_wander(self, dt):

        self.wander_timer -= dt

        if self.wander_timer <= 0:
            self.wander_timer = random.uniform(0.7, 1.2)
            angle = random.uniform(0, 2 * math.pi)
            self.wander_dir = pygame.Vector2(math.cos(angle), math.sin(angle))

        if self.health < 50:
            self.max_speed = 250
            self.max_force = 600
            self.state = State.ARRIVE
            return

        to_target = self.target.pos - self.pos
        distance = to_target.length()

        if distance < self.pursue_radius and self.has_line_of_sight():
            self.max_speed = 350
            self.max_force = 900
            self.state = State.PURSUE
            return

        self.vel += self.wander_dir * self.max_force * dt

    def update_pursue(self, dt):
        to_target = self.target.pos - self.pos
        distance = to_target.length()

        if distance > self.pursue_radius or not self.has_line_of_sight():
            self.max_speed = 100
            self.max_force = 200
            self.state = State.WANDER
            return

        if self.health < 50:
            self.max_speed = 250
            self.max_force = 600
            self.state = State.ARRIVE
            return

        if distance < self.flee_radius:
            self.max_speed = 250
            self.max_force = 600
            self.flee_timer = self.flee_timer_threshold
            self.state = State.FLEE
            return

        if distance < self.STOP_RADIUS:
            self.vel *= 0
            return

        force = self.seek(self.target.pos)
        self.apply_force(force)

    def seek(self, target):
        desired = target - self.pos
        distance = desired.length()

        if distance == 0:
            return pygame.Vector2(0, 0)

        desired = desired.normalize()

        if distance < self.slow_radius:
            desired *= self.max_speed * (distance / self.slow_radius)
        else:
            desired *= self.max_speed

        steer = desired - self.vel

        if steer.length() > self.max_force:
            steer = steer.normalize() * self.max_force

        return steer

    def update_flee(self, dt):
        self.flee_timer -= dt
        to_target = self.target.pos - self.pos
        distance = to_target.length()

        if self.health < 50:
            self.max_speed = 250
            self.max_force = 600
            self.state = State.ARRIVE
            return

        if distance > self.pursue_radius and self.flee_timer <= 0:
            self.flee_timer = 0
            self.max_speed = 100
            self.max_force = 200
            self.state = State.WANDER
            return

        force = self.flee(self.target.pos)
        self.apply_force(force)

    def flee(self, target):
        desired = self.pos - target

        if desired.length() == 0:
            return pygame.Vector2(0, 0)

        desired = desired.normalize() * self.max_speed
        steer = desired - self.vel

        if steer.length() > self.max_force:
            steer = steer.normalize() * self.max_force

        return steer

    def update_arrive(self, dt):
        if not self.heal_target:
            return

        to_station = self.heal_target.pos - self.pos
        distance = to_station.length()

        if distance > 30:
            force = self.arrive(self.heal_target.pos)
            self.apply_force(force)
        else:
            self.vel *= 0.8
            self.health += 10 * dt

            if self.health >= 100:
                self.health = 100
                self.max_speed = 100
                self.max_force = 200
                self.state = State.WANDER

    def arrive(self, target):
        desired = target - self.pos
        distance = desired.length()

        if distance == 0:
            return pygame.Vector2(0, 0)

        desired = desired.normalize()

        if distance < self.slow_radius:
            speed = self.max_speed * (distance / self.slow_radius)
        else:
            speed = self.max_speed

        desired *= speed

        steer = desired - self.vel

        if steer.length() > self.max_force:
            steer = steer.normalize() * self.max_force

        return steer

    def apply_force(self, force):
        self.acc += force

    def draw(self, surface):
        super().draw(surface)

        self.draw_health_bar(surface)

        if globals.SHOW_DEBUG:
            self.show_wireframe(surface)

        text_surface = globals.FONT.render(f"{self.name} - {self.state.name}", True, (255, 255, 255))

        rect = text_surface.get_rect(center=(self.pos.x, self.pos.y - self.size.y / 2 - 30))

        surface.blit(text_surface, rect)

    def show_wireframe(self, surface):
        pygame.draw.line(surface, (255, 0, 0), self.pos, self.pos + self.vel, 2)
        pygame.draw.line(surface, (0, 255, 0), self.pos, self.pos + self.wander_dir * 50, 2)
        pygame.draw.circle(surface, (0, 0, 255), (int(self.pos.x), int(self.pos.y)), int(self.pursue_radius), 1)
        pygame.draw.circle(surface, (0, 255, 255), (int(self.pos.x), int(self.pos.y)), int(self.flee_radius), 1)

        left_angle = self.angle - self.fov_angle / 2
        right_angle = self.angle + self.fov_angle / 2

        left_dir = pygame.Vector2(math.cos(left_angle), math.sin(left_angle))
        right_dir = pygame.Vector2(math.cos(right_angle), math.sin(right_angle))

        left_end = self.pos + left_dir * self.pursue_radius
        right_end = self.pos + right_dir * self.pursue_radius

        pygame.draw.line(surface, (255, 255, 0), self.pos, left_end, 1)
        pygame.draw.line(surface, (255, 255, 0), self.pos, right_end, 1)

        rect = pygame.Rect(self.pos.x - self.size.x / 2, self.pos.y - self.size.y / 2, self.size.x, self.size.y)

        pygame.draw.rect(surface, (255, 255, 255), rect, 1)

    def get_name(self):
        return self.name

    def clamp_to_screen(self, width, height):
        half_w = self.size.x / 2
        half_h = self.size.y / 2

        if self.pos.x < half_w:
            self.pos.x = half_w
            if self.vel.x < 0:
                self.vel.x = 0
            self.wander_dir.x = abs(self.wander_dir.x)

        elif self.pos.x > width - half_w:
            self.pos.x = width - half_w
            if self.vel.x > 0:
                self.vel.x = 0
            self.wander_dir.x = -abs(self.wander_dir.x)

        if self.pos.y < half_h:
            self.pos.y = half_h
            if self.vel.y < 0:
                self.vel.y = 0
            self.wander_dir.y = abs(self.wander_dir.y)

        elif self.pos.y > height - half_h:
            self.pos.y = height - half_h
            if self.vel.y > 0:
                self.vel.y = 0
            self.wander_dir.y = -abs(self.wander_dir.y)

    def set_target(self, target):
        self.target = target

    def draw_health_bar(self, surface):
        bar_width = int(self.size.x)
        bar_height = 5

        x = int(self.pos.x - bar_width / 2)
        y = int(self.pos.y - self.size.y / 2 - 15)

        pygame.draw.rect(surface, (255, 0, 0), (x, y, bar_width, bar_height))

        ratio = max(0, self.health / 100)

        pygame.draw.rect(surface, (0, 255, 0), (x, y, int(bar_width * ratio), bar_height))

    def update_health(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.alive = False

    def has_line_of_sight(self):
        to_target = self.target.pos - self.pos
        distance = to_target.length()

        if distance == 0:
            return True

        to_target = to_target.normalize()

        forward = pygame.Vector2(math.cos(self.angle), math.sin(self.angle))

        dot = forward.dot(to_target)

        threshold = math.cos(self.fov_angle / 2)

        return dot > threshold
