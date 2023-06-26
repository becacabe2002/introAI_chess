import pygame_menu, pygame

class ChessMenu:
    def __init__(self, WIDTH, HEIGHT, screen, events):
        self.height = HEIGHT
        self.width = WIDTH
        self.screen = screen
        self.events = events
        self.main_menu = pygame_menu.Menu('Chess AI', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_BLUE)
        self.mode_menu = pygame_menu.Menu('Choose mode', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_BLUE)
        self.algorithm_menu = pygame_menu.Menu('Choose algorithm', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_BLUE)
        self.depth_menu = pygame_menu.Menu('Choose depth', WIDTH, HEIGHT,
                       theme=pygame_menu.themes.THEME_BLUE)
        self.algorithm = None
        self.mode = None
        self.depth = None

    def show_main_menu(self):
        # mode menu
        self.mode_menu.add.button("Human vs Human", self.set_mode, 'hvh') 
        self.mode_menu.add.button("Human vs AI", self.set_mode, 'hva') 
        self.mode_menu.add.button("AI vs AI", self.set_mode, 'ava')
        self.mode_menu.add.button('Back', pygame_menu.events.BACK)

        # algorithm menu
        # self.algorithm_menu.add.button("Greedy", self.set_algorithm, 'greedy')
        self.algorithm_menu.add.button("Minmax", self.set_algorithm, 'minmax')
        self.algorithm_menu.add.button("NegaMax", self.set_algorithm, 'negamax')
        self.algorithm_menu.add.button("Alpha-Beta Pruning", self.set_algorithm, 'alpha-beta-pruning')
        self.algorithm_menu.add.button("Back", pygame_menu.events.BACK)

        # depth menu
        range_values = {0: '1', 1: '2', 2: '3', 3: '4'}
        self.depth_menu.add.range_slider('Depth', 0, list(range_values.keys()),
                                         slider_text_value_enabled=False,
                                         value_format=lambda x: range_values[x], onchange=self.set_depth)
        self.depth_menu.add.button("Play", self.depth_menu.disable)

        # main menu
        self.main_menu.add.button("Begin",self.mode_menu)
        self.main_menu.add.button('Quit', pygame_menu.events.EXIT)
        self.main_menu.mainloop(self.screen)
    
    def set_mode(self, mode: str):
        if mode == 'hvh': # if human vs human then play immediately
            self.mode_menu.disable()
        self.mode_menu._open(self.algorithm_menu) # open next menu
        self.mode = mode
        print(self.mode)

    def set_algorithm(self, algorithm: str):
        self.algorithm_menu._open(self.depth_menu) # open next menu
        self.algorithm = algorithm
        print(self.algorithm)

    # on change call function for depth range slider
    def set_depth(self, range_value):
        self.depth = range_value + 1
        print(self.depth)