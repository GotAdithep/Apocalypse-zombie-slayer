import pygame
import random
from entity import Zombie, SpeedyZombie, TankyZombie, SpitterZombie, KingZombie, Projectile
from player import Player
from database import Database

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.SCREEN_WIDTH, self.SCREEN_HEIGHT = screen.get_width(), screen.get_height()
        self.WORLD_WIDTH, self.WORLD_HEIGHT = 1600, 1200

        # Load Background Image
        self.background = pygame.image.load("pictures/pixel-background.jpg")
        self.background = pygame.transform.scale(self.background, (self.WORLD_WIDTH, self.WORLD_HEIGHT))

        # Load Player Image
        self.player_img = pygame.image.load("pictures/amounguspng.png")
        self.player_img = pygame.transform.scale(self.player_img, (60, 60))

        # Load Zombie Images
        self.zombie_img = pygame.image.load("pictures/zombie.webp")
        self.zombie_img = pygame.transform.scale(self.zombie_img, (40, 40))
        self.speedy_zombie_img = pygame.image.load("pictures/speedy_zombie.png")
        self.speedy_zombie_img = pygame.transform.scale(self.speedy_zombie_img, (40, 40))
        self.tanky_zombie_img = pygame.image.load("pictures/TankZombert.webp")
        self.tanky_zombie_img = pygame.transform.scale(self.tanky_zombie_img, (50, 50))
        self.splitter_img = pygame.image.load("pictures/splitter.webp")
        self.splitter_img = pygame.transform.scale(self.splitter_img, (40, 40))
        
        # Load King Zombie Image
        self.king_zombie_img = pygame.image.load("pictures/king_zombie.png")
        self.king_zombie_img = pygame.transform.scale(self.king_zombie_img, (60, 60))
        
        # Load Weapon Image
        self.bat_img = pygame.image.load("pictures/bat_new1.png")
        self.bat_img = pygame.transform.scale(self.bat_img, (60, 30))
        
        # Load Loot Drop and Buff Images
        self.health_box_img = pygame.image.load("pictures/health_box.png")
        self.health_box_img = pygame.transform.scale(self.health_box_img, (50, 50))
        self.attack_buff_img = pygame.image.load("pictures/attack_buff.png")
        self.attack_buff_img = pygame.transform.scale(self.attack_buff_img, (50, 50))
        self.speed_buff_img = pygame.image.load("pictures/speed_buff.webp")
        self.speed_buff_img = pygame.transform.scale(self.speed_buff_img, (50, 50))
        
        # UI and Skill Tree Icon
        self.skill_tree_icon = pygame.image.load("images/skill_tree.jpg")
        self.skill_tree_icon = pygame.transform.scale(self.skill_tree_icon, (80, 80))
        
        # Buff & Ability Icons
        self.earthquake_img = pygame.image.load("images/earthquake.png")
        self.earthquake_img = pygame.transform.scale(self.earthquake_img, (200, 200))
        self.bullet_img = pygame.image.load("pictures/bullet.png")
        self.bullet_img = pygame.transform.scale(self.bullet_img, (30, 30))
        
        # Colors & Fonts
        self.RED, self.GREEN, self.WHITE = (255, 0, 0), (0, 255, 0), (255, 255, 255)
        self.big_font = pygame.font.Font(None, 100)
        self.small_font = pygame.font.Font(None, 36)
        self.extra_small_font = pygame.font.Font(None, 24)
        
        # Initialize Player and Other Game Components
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
        
        self.start_time = pygame.time.get_ticks()
        self.final_time = None
        
        self.skill_tree_active = False
        
        self.database = Database(self)
        
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
                        self))
                elif r < 0.70:
                    self.zombies.append(SpeedyZombie(
                        random.randint(0, self.WORLD_WIDTH - 40),
                        random.randint(0, self.WORLD_HEIGHT - 40),
                        self))
                elif r < 0.85:
                    self.zombies.append(SpitterZombie(
                        random.randint(0, self.WORLD_WIDTH - 40),
                        random.randint(0, self.WORLD_HEIGHT - 40),
                        self))
                else:
                    self.zombies.append(TankyZombie(
                        random.randint(0, self.WORLD_WIDTH - 40),
                        random.randint(0, self.WORLD_HEIGHT - 40),
                        self))
                self.zombie_spawn_timer = 0
            
            desired_king_count = self.zombies_killed // 50
            current_king_count = sum(1 for z in self.zombies if isinstance(z, KingZombie))
            if current_king_count < desired_king_count:
                num_to_spawn = desired_king_count - current_king_count
                for _ in range(num_to_spawn):
                    king_zombie = KingZombie(
                        random.randint(0, self.WORLD_WIDTH - 60),
                        random.randint(0, self.WORLD_HEIGHT - 60),
                        self
                    )
                    self.zombies.append(king_zombie)
            
            new_level = self.zombies_killed // 20
            if new_level > self.current_level:
                self.spawn_interval = max(20, self.spawn_interval - 5)
                self.current_level = new_level
            
            current_time = pygame.time.get_ticks()
            if current_time >= self.player.damage_buff_end_time:
                self.player.damage_multiplier = 1.0
            if current_time >= self.player.speed_buff_end_time:
                self.player.speed_multiplier = 1.0
            
            self.database.update()
            
            if self.player.health <= 0:
                self.game_over = True
                self.final_time = pygame.time.get_ticks() - self.start_time
                self.database.save_data_to_csv()
                
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
            elapsed = self.final_time / 1000
        else:
            elapsed = (pygame.time.get_ticks() - self.start_time) / 1000
        time_text = self.small_font.render(f"Time Survived: {elapsed:.2f}s", True, self.WHITE)
        self.screen.blit(time_text, (20, 70))
        
        self.screen.blit(self.skill_tree_icon, (self.SCREEN_WIDTH - 90, 160))
        
        current_time = pygame.time.get_ticks()
        if current_time < self.player.earthquake_cooldown_end:
            cooldown_time_left = (self.player.earthquake_cooldown_end - current_time) // 1000
            eq_text = self.extra_small_font.render(f"EQ Cooldown: {cooldown_time_left}s", True, self.WHITE)
            eq_rect = eq_text.get_rect(center=(self.SCREEN_WIDTH - 70, 250))
            self.screen.blit(eq_text, eq_rect)
        
        shop_instr = self.extra_small_font.render("Press Tab to Open Shop", True, self.WHITE)
        self.screen.blit(shop_instr, (10, self.SCREEN_HEIGHT - shop_instr.get_height() - 10))
        
        bonus = 0
        if hasattr(self.player.weapon, "base_upgrade_applied") and self.player.weapon.base_upgrade_applied:
            bonus += 50
        if hasattr(self.player.weapon, "stackable_upgrade_applied") and self.player.weapon.stackable_upgrade_applied:
            bonus += 100
        bonus_text_str = f"Weapon Size: +{bonus}%"
        bonus_text = self.extra_small_font.render(bonus_text_str, True, self.WHITE)
        bonus_x = (self.SCREEN_WIDTH - bonus_text.get_width()) // 2
        bonus_y = self.SCREEN_HEIGHT - 50
        self.screen.blit(bonus_text, (bonus_x, bonus_y))
        
        buff_margin = 10
        x_attack = self.SCREEN_WIDTH - self.attack_buff_img.get_width() - buff_margin
        x_speed = self.SCREEN_WIDTH - self.speed_buff_img.get_width() - buff_margin
        
        if current_time < self.player.damage_buff_end_time:
            damage_time_left = (self.player.damage_buff_end_time - current_time) // 1000
            atk_text = self.small_font.render("Attack: " + str(damage_time_left) + "s", True, self.WHITE)
            y_attack = self.SCREEN_HEIGHT - self.attack_buff_img.get_height() - buff_margin
            self.screen.blit(self.attack_buff_img, (x_attack, y_attack))
            self.screen.blit(atk_text, (x_attack - atk_text.get_width() - 5,
                                         y_attack + (self.attack_buff_img.get_height() - atk_text.get_height()) // 2))
        if current_time < self.player.speed_buff_end_time:
            speed_time_left = (self.player.speed_buff_end_time - current_time) // 1000
            spd_text = self.small_font.render("Speed: " + str(speed_time_left) + "s", True, self.WHITE)
            if current_time < self.player.damage_buff_end_time:
                y_speed = self.SCREEN_HEIGHT - self.attack_buff_img.get_height() - self.speed_buff_img.get_height() - (2 * buff_margin)
            else:
                y_speed = self.SCREEN_HEIGHT - self.speed_buff_img.get_height() - buff_margin
            self.screen.blit(self.speed_buff_img, (x_speed, y_speed))
            self.screen.blit(spd_text, (x_speed - spd_text.get_width() - 5,
                                         y_speed + (self.speed_buff_img.get_height() - spd_text.get_height()) // 2))
        
        if self.game_over:
            game_over_text = self.big_font.render("Game Over", True, self.RED)
            restart_text = self.big_font.render("Press R to Restart", True, self.WHITE)
            self.screen.blit(game_over_text, (self.SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
                                               self.SCREEN_HEIGHT // 2 - game_over_text.get_height()))
            self.screen.blit(restart_text, (self.SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
                                            self.SCREEN_HEIGHT // 2 + 20))
            time_text_game_over = self.big_font.render(f"Time Survived: {elapsed:.2f}s", True, self.WHITE)
            self.screen.blit(time_text_game_over, (self.SCREEN_WIDTH // 2 - time_text_game_over.get_width() // 2,
                                                   self.SCREEN_HEIGHT // 2 + 20 + restart_text.get_height() + 10))
        
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