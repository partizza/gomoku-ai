class Settings:

    def __init__(self):
        self.screen_background = (127, 127, 127)
        self.screen_width = 800
        self.screen_height = 800

        self.menu_width = 200
        self.menu_height = 50
        self.menu_background = (240, 240, 240)
        self.menu_text_color = (0, 0, 0)
        self.menu_text_size = 30

        self.board_size = 15

        self.line_indent = 50
        self.line_color = (0, 0, 0)

        self.dot_color_black = (0, 0, 0)
        self.dot_color_white = (240, 240, 240)
        self.dot_radius = 20

        self.ai_model = 'gpt-4o'
        self.ai_key_env_variable = 'OPENAI_API_KEY'
