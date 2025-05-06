import pygame
from game_manager import Game
from shop import Shop
from skill_tree import SkillTree

def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Zombie Survival")
    clock = pygame.time.Clock()

    game = Game(screen)
    shop = Shop(screen, game)
    skill_tree = SkillTree(screen, game)
    
    shop_active = False
    
    running = True
    while running:
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB and not game.skill_tree_active:
                    shop_active = not shop_active
                

                if event.key == pygame.K_r and game.game_over:
                    game = Game(screen)
                    shop = Shop(screen, game)
                    skill_tree = SkillTree(screen, game)
                    shop_active = False
            

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    skill_tree_rect = pygame.Rect(SCREEN_WIDTH - 90, 160, 80, 80)
                    if skill_tree_rect.collidepoint(mouse_pos) and not shop_active and not game.skill_tree_active:
                        game.skill_tree_active = True
                    elif not shop_active and not game.skill_tree_active:
                        game.player.weapon.swing()
                elif event.button == 3:
                    if not shop_active and not game.skill_tree_active:
                        game.player.activate_earthquake(game)
        
        if shop_active:
            shop.update(events)
            shop.draw()
        elif game.skill_tree_active:
            skill_tree.update(events)
            skill_tree.draw()
        else:
            game.update()
            game.draw()
                
        pygame.display.flip()
        clock.tick(30)
        
    pygame.quit()

if __name__ == "__main__":
    main()