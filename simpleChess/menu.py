import pygame_menu

class ChessMenu:
    def __init__(self, WIDTH, HEIGHT, screen):
        self.height = HEIGHT
        self.width = WIDTH
        self.screen = screen
        self.main_menu = pygame_menu.Menu('Chess AI', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_BLUE)
        self.mode_menu = pygame_menu.Menu('Choose mode', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_BLUE)
        self.algorithm_menu = pygame_menu.Menu('Choose algorithm', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_BLUE)
        self.depth_menu = pygame_menu.Menu('Choose depth', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_BLUE)

    def show_main_menu(self):
        # mode menu
        self.mode_menu.add.button("Human vs Human", self.algorithm_menu)
        self.mode_menu.add.button("Human vs AI", self.algorithm_menu)
        self.mode_menu.add.button("AI vs AI", self.algorithm_menu)
        self.mode_menu.add.button('Back', pygame_menu.events.BACK)

        # algorithm menu
        self.algorithm_menu.add.button("Greedy", self.depth_menu)
        self.algorithm_menu.add.button("Minmax", self.depth_menu)
        self.algorithm_menu.add.button("NegaMax", self.depth_menu)
        self.algorithm_menu.add.button("Alpha-Beta Pruning", self.depth_menu)
        self.algorithm_menu.add.button("Back", pygame_menu.events.BACK)

        # depth menu
        range_values = {0: '1', 1: '2', 2: '3', 3: '4'}
        self.depth_menu.add.range_slider('Depth', 0, list(range_values.keys()),
                                         slider_text_value_enabled=False,
                                         value_format=lambda x: range_values[x])
        self.depth_menu.add.button("Play")

        self.main_menu.add.button("Play",self.mode_menu)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)
        self.main_menu.mainloop(self.screen)