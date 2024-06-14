import sys

import pygame
from button import Button
from enum import Enum


class MenuLabel(Enum):
    PLAYER_VS_PLAYER = 0
    PLAYER_VS_AI = 1
    EXIT = 2

    def text(self):
        return self.name.replace('_',' ')

class Menu:

    def __init__(self, game):
        self.screen = game.screen
        self.settings = game.settings
        self.buttons = pygame.sprite.Group()
        self.selected = None

        # buttons
        for lable in list(MenuLabel):
            self._add_button_(lable)

    def _add_button_(self, label):
        center_height = self.settings.menu_height * 3 + self.settings.menu_height * 1.5 * label.value
        self.buttons.add(Button(self.settings.menu_width,
                                self.settings.menu_height,
                                (self.screen.get_rect().center[0], center_height),
                                self._text_surface_(label.text()),
                                self.settings.menu_background,
                                label))

    def _text_surface_(self, text_string):
        font = pygame.font.SysFont(None, self.settings.menu_text_size)
        return font.render(text_string, True, self.settings.menu_text_color, self.settings.menu_background)

    def blit(self):
        self.buttons.draw(self.screen)

    def process_click(self, position):
        for button in self.buttons:
            if button.collide(position):
                self.selected = button.label
                if button.label == MenuLabel.EXIT:
                    sys.exit()
                else:
                    return
