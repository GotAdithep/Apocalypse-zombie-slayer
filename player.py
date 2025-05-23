import pygame
from entity import SpeedyZombie, TankyZombie  # Import other zombie types as needed

class Player:
    def __init__(self, x, y, game):
        self.rect = pygame.Rect(x, y, 60, 60)
        self.health = 200
        self.game = game
        self.weapon = Weapon(self)

        self.speed_multiplier = 1.0
        self.damage_multiplier = 1.0
        self.damage_buff_end_time = 0
        self.speed_buff_end_time = 0

        self.level = 1
        self.exp = 0
        self.next_level_exp = 10
        self.enhance_points = 0

        self.attack_buff_usage_count = 0
        self.speed_buff_usage_count = 0

        self.moving = False

        self.spritesheet = pygame.image.load("pictures/pokemon_sprite.png").convert_alpha()
        self.sprite_size = 64
        self.animations = {
            "down": [self.get_sprite(0, i) for i in range(4)],
            "left": [self.get_sprite(1, i) for i in range(4)],
            "right": [self.get_sprite(2, i) for i in range(4)],
            "up": [self.get_sprite(3, i) for i in range(4)],
        }
        self.current_animation = "down"
        self.animation_frame = 0
        self.animation_timer = pygame.time.get_ticks()

        self.earthquake_unlocked = False
        self.earthquake_cooldown_end = 0
        self.earthquake_active = False
        self.earthquake_effect_start_time = 0

    def get_sprite(self, row, col):
        x, y = col * self.sprite_size, row * self.sprite_size
        return self.spritesheet.subsurface((x, y, self.sprite_size, self.sprite_size))

    def move(self, keys):
        moved = False
        base_speed = 8
        sprint_factor = 1.5 if (keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT]) else 1.0
        effective_speed = int(base_speed * sprint_factor * self.speed_multiplier)

        if keys[pygame.K_w]:
            self.rect.y -= effective_speed
            self.current_animation = "up"
            moved = True
        if keys[pygame.K_s]:
            self.rect.y += effective_speed
            self.current_animation = "down"
            moved = True
        if keys[pygame.K_a]:
            self.rect.x -= effective_speed
            self.current_animation = "left"
            moved = True
        if keys[pygame.K_d]:
            self.rect.x += effective_speed
            self.current_animation = "right"
            moved = True

        self.rect.x = max(0, min(self.rect.x, self.game.WORLD_WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, self.game.WORLD_HEIGHT - self.rect.height))

        self.moving = moved

    def add_exp(self, amount):
        self.exp += amount
        while self.exp >= self.next_level_exp:
            self.exp -= self.next_level_exp
            self.level += 1
            self.enhance_points += 1
            self.next_level_exp = int(self.next_level_exp * 1.4)

    def draw(self, screen, camera_x, camera_y):
        now = pygame.time.get_ticks()
        if self.moving:
            if now - self.animation_timer > 150:
                self.animation_frame = (self.animation_frame + 1) % len(self.animations[self.current_animation])
                self.animation_timer = now
        else:
            self.animation_frame = 0

        sprite = self.animations[self.current_animation][self.animation_frame]
        screen.blit(sprite, (self.rect.x - camera_x, self.rect.y - camera_y))
        self.weapon.draw(screen, camera_x, camera_y)

        pygame.draw.rect(screen, self.game.RED, (20, 20, 200, 20))
        pygame.draw.rect(screen, self.game.GREEN, (20, 20, max(0, 2 * self.health), 20))

        if self.earthquake_active:
            current_time = pygame.time.get_ticks()
            elapsed = current_time - self.earthquake_effect_start_time
            duration = 3000
            if elapsed > duration:
                self.earthquake_active = False
            else:
                fade_ratio = 1 - (elapsed / duration)
                earthquake_img = pygame.image.load("images/earthquake.png").convert_alpha()
                earthquake_img = pygame.transform.scale(earthquake_img, (200, 200))
                earthquake_img.set_alpha(int(255 * fade_ratio))
                pos = (self.rect.centerx - 100 - camera_x, self.rect.centery - 100 - camera_y)
                screen.blit(earthquake_img, pos)

    def activate_earthquake(self, game):
        current_time = pygame.time.get_ticks()
        if self.earthquake_unlocked and current_time >= self.earthquake_cooldown_end:
            self.earthquake_cooldown_end = current_time + 10000
            self.earthquake_active = True
            self.earthquake_effect_start_time = current_time
            radius = 300
            for zombie in game.zombies[:]:
                dx = self.rect.centerx - zombie.rect.centerx
                dy = self.rect.centery - zombie.rect.centery
                distance = (dx * dx + dy * dy) ** 0.5
                if distance <= radius:
                    zombie.health -= 150
                    if zombie.health <= 0:
                        game.zombies.remove(zombie)
                        game.zombies_killed += 1
        else:
            print("Earthquake on cooldown or not unlocked.")

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
                direction = self.owner.current_animation
                size_mult = self.size_multiplier
                if direction == "right":
                    offset = (30 * size_mult, 0)
                elif direction == "left":
                    offset = (-40 * size_mult, 0)
                elif direction == "up":
                    offset = (0, -40 * size_mult)
                elif direction == "down":
                    offset = (0, 30 * size_mult)
                else:
                    offset = (30 * size_mult, 0)

                hitbox_width = int(60 * size_mult)
                hitbox_height = int(60 * size_mult)
                weapon_hitbox = pygame.Rect(
                    self.owner.rect.x + int(offset[0]),
                    self.owner.rect.y + int(offset[1]),
                    hitbox_width,
                    hitbox_height
                )
                for z in zombies[:]:
                    if z not in self.hit_zombies and weapon_hitbox.colliderect(z.rect):
                        z.health -= self.damage * self.owner.damage_multiplier
                        self.hit_zombies.add(z)
                        if z.health <= 0:
                            loot_drops.drop_health_box(z.rect.x, z.rect.y)
                            zombies.remove(z)
                            game.zombies_killed += 1
                            self.owner.game.database.register_zombie_kill(z.__class__.__name__)
                            if hasattr(z, "is_king") and z.is_king:
                                game.coin_count += 1500
                                self.owner.add_exp(20)
                            elif hasattr(z, "speed") and z.speed == 5:
                                game.coin_count += 150
                                self.owner.add_exp(5)
                            elif hasattr(z, "speed") and z.speed == 2:
                                game.coin_count += 500
                                self.owner.add_exp(10)
                            elif hasattr(z, "attack_range"):
                                game.coin_count += 200
                                self.owner.add_exp(8)
                            else:
                                game.coin_count += 100
                                self.owner.add_exp(3)

    def draw(self, screen, camera_x, camera_y):
        direction = self.owner.current_animation
        size_mult = self.size_multiplier
        vertical_adjustment = 15

        if direction == "right":
            offset = (30 * size_mult, 0)
            flip = False
            swing_factor = 90
        elif direction == "left":
            offset = (-40 * size_mult, 0)
            flip = True
            swing_factor = -90
        elif direction == "up":
            offset = (0, -40 * size_mult)
            flip = False
            swing_factor = -90
        elif direction == "down":
            offset = (0, 30 * size_mult)
            flip = False
            swing_factor = 90
        else:
            offset = (30 * size_mult, 0)
            flip = False
            swing_factor = 90

        sprite = self.owner.game.bat_img
        if flip:
            sprite = pygame.transform.flip(sprite, True, False)
        scaled_sprite = pygame.transform.scale(sprite,
                                               (int(sprite.get_width() * size_mult),
                                                int(sprite.get_height() * size_mult)))
        if self.swinging:
            elapsed = pygame.time.get_ticks() - self.swing_timer
            swing_progress = elapsed / self.swing_duration
            angle = swing_factor * swing_progress
            rotated_sprite = pygame.transform.rotate(scaled_sprite, angle)
            swing_pos = (
                self.owner.rect.x + int(offset[0]) - camera_x,
                self.owner.rect.y + int(offset[1]) + vertical_adjustment - camera_y
            )
            screen.blit(rotated_sprite, swing_pos)
        else:
            pos = (
                self.owner.rect.x + int(offset[0]) - camera_x,
                self.owner.rect.y + int(offset[1]) + vertical_adjustment - camera_y
            )
            screen.blit(scaled_sprite, pos)