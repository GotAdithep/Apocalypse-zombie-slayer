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
            
            # Toggle shop using Tab (only if not in Skill Tree mode)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB and not game.skill_tree_active:
                    shop_active = not shop_active
                
                # Restart game on R key if game is over.
                if event.key == pygame.K_r and game.game_over:
                    game = Game(screen)
                    shop = Shop(screen, game)
                    skill_tree = SkillTree(screen, game)
                    shop_active = False
            
            # Mouse events handling.
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Left click (button 1):
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    # Fixed rectangle for the Skill Tree icon (positioned as drawn in game_manager.py)
                    skill_tree_rect = pygame.Rect(SCREEN_WIDTH - 90, 160, 80, 80)
                    if skill_tree_rect.collidepoint(mouse_pos) and not shop_active and not game.skill_tree_active:
                        game.skill_tree_active = True
                    # Otherwise, let the player swing their weapon.
                    elif not shop_active and not game.skill_tree_active:
                        game.player.weapon.swing()
                # Right click (button 3): Attempt to activate earthquake skill.
                elif event.button == 3:
                    if not shop_active and not game.skill_tree_active:
                        game.player.activate_earthquake(game)
        
        # Route update/draw calls based on current mode.
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