import pygame
from game_manager import Game
from shop import Shop
from entity import Zombie, SpeedyZombie, TankyZombie

def main():
    pygame.init()
    SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Zombie Survival")
    clock = pygame.time.Clock()

    game = Game(screen)
    shop = Shop(screen, game)
    
    shop_active = False
    
    running = True
    while running:
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    shop_active = not shop_active
                
                if event.key == pygame.K_r and game.game_over:
                    game = Game(screen)         
                    shop = Shop(screen, game)
                    shop_active = False
        
        if shop_active and not game.game_over:
            shop.update(events)
            shop.draw()
        else:
            for event in events:
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not shop_active:
                    game.player.weapon.swing()
            game.update()
            game.draw()
        
        pygame.display.flip()
        clock.tick(30)
        
    pygame.quit()

if __name__ == "__main__":
    main()
