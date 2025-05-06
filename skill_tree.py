import pygame

class SkillTree:
    def __init__(self, screen, game):
        """
        screen: the Pygame surface to draw on.
        game: a reference to the Game instance.
        """
        self.screen = screen
        self.game = game

        # Use the skill tree background image from the "images" folder.
        self.background_img = pygame.image.load("images/skill_tree_background.jpg")
        self.background_img = pygame.transform.scale(self.background_img, (self.screen.get_width(), self.screen.get_height()))

        # Load icons for the items.
        self.attack_buff_img = pygame.image.load("images/attack_buff.png")
        self.attack_buff_img = pygame.transform.scale(self.attack_buff_img, (50, 50))
        self.earthquake_img = pygame.image.load("images/earthquake.png")
        self.earthquake_img = pygame.transform.scale(self.earthquake_img, (50, 50))

        # Use smaller fonts: normal text = 24, title = 48, small = 20.
        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 20)

        # --- Set up Permanent Attack Buff Item ---
        if not hasattr(self.game.player.weapon, "perm_attack_buff_bought"):
            self.game.player.weapon.perm_attack_buff_bought = False
        self.permanent_attack_buff_bought = self.game.player.weapon.perm_attack_buff_bought
        self.item1_text = "PRESS 7: Permanent Attack Buff - Cost: 1 Enhance Point"

        # --- Set up Earthquake Skill Unlock Item ---
        self.earthquake_unlocked = self.game.player.earthquake_unlocked
        self.item2_text = "PRESS 8: Earthquake Skill Unlock - Cost: 5 Enhance Points"

        # Horizontal offset to nudge all text to the right
        self.text_offset_x = 80

    def update(self, events):
        """
        Process user inputs for the Skill Tree screen:
          - Press ESC to return to the main game.
          - Press 7 to purchase the Permanent Attack Buff upgrade.
          - Press 8 to purchase the Earthquake Skill Unlock.
        """
        for event in events:
            if event.type == pygame.KEYDOWN:
                # Exit Skill Tree screen on ESC key.
                if event.key == pygame.K_ESCAPE:
                    self.game.skill_tree_active = False
                elif event.key == pygame.K_7:
                    if not self.permanent_attack_buff_bought:
                        if self.game.player.enhance_points >= 1:
                            self.game.player.enhance_points -= 1
                            # Apply a permanent buff on the weapon.
                            self.game.player.weapon.damage = int(self.game.player.weapon.damage * 1.5)
                            self.permanent_attack_buff_bought = True
                            self.game.player.weapon.perm_attack_buff_bought = True
                        else:
                            print("Not enough enhance points for Permanent Attack Buff!")
                elif event.key == pygame.K_8:
                    if not self.earthquake_unlocked:
                        if self.game.player.enhance_points >= 5:
                            self.game.player.enhance_points -= 5
                            self.earthquake_unlocked = True
                            self.game.player.earthquake_unlocked = True
                            print("Earthquake skill unlocked!")
                        else:
                            print("Not enough enhance points for Earthquake Skill!")

    def draw(self):
        """
        Render the Skill Tree screen.
        """
        # Draw the background.
        self.screen.blit(self.background_img, (0, 0))

        # Draw the title, centered at the top.
        title_text = self.title_font.render("Skill Tree", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 40))
        self.screen.blit(title_text, title_rect)

        # Define the horizontal offset for texts.
        offset = self.text_offset_x

        # --- Draw Permanent Attack Buff Item ---
        item1_surface = self.font.render(self.item1_text, True, (255, 255, 255))
        # Move the text to the right using the offset.
        item1_rect = item1_surface.get_rect(topleft=(50 + offset, 100))
        self.screen.blit(item1_surface, item1_rect)
        # Draw its icon to the right of the text.
        icon1_x = item1_rect.right + 10
        icon1_y = item1_rect.top
        self.screen.blit(self.attack_buff_img, (icon1_x, icon1_y))
        # Display purchase status.
        status1 = "Purchased" if self.permanent_attack_buff_bought else "Not Purchased"
        color1 = (0, 255, 0) if self.permanent_attack_buff_bought else (255, 0, 0)
        status1_surface = self.font.render("Status: " + status1, True, color1)
        status1_rect = status1_surface.get_rect(topleft=(50 + offset, item1_rect.bottom + 5))
        self.screen.blit(status1_surface, status1_rect)

        # --- Draw Earthquake Skill Unlock Item ---
        item2_surface = self.font.render(self.item2_text, True, (255, 255, 255))
        item2_rect = item2_surface.get_rect(topleft=(50 + offset, status1_rect.bottom + 20))
        self.screen.blit(item2_surface, item2_rect)
        # Draw its icon to the right of the text.
        icon2_x = item2_rect.right + 10
        icon2_y = item2_rect.top
        self.screen.blit(self.earthquake_img, (icon2_x, icon2_y))
        # Display purchase status.
        status2 = "Unlocked" if self.earthquake_unlocked else "Locked"
        color2 = (0, 255, 0) if self.earthquake_unlocked else (255, 0, 0)
        status2_surface = self.font.render("Status: " + status2, True, color2)
        status2_rect = status2_surface.get_rect(topleft=(50 + offset, item2_rect.bottom + 5))
        self.screen.blit(status2_surface, status2_rect)

        # Draw an instruction to exit.
        exit_surface = self.small_font.render("Press ESC to return to game", True, (200, 200, 200))
        exit_rect = exit_surface.get_rect(topleft=(50 + offset, status2_rect.bottom + 20))
        self.screen.blit(exit_surface, exit_rect)