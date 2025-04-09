import pygame
import random
from entity import Zombie, SpeedyZombie, TankyZombie, SpitterZombie, Projectile
from player import Player

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen.get_width(), screen.get_height()
        self.WORLD_WIDTH, self.WORLD_HEIGHT = 1600, 1200

        self.background = pygame.image.load("pixel-background.jpg")
        self.background = pygame.transform.scale(self.background, (self.WORLD_WIDTH, self.WORLD_HEIGHT))
        self.player_img = pygame.image.load("amounguspng.png")
        self.player_img = pygame.transform.scale(self.player_img, (60, 60))
        self.zombie_img = pygame.image.load("zombie.webp")
        self.zombie_img = pygame.transform.scale(self.zombie_img, (40, 40))
        self.speedy_zombie_img = pygame.image.load("speedy_zombie.png")
        self.speedy_zombie_img = pygame.transform.scale(self.speedy_zombie_img, (40, 40))
        self.tanky_zombie_img = pygame.image.load("TankZombert.webp")
        self.tanky_zombie_img = pygame.transform.scale(self.tanky_zombie_img, (50, 50))
        self.bat_img = pygame.image.load("bat_new1.png")
        self.bat_img = pygame.transform.scale(self.bat_img, (60, 30))
        self.health_box_img = pygame.image.load("health_box.png")
        self.health_box_img = pygame.transform.scale(self.health_box_img, (50, 50))
        
        self.attack_buff_img = pygame.image.load("attack_buff.png")
        self.attack_buff_img = pygame.transform.scale(self.attack_buff_img, (50, 50))
        self.speed_buff_img = pygame.image.load("speed_buff.webp")
        self.speed_buff_img = pygame.transform.scale(self.speed_buff_img, (50, 50))
        
        self.splitter_img = pygame.image.load("splitter.webp")
        self.splitter_img = pygame.transform.scale(self.splitter_img, (40, 40))

        self.RED, self.GREEN, self.WHITE = (255, 0, 0), (0, 255, 0), (255, 255, 255)
        self.big_font = pygame.font.Font(None, 100)
        self.small_font = pygame.font.Font(None, 36)

        self.player = Player(400, 300, self)
        self.zombies = []
        self.loot_drops = LootDrops(self)
        self.projectiles = []
        self.zombie_spawn_timer = 0
        self.game_over = False

        self.zombies_killed = 0
        self.coin_count = 0
        self.loot_pickup_count = 0


        self.spawn_interval = 60
        self.current_level = 0

    def update(self):
        if not self.game_over:
            keys = pygame.key.get_pressed()
            self.player.move(keys)
            for z in self.zombies:
                z.move_towards(self.player)
            self.player.weapon.update(self.zombies, self.loot_drops, self)
            self.loot_drops.check_pickup(self.player)

            for projectile in self.projectiles[:]:
                projectile.update()
                if projectile.rect.colliderect(self.player.rect):
                    self.player.health -= 20
                    self.projectiles.remove(projectile)
                elif (projectile.x < 0 or projectile.x > self.WORLD_WIDTH or
                      projectile.y < 0 or projectile.y > self.WORLD_HEIGHT):
                    self.projectiles.remove(projectile)

            self.zombie_spawn_timer += 1
            if self.zombie_spawn_timer >= self.spawn_interval:
                r = random.random()
                if r < 0.55:
                    self.zombies.append(Zombie(
                        random.randint(0, self.WORLD_WIDTH - 40),
                        random.randint(0, self.WORLD_HEIGHT - 40),
                        self
                    ))
                elif r < 0.70:
                    self.zombies.append(SpeedyZombie(
                        random.randint(0, self.WORLD_WIDTH - 40),
                        random.randint(0, self.WORLD_HEIGHT - 40),
                        self
                    ))
                elif r < 0.85:
                    self.zombies.append(SpitterZombie(
                        random.randint(0, self.WORLD_WIDTH - 40),
                        random.randint(0, self.WORLD_HEIGHT - 40),
                        self
                    ))
                else:
                    self.zombies.append(TankyZombie(
                        random.randint(0, self.WORLD_WIDTH - 40),
                        random.randint(0, self.WORLD_HEIGHT - 40),
                        self
                    ))
                self.zombie_spawn_timer = 0

            new_level = self.zombies_killed // 20
            if new_level > self.current_level:
                self.spawn_interval = max(20, self.spawn_interval - 5)
                self.current_level = new_level

            current_time = pygame.time.get_ticks()
            if current_time >= self.player.damage_buff_end_time:
                self.player.damage_multiplier = 1.0
            if current_time >= self.player.speed_buff_end_time:
                self.player.speed_multiplier = 1.0

        if self.player.health <= 0:
            self.game_over = True

    def draw(self):
        camera_x = self.player.rect.x - self.SCREEN_WIDTH // 2
        camera_y = self.player.rect.y - self.SCREEN_HEIGHT // 2
        camera_x = max(0, min(camera_x, self.WORLD_WIDTH - self.SCREEN_WIDTH))
        camera_y = max(0, min(camera_y, self.WORLD_HEIGHT - self.SCREEN_HEIGHT))
        
        self.screen.fill((0, 0, 0))
        self.screen.blit(self.background, (-camera_x, -camera_y))
        self.player.draw(self.screen, camera_x, camera_y)
        for z in self.zombies:
            z.draw(self.screen, camera_x, camera_y)
        self.loot_drops.draw(self.screen, camera_x, camera_y)
        for projectile in self.projectiles:
            projectile.draw(self.screen, camera_x, camera_y)

        zombie_count_text = self.small_font.render(f"Zombies: {len(self.zombies)}", True, self.WHITE)
        zombies_killed_text = self.small_font.render(f"Eliminated: {self.zombies_killed}", True, self.WHITE)
        coin_count_text = self.small_font.render(f"Coins: {self.coin_count}", True, self.WHITE)
        loot_pickup_text = self.small_font.render(f"Loot Pickups: {self.loot_pickup_count}", True, self.WHITE)
        self.screen.blit(zombie_count_text, (self.SCREEN_WIDTH - zombie_count_text.get_width() - 10, 10))
        self.screen.blit(zombies_killed_text, (self.SCREEN_WIDTH - zombies_killed_text.get_width() - 10, 40))
        self.screen.blit(coin_count_text, (self.SCREEN_WIDTH - coin_count_text.get_width() - 10, 70))
        self.screen.blit(loot_pickup_text, (self.SCREEN_WIDTH - loot_pickup_text.get_width() - 10, 100))

        exp_bar_width = 200
        exp_bar_height = 10
        exp_percentage = (self.player.exp / self.player.next_level_exp) if self.player.next_level_exp > 0 else 0
        pygame.draw.rect(self.screen, (100, 100, 100), (20, 45, exp_bar_width, exp_bar_height))
        pygame.draw.rect(self.screen, (50, 150, 255), (20, 45, int(exp_bar_width * exp_percentage), exp_bar_height))
        exp_text = self.small_font.render(f"LVL {self.player.level}", True, self.WHITE)
        self.screen.blit(exp_text, (20 + exp_bar_width + 10, 40))
        
        enhance_text = self.small_font.render(f"Enhance Points: {self.player.enhance_points}", True, self.WHITE)
        self.screen.blit(enhance_text, (self.SCREEN_WIDTH - enhance_text.get_width() - 10, 130))
        
        if self.game_over:
            game_over_text = self.big_font.render("Game Over", True, self.RED)
            restart_text = self.big_font.render("Press R to Restart", True, self.WHITE)
            self.screen.blit(game_over_text, (self.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                              self.SCREEN_HEIGHT // 2 - game_over_text.get_height()))
            self.screen.blit(restart_text, (self.SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                                            self.SCREEN_HEIGHT // 2 + 20))
        else:
            shop_instr = self.small_font.render("Press Tab to Open Shop", True, self.WHITE)
            self.screen.blit(shop_instr, (10, self.SCREEN_HEIGHT - shop_instr.get_height() - 10))
        
        current_time = pygame.time.get_ticks()
        buff_margin = 10
        x_attack = self.SCREEN_WIDTH - self.attack_buff_img.get_width() - buff_margin
        x_speed = self.SCREEN_WIDTH - self.speed_buff_img.get_width() - buff_margin

        if current_time < self.player.damage_buff_end_time:
            damage_time_left = (self.player.damage_buff_end_time - current_time) // 1000
            attack_text = self.small_font.render("Attack: " + str(damage_time_left) + "s", True, self.WHITE)
            y_attack = self.SCREEN_HEIGHT - self.attack_buff_img.get_height() - buff_margin
            self.screen.blit(self.attack_buff_img, (x_attack, y_attack))
            self.screen.blit(
                attack_text,
                (x_attack - attack_text.get_width() - 5,
                 y_attack + (self.attack_buff_img.get_height() - attack_text.get_height()) // 2)
            )

        if current_time < self.player.speed_buff_end_time:
            speed_time_left = (self.player.speed_buff_end_time - current_time) // 1000
            speed_text = self.small_font.render("Speed: " + str(speed_time_left) + "s", True, self.WHITE)
            if current_time < self.player.damage_buff_end_time:
                y_speed = self.SCREEN_HEIGHT - self.attack_buff_img.get_height() - self.speed_buff_img.get_height() - 2 * buff_margin
            else:
                y_speed = self.SCREEN_HEIGHT - self.speed_buff_img.get_height() - buff_margin
            self.screen.blit(self.speed_buff_img, (x_speed, y_speed))
            self.screen.blit(
                speed_text,
                (x_speed - speed_text.get_width() - 5,
                 y_speed + (self.speed_buff_img.get_height() - speed_text.get_height()) // 2)
            )

class LootDrops:
    def __init__(self, game):
        self.game = game
        self.drops = []

    def drop_health_box(self, x, y):
        if random.random() < 0.05:
            self.drops.append(pygame.Rect(x, y, 50, 50))

    def check_pickup(self, player):
        for box in self.drops[:]:
            if player.rect.colliderect(box):
                player.health = min(200, player.health + 30)
                self.drops.remove(box)
                self.game.loot_pickup_count += 1

    def draw(self, screen, camera_x, camera_y):
        for box in self.drops:
            screen.blit(self.game.health_box_img, (box.x - camera_x, box.y - camera_y))
