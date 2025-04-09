import pygame
from entity import SpeedyZombie, TankyZombie

class Player:
    def __init__(self, x, y, game):
        self.rect = pygame.Rect(x, y, 60, 60)
        self.health = 200
        self.facing_right = True
        self.game = game
        self.weapon = Weapon(self)

        self.damage_multiplier = 1.0
        self.speed_multiplier = 1.0
        self.damage_buff_end_time = 0
        self.speed_buff_end_time = 0

        self.level = 1
        self.exp = 0
        self.total_exp = 0
        self.next_level_exp = 10
        self.enhance_points = 0

        self.attack_buff_usage_count = 0
        self.speed_buff_usage_count = 0

    def move(self, keys):
        base_speed = 8
        effective_speed = int(
            base_speed * (1.5 if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) else 1.0) * self.speed_multiplier
        )
        if keys[pygame.K_a]:
            self.rect.x -= effective_speed
            self.facing_right = False
        if keys[pygame.K_d]:
            self.rect.x += effective_speed
            self.facing_right = True
        if keys[pygame.K_w]:
            self.rect.y -= effective_speed
        if keys[pygame.K_s]:
            self.rect.y += effective_speed
        self.rect.x = max(0, min(self.rect.x, self.game.WORLD_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.game.WORLD_HEIGHT - self.rect.height))

    def add_exp(self, amount):
        self.total_exp += amount
        self.exp += amount
        while self.exp >= self.next_level_exp:
            self.exp -= self.next_level_exp
            self.level += 1
            self.enhance_points += 1
            self.next_level_exp = int(self.next_level_exp * 1.2)

    def draw(self, screen, camera_x, camera_y):
        sprite = (
            self.game.player_img
            if self.facing_right
            else pygame.transform.flip(self.game.player_img, True, False)
        )
        screen.blit(sprite, (self.rect.x - camera_x, self.rect.y - camera_y))
        self.weapon.draw(screen, camera_x, camera_y)

        pygame.draw.rect(screen, self.game.RED, (20, 20, 200, 20))
        pygame.draw.rect(screen, self.game.GREEN, (20, 20, max(0, 2 * self.health), 20))

class Weapon:
    def __init__(self, owner):
        self.owner = owner
        self.damage = 50
        self.swinging = False
        self.swing_timer = 0
        self.swing_duration = 200
        self.hit_zombies = set()
        self.size_multiplier = 1.0
        self.base_upgrade_applied = False
        self.stackable_upgrade_applied = False

    def swing(self):
        if not self.swinging:
            self.swinging = True
            self.swing_timer = pygame.time.get_ticks()
            self.hit_zombies.clear()

    def update(self, zombies, loot_drops, game):
        if self.swinging:
            elapsed = pygame.time.get_ticks() - self.swing_timer
            if elapsed > self.swing_duration:
                self.swinging = False
            else:
                offset = 30 if self.owner.facing_right else -40
                offset = int(offset * self.size_multiplier)
                hitbox_width = int(60 * self.size_multiplier)
                hitbox_height = int(60 * self.size_multiplier)
                weapon_hitbox = pygame.Rect(
                    self.owner.rect.x + offset,
                    self.owner.rect.y + 10,
                    hitbox_width, hitbox_height
                )
                for z in zombies[:]:
                    if z not in self.hit_zombies and weapon_hitbox.colliderect(z.rect):
                        z.health -= self.damage * self.owner.damage_multiplier
                        self.hit_zombies.add(z)
                        if z.health <= 0:
                            loot_drops.drop_health_box(z.rect.x, z.rect.y)
                            zombies.remove(z)
                            game.zombies_killed += 1

                            if hasattr(z, "speed") and z.speed == 5:  # SpeedyZombie.
                                game.coin_count += 30
                                self.owner.add_exp(3)
                            elif hasattr(z, "speed") and z.speed == 2:  # TankyZombie.
                                game.coin_count += 1000
                                self.owner.add_exp(10)
                            elif hasattr(z, "attack_range"):  # SpitterZombie.
                                game.coin_count += 120
                                self.owner.add_exp(8)
                            else:
                                game.coin_count += 100
                                self.owner.add_exp(1)

    def draw(self, screen, camera_x, camera_y):
        offset_x = 30 if self.owner.facing_right else -40
        sprite = (
            self.owner.game.bat_img
            if self.owner.facing_right
            else pygame.transform.flip(self.owner.game.bat_img, True, False)
        )
        scaled_sprite = pygame.transform.scale(
            sprite, 
            (int(sprite.get_width() * self.size_multiplier), int(sprite.get_height() * self.size_multiplier))
        )
        if self.swinging:
            elapsed = pygame.time.get_ticks() - self.swing_timer
            swing_progress = elapsed / self.swing_duration
            angle = 90 * swing_progress if self.owner.facing_right else -90 * swing_progress
            rotated_sprite = pygame.transform.rotate(scaled_sprite, angle)
            swing_pos = (
                self.owner.rect.x + int(offset_x * self.size_multiplier) - camera_x,
                self.owner.rect.y - camera_y
            )
            screen.blit(rotated_sprite, swing_pos)
        else:
            screen.blit(
                scaled_sprite,
                (self.owner.rect.x + int(offset_x * self.size_multiplier) - camera_x, self.owner.rect.y - camera_y)
            )
