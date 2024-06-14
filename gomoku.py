import pygame
import sys
from settings import Settings
from board import Board
from menu import Menu
from menu import MenuLabel
from ai_player import AiPlayer


class Gomoku:
    """Main class implementing game"""

    def __init__(self):
        """Init game"""

        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        pygame.display.set_caption("Gomoku")

        self.board = Board(self)
        self.menu = Menu(self)
        self.ai_player = AiPlayer(self, self.board)

    def play(self):
        """Run the game"""

        while True:
            self.update_screen()
            self.wait_events()

    def update_screen(self):
        """Updates screen"""

        self.screen.fill(self.settings.screen_background)

        if self.menu.selected is None:
            self.menu.blit()
        elif self.board.finished:
            self.board.update()
            self._print_winner()
        else:
            self.board.update()

        pygame.display.flip()

    def _print_winner(self):
        text = self._winner_text()
        text_rec = text.get_rect()
        text_rec.center = (self.screen.get_width() / 2, self.screen.get_height() / 2)
        self.screen.blit(text, text_rec)

    def _winner_text(self):
        font = pygame.font.SysFont(None, 50)
        if self.board.winner is None:
            return font.render('The game ended with a draw', True, (0, 0, 255), self.settings.screen_background)
        else:
            return font.render(f'{self.board.winner} won the game !!!', True, (0, 0, 255),
                               self.settings.screen_background)

    def wait_events(self):
        event = pygame.event.wait()

        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.process_mouse_click(event)

    def process_mouse_click(self, event):
        if self.menu.selected is None:
            self.menu.process_click(event.pos)
        elif not self.board.finished:
            isDotPlaced = self.board.process_click(event.pos)
            if isDotPlaced and not self.board.finished and self.menu.selected == MenuLabel.PLAYER_VS_AI:
                self.update_screen()
                self.make_ai_move()

    def make_ai_move(self):
        attempt = 1
        while attempt < 4:
            ai_position = self.ai_player.make_move()
            dot_pos = self.board.dot_coordinates(ai_position[0], ai_position[1])
            isDotPlaced = self.board.process_click(dot_pos)
            if isDotPlaced:
                return

        raise Exception(f"Can't make AI move in {attempt} attempts")


if __name__ == '__main__':
    gomoku = Gomoku()
    gomoku.play()
