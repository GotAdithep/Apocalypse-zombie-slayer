import pygame

class SkillTree:
    def __init__(self, screen, game):

        self.screen = screen
        self.game = game

        self.background_img = pygame.image.load("images/skill_tree_background.jpg")
        self.background_img = pygame.transform.scale(self.background_img, (self.screen.get_width(), self.screen.get_height()))

        self.attack_buff_img = pygame.image.load("images/attack_buff.png")
        self.attack_buff_img = pygame.transform.scale(self.attack_buff_img, (50, 50))
        self.earthquake_img = pygame.image.load("images/earthquake.png")
        self.earthquake_img = pygame.transform.scale(self.earthquake_img, (50, 50))
        self.heal_img = pygame.image.load("images/heal.webp")
        self.heal_img = pygame.transform.scale(self.heal_img, (50, 50))

        self.font = pygame.font.Font(None, 24)
        self.title_font = pygame.font.Font(None, 48)
        self.small_font = pygame.font.Font(None, 20)

        if not hasattr(self.game.player.weapon, "perm_attack_buff_bought"):
            self.game.player.weapon.perm_attack_buff_bought = False
        self.permanent_attack_buff_bought = self.game.player.weapon.perm_attack_buff_bought
        self.item1_text = "PRESS 7: Permanent Attack Buff - Cost: 1 Enhance Point"

        self.earthquake_unlocked = self.game.player.earthquake_unlocked
        self.item2_text = "PRESS 8: Earthquake Skill Unlock - Cost: 5 Enhance Points"

        self.heal_item_text = "PRESS 9: Heal 100 Health - Cost: 1 Enhance Point"

        self.text_offset_x = 80

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.game.skill_tree_active = False
                elif event.key == pygame.K_7:
                    if not self.permanent_attack_buff_bought:
                        if self.game.player.enhance_points >= 1:
                            self.game.player.enhance_points -= 1
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
                elif event.key == pygame.K_9:
                    if self.game.player.enhance_points >= 1:
                        self.game.player.enhance_points -= 1
                        self.game.player.health = min(200, self.game.player.health + 100)
                        print("Healed 100 health!")
                    else:
                        print("Not enough enhance points for healing!")

    def draw(self):
        self.screen.blit(self.background_img, (0, 0))

        title_text = self.title_font.render("Skill Tree", True, (255, 215, 0))
        title_rect = title_text.get_rect(center=(self.screen.get_width() // 2, 40))
        self.screen.blit(title_text, title_rect)

        offset = self.text_offset_x

        item1_surface = self.font.render(self.item1_text, True, (255, 255, 255))
        item1_rect = item1_surface.get_rect(topleft=(50 + offset, 100))
        self.screen.blit(item1_surface, item1_rect)

        icon1_x = item1_rect.right + 10
        icon1_y = item1_rect.top
        self.screen.blit(self.attack_buff_img, (icon1_x, icon1_y))

        status1 = "Purchased" if self.permanent_attack_buff_bought else "Not Purchased"
        color1 = (0, 255, 0) if self.permanent_attack_buff_bought else (255, 0, 0)
        status1_surface = self.font.render("Status: " + status1, True, color1)
        status1_rect = status1_surface.get_rect(topleft=(50 + offset, item1_rect.bottom + 5))
        self.screen.blit(status1_surface, status1_rect)

        item2_surface = self.font.render(self.item2_text, True, (255, 255, 255))
        item2_rect = item2_surface.get_rect(topleft=(50 + offset, status1_rect.bottom + 20))
        self.screen.blit(item2_surface, item2_rect)

        icon2_x = item2_rect.right + 10
        icon2_y = item2_rect.top
        self.screen.blit(self.earthquake_img, (icon2_x, icon2_y))

        status2 = "Unlocked" if self.earthquake_unlocked else "Locked"
        color2 = (0, 255, 0) if self.earthquake_unlocked else (255, 0, 0)
        status2_surface = self.font.render("Status: " + status2, True, color2)
        status2_rect = status2_surface.get_rect(topleft=(50 + offset, item2_rect.bottom + 5))
        self.screen.blit(status2_surface, status2_rect)

        heal_surface = self.font.render(self.heal_item_text, True, (255, 255, 255))
        heal_rect = heal_surface.get_rect(topleft=(50 + offset, status2_rect.bottom + 20))
        self.screen.blit(heal_surface, heal_rect)

        icon_heal_x = heal_rect.right + 10
        icon_heal_y = heal_rect.top
        self.screen.blit(self.heal_img, (icon_heal_x, icon_heal_y))

        exit_surface = self.small_font.render("Press ESC to return to game", True, (200, 200, 200))
        exit_rect = exit_surface.get_rect(topleft=(50 + offset, heal_rect.bottom + 20))
        self.screen.blit(exit_surface, exit_rect)

        enhance_points_text = self.font.render(f"Enhance Points: {self.game.player.enhance_points}", True, (255, 255, 255))
        enhance_points_rect = enhance_points_text.get_rect()
        enhance_points_rect.bottomright = (self.screen.get_width() - 20, self.screen.get_height() - 20)
        self.screen.blit(enhance_points_text, enhance_points_rect)