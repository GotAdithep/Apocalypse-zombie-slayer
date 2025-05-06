import pygame

class Shop:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.width, self.height = screen.get_width(), screen.get_height()
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 48)
        
        self.attack_buff_img = pygame.image.load("pictures/attack_buff.png")
        self.attack_buff_img = pygame.transform.scale(self.attack_buff_img, (50, 50))
        self.speed_buff_img = pygame.image.load("pictures/speed_buff.webp")
        self.speed_buff_img = pygame.transform.scale(self.speed_buff_img, (50, 50))
    
    def update(self, events):
        current_time = pygame.time.get_ticks()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if self.game.coin_count >= 400 and current_time >= self.game.player.damage_buff_end_time:
                        self.game.coin_count -= 400
                        self.game.player.damage_multiplier = 1.5
                        self.game.player.damage_buff_end_time = current_time + 60000
                        self.game.player.attack_buff_usage_count += 1
                elif event.key == pygame.K_2:
                    if self.game.coin_count >= 400 and current_time >= self.game.player.speed_buff_end_time:
                        self.game.coin_count -= 400
                        self.game.player.speed_multiplier = 1.5
                        self.game.player.speed_buff_end_time = current_time + 60000
                        self.game.player.speed_buff_usage_count += 1
                elif event.key == pygame.K_3:
                    if self.game.coin_count >= 1500 and not self.game.player.weapon.base_upgrade_applied:
                        self.game.coin_count -= 1500
                        self.game.player.weapon.size_multiplier += 0.5
                        self.game.player.weapon.base_upgrade_applied = True
                elif event.key == pygame.K_4:
                    if self.game.coin_count >= 5000 and not self.game.player.weapon.stackable_upgrade_applied:
                        self.game.coin_count -= 5000
                        self.game.player.weapon.size_multiplier += 1.0
                        self.game.player.weapon.stackable_upgrade_applied = True

    def draw(self):
        overlay = pygame.Surface((self.width, self.height))
        overlay.set_alpha(220)
        overlay.fill((30, 30, 30))
        self.screen.blit(overlay, (0, 0))
        
        # Draw the shop panel.
        panel_width = self.width - 100
        panel_height = self.height - 100
        panel_x = 50
        panel_y = 50
        pygame.draw.rect(self.screen, (50, 50, 50), (panel_x, panel_y, panel_width, panel_height))
        pygame.draw.rect(self.screen, (255, 255, 0), (panel_x, panel_y, panel_width, panel_height), 3)
        
        title = self.title_font.render("SHOP", True, (255, 215, 0))
        title_rect = title.get_rect(center=(self.width // 2, panel_y + 40))
        self.screen.blit(title, title_rect)
        
        base_y = panel_y + 80
        item_spacing = 60
        
        # Item 1: Attack Buff.
        self.screen.blit(self.attack_buff_img, (panel_x + 20, base_y))
        item1_text = self.font.render("PRESS 1: Increase Attack 50% (1 min) - 400 coins", True, (255, 255, 255))
        self.screen.blit(item1_text, (panel_x + 80, base_y + 5))
        
        # Item 2: Speed Buff.
        self.screen.blit(self.speed_buff_img, (panel_x + 20, base_y + item_spacing))
        item2_text = self.font.render("PRESS 2: Increase Speed 50% (1 min) - 400 coins", True, (255, 255, 255))
        self.screen.blit(item2_text, (panel_x + 80, base_y + item_spacing + 5))
        
        # Item 3: Bigger Weapon & Range +50%.
        item3_text = self.font.render("PRESS 3: Bigger Weapon & Range +50% - 1500 coins", True, (255, 255, 255))
        self.screen.blit(item3_text, (panel_x + 20, base_y + item_spacing * 2))
        item3_status = "Bought" if self.game.player.weapon.base_upgrade_applied else "Unbought"
        status_color = (0, 255, 0) if item3_status == "Bought" else (255, 0, 0)
        item3_status_text = self.font.render(item3_status, True, status_color)
        status_rect = item3_status_text.get_rect(right=panel_x + panel_width - 20, centery=base_y + item_spacing * 2 + 10)
        self.screen.blit(item3_status_text, status_rect)
        
        # Item 4: Bigger Weapon & Range +100%.
        item4_text = self.font.render("PRESS 4: Bigger Weapon & Range +100% - 5000 coins", True, (255, 255, 255))
        self.screen.blit(item4_text, (panel_x + 20, base_y + item_spacing * 3))
        item4_status = "Bought" if self.game.player.weapon.stackable_upgrade_applied else "Unbought"
        status_color = (0, 255, 0) if item4_status == "Bought" else (255, 0, 0)
        item4_status_text = self.font.render(item4_status, True, status_color)
        status_rect = item4_status_text.get_rect(right=panel_x + panel_width - 20, centery=base_y + item_spacing * 3 + 10)
        self.screen.blit(item4_status_text, status_rect)
        
        coin_text = self.font.render(f"Coins: {self.game.coin_count}", True, (173, 216, 230))
        coin_rect = coin_text.get_rect(bottomright=(panel_x + panel_width - 20, panel_y + panel_height - 20))
        self.screen.blit(coin_text, coin_rect)