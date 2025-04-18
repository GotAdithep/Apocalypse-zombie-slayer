import pygame

class Zombie:
    def __init__(self, x, y, game):
        self.rect = pygame.Rect(x, y, 40, 40)
        self.speed = 3          # Normal zombie speed.
        self.health = 150
        self.max_health = 150
        self.game = game
        self.facing_right = True

    def move_towards(self, player):
        self.facing_right = player.rect.x >= self.rect.x
        if self.rect.x < player.rect.x:
            self.rect.x += self.speed
        elif self.rect.x > player.rect.x:
            self.rect.x -= self.speed

        if self.rect.y < player.rect.y:
            self.rect.y += self.speed
        elif self.rect.y > player.rect.y:
            self.rect.y -= self.speed

        if self.rect.colliderect(player.rect):
            player.health -= 0.3

        self.rect.x = max(0, min(self.rect.x, self.game.WORLD_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.game.WORLD_HEIGHT - self.rect.height))

    def draw_health_bar(self, screen, camera_x, camera_y):
        health_bar_width = 40
        health_ratio = self.health / self.max_health
        pygame.draw.rect(
            screen, self.game.RED, 
            (self.rect.x - camera_x, self.rect.y - 10 - camera_y, health_bar_width, 5)
        )
        pygame.draw.rect(
            screen, self.game.GREEN, 
            (self.rect.x - camera_x, self.rect.y - 10 - camera_y, int(health_bar_width * health_ratio), 5)
        )

    def draw(self, screen, camera_x, camera_y):
        image_to_draw = self.game.zombie_img
        if not self.facing_right:
            image_to_draw = pygame.transform.flip(self.game.zombie_img, True, False)
        screen.blit(image_to_draw, (self.rect.x - camera_x, self.rect.y - camera_y))
        self.draw_health_bar(screen, camera_x, camera_y)

class SpeedyZombie(Zombie):
    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        self.speed = 5
        self.health = 75
        self.max_health = 75

    def draw(self, screen, camera_x, camera_y):
        image_to_draw = self.game.speedy_zombie_img
        if not self.facing_right:
            image_to_draw = pygame.transform.flip(self.game.speedy_zombie_img, True, False)
        screen.blit(image_to_draw, (self.rect.x - camera_x, self.rect.y - camera_y))
        self.draw_health_bar(screen, camera_x, camera_y)

class TankyZombie(Zombie):
    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        self.speed = 2
        self.health = 500
        self.max_health = 500

    def draw(self, screen, camera_x, camera_y):
        image_to_draw = self.game.tanky_zombie_img
        if not self.facing_right:
            image_to_draw = pygame.transform.flip(self.game.tanky_zombie_img, True, False)
        screen.blit(image_to_draw, (self.rect.x - camera_x, self.rect.y - camera_y))
        self.draw_health_bar(screen, camera_x, camera_y)

class SpitterZombie(Zombie):
    def __init__(self, x, y, game):
        super().__init__(x, y, game)
        self.health = 100
        self.max_health = 100
        self.speed = 3
        self.attack_cooldown = 2000
        self.last_attack_time = 0
        self.attack_range = 400
        self.image = self.game.splitter_img

    def move_towards(self, player):
        current_time = pygame.time.get_ticks()
        dx = player.rect.x - self.rect.x
        dy = player.rect.y - self.rect.y
        distance = (dx**2 + dy**2) ** 0.5

        self.facing_right = player.rect.x >= self.rect.x

        if distance < self.attack_range:
            move_speed = self.speed * 0.5
            if distance != 0:
                self.rect.x += int(move_speed * (dx / distance))
                self.rect.y += int(move_speed * (dy / distance))
        else:
            if self.rect.x < player.rect.x:
                self.rect.x += self.speed
            elif self.rect.x > player.rect.x:
                self.rect.x -= self.speed

            if self.rect.y < player.rect.y:
                self.rect.y += self.speed
            elif self.rect.y > player.rect.y:
                self.rect.y -= self.speed

        self.rect.x = max(0, min(self.rect.x, self.game.WORLD_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.game.WORLD_HEIGHT - self.rect.height))

        if distance < self.attack_range and current_time - self.last_attack_time >= self.attack_cooldown:
            self.shoot_projectile(player)
            self.last_attack_time = current_time

    def shoot_projectile(self, player):
        projectile = Projectile(
            self.rect.centerx, self.rect.centery,
            (player.rect.centerx, player.rect.centery), self.game
        )
        self.game.projectiles.append(projectile)

    def draw(self, screen, camera_x, camera_y):
        image_to_draw = self.image
        if not self.facing_right:
            image_to_draw = pygame.transform.flip(self.image, True, False)
        screen.blit(image_to_draw, (self.rect.x - camera_x, self.rect.y - camera_y))
        self.draw_health_bar(screen, camera_x, camera_y)

class Projectile:
    def __init__(self, x, y, target, game):
        self.game = game
        self.x = x
        self.y = y
        self.target = target
        self.speed = 7
        dx = target[0] - x
        dy = target[1] - y
        distance = (dx**2 + dy**2) ** 0.5
        if distance == 0:
            distance = 1
        self.dx = dx / distance
        self.dy = dy / distance
        self.rect = pygame.Rect(x, y, 10, 10)

    def update(self):
        self.x += self.dx * self.speed
        self.y += self.dy * self.speed
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)

    def draw(self, screen, camera_x, camera_y):
        if not hasattr(Projectile, "bullet_img"):
            Projectile.bullet_img = pygame.image.load("bullet.png")
            Projectile.bullet_img = pygame.transform.scale(Projectile.bullet_img, (30, 30))
        screen.blit(Projectile.bullet_img, (self.rect.x - camera_x, self.rect.y - camera_y))
