import pygame, pygame_menu

class ChessMenu:
    def __init__(self, WIDTH, HEIGHT, screen):
        self.height = HEIGHT
        self.width = WIDTH
        self.screen = screen
        self.main_menu = pygame_menu.Menu('Chess AI', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)
        self.mode_menu = pygame_menu.Menu('Choose mode', 400, 300,
                       theme=pygame_menu.themes.THEME_BLUE)

    def show_main_menu(self):

        self.mode_menu.add.button("Human vs AI",self.mode_menu.disable)
        self.mode_menu.add.button('Back', pygame_menu.events.BACK)
        
        self.main_menu.add.button("Play",self.mode_menu)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)
        self.main_menu.mainloop(self.screen)