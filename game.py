import pygame
import globals
from bullet import Bullet
from gameObject import GameObject
from path import resource_path
from sprite import Sprite
from player import Player
from enemy import Enemy


class Game:
    def __init__(self):
        self.objects = []
        self.bullets = []

        self.background = pygame.image.load(resource_path("assets/background.png"))
        self.background = pygame.transform.scale(self.background, (globals.WIDTH, globals.HEIGHT))

        self.charger = GameObject("Charger", 300, globals.HEIGHT - 25, 50, 50, Sprite(resource_path("assets/charger.png")))
        self.objects.append(self.charger)

        self.player = Player(name="Player", x=globals.WIDTH // 2, y=globals.HEIGHT // 2, w=64, h=64, sprite=Sprite(
            resource_path("assets/player.png")))
        self.objects.append(self.player)
        self.objects.append(Enemy(name="Enemy 1", x=300, y=300, w=50, h=50, sprite=Sprite(resource_path("assets/enemy1.png")), target=self.player, heal_target=self.charger))
        self.objects.append(Enemy(name="Enemy 2", x=900, y=900, w=50, h=50, sprite=Sprite(resource_path("assets/enemy2.png")), target=self.player, heal_target=self.charger))

    def update(self, dt):
        for obj in self.objects:
            obj.update(dt)

        shot = self.player.shoot()
        if shot:
            bullet = Bullet(shot["pos"].x, shot["pos"].y, shot["angle"])
            self.bullets.append(bullet)

        for bullet in self.bullets:
            bullet.update(dt)

        for bullet in self.bullets:
            for obj in self.objects:
                if obj is self.player:
                    continue
                if bullet.is_colliding(obj):
                    bullet.alive = False
                    if isinstance(obj, Enemy):
                        obj.update_health(bullet.get_damage())

        self.objects = [o for o in self.objects if o.alive]

        self.bullets = [
            b for b in self.bullets
            if b.alive and 0 < b.pos.x < globals.WIDTH and 0 < b.pos.y < globals.HEIGHT
        ]

    def draw(self, surface):
        surface.blit(self.background, (0, 0))

        globals.CONTROLS_OFFSET_Y = 0
        for control in globals.CONTROLS:
            text = globals.FONT.render(control, True, (200, 200, 200))
            surface.blit(text, (10, globals.CONTROLS_OFFSET_Y))
            globals.CONTROLS_OFFSET_Y += 20

        for bullet in self.bullets:
            bullet.draw(surface)

        for obj in self.objects:
            obj.draw(surface)

