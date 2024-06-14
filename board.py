import pygame
from dot import Dot
from counter import Counter


class Board:
    """Board of the game: view and dots"""

    def __init__(self, game):
        self.screen = game.screen
        self.settings = game.settings
        self.dots_matrix = self._init_dots_matrix()
        self.active_dots = pygame.sprite.Group()
        self.current_dot_color = self.settings.dot_color_black
        self.winner = None
        self.finished = False

    def _init_dots_matrix(self):
        return [[self._init_dot(i, j) for i in range(self.settings.board_size)] for j in
                range(self.settings.board_size)]

    def _init_dot(self, column, row):
        return Dot(self, self.settings.dot_color_black, self.dot_coordinates(column, row))

    def dot_coordinates(self, x, y):
        indent = self.settings.line_indent
        return (x + 1) * indent, (y + 1) * indent

    def white_dot_matrix_positions(self):
        whites = []
        for y in range(self.settings.board_size):
            for x in range(self.settings.board_size):
                dot = self.dots_matrix[y][x]
                if dot.active and dot.color == self.settings.dot_color_white:
                    whites.append((x, y))

        return whites

    def black_dot_matrix_positions(self):
        blacks = []
        for y in range(self.settings.board_size):
            for x in range(self.settings.board_size):
                dot = self.dots_matrix[y][x]
                if dot.active and dot.color == self.settings.dot_color_black:
                    blacks.append((x, y))

        return blacks

    def empty_dot_matrix_positions(self):
        empties = []
        for y in range(self.settings.board_size):
            for x in range(self.settings.board_size):
                dot = self.dots_matrix[y][x]
                if not dot.active:
                    empties.append((x, y))

        return empties

    def update(self):
        self._update_background()
        self._update_dots()

    def _update_background(self):
        indent = self.settings.line_indent / 2

        for k in range(self.settings.board_size):
            position = (k + 1) * self.settings.line_indent

            pygame.draw.line(self.screen, self.settings.line_color,
                             (position, indent),
                             (position, self.screen.get_height() - indent))

            pygame.draw.line(self.screen, self.settings.line_color,
                             (indent, position),
                             (self.screen.get_width() - indent, position))

    def _update_dots(self):
        self.active_dots.draw(self.screen)

    def process_click(self, position):
        """return True if a new dot activated, else - False"""

        for row in self.dots_matrix:
            for dot in row:
                if not dot.active and dot.collide(position):
                    dot.activate(self.current_dot_color)
                    self.active_dots.add(dot)
                    self._change_current_color()
                    self._check_status()
                    return True

        return False

    def _change_current_color(self):
        if self.current_dot_color == self.settings.dot_color_black:
            self.current_dot_color = self.settings.dot_color_white
        else:
            self.current_dot_color = self.settings.dot_color_black

    def _check_status(self):
        if self._has_five_in_row() or not self._has_open_position():
            self.finished = True

    def _has_open_position(self):
        for row in self.dots_matrix:
            for dot in row:
                if not dot.active:
                    return True
        # there are no more position to place dot on the board
        return False

    def _has_five_in_row(self):
        return (self._check_five_horizontally()
                or self._check_five_vertically()
                or self._check_five_diagonally_from_left_to_right()
                or self._check_five_diagonally_from_right_to_left())

    def _check_five_horizontally(self):
        for row in self.dots_matrix:
            counter = Counter(self)
            for dot in row:
                counter.update(dot)
                if counter.has_five():
                    self.winner = counter.color_name()
                    return True

        return False

    def _check_five_vertically(self):
        for c in range(self.settings.board_size):
            counter = Counter(self)
            for r in range(self.settings.board_size):
                dot = self.dots_matrix[r][c]
                counter.update(dot)
                if counter.has_five():
                    self.winner = counter.color_name()
                    return True

        return False

    def _check_five_diagonally_from_left_to_right(self):
        # right-top
        for i in range(self.settings.board_size):
            counter = Counter(self)
            for k in range(0, self.settings.board_size - i):
                dot = self.dots_matrix[k][k + i]
                counter.update(dot)
                if counter.has_five():
                    self.winner = counter.color_name()
                    return True

        # left-bottom
        for i in range(1, self.settings.board_size, 1):
            counter = Counter(self)
            for k in range(0, self.settings.board_size - i):
                dot = self.dots_matrix[k + i][k]
                counter.update(dot)
                if counter.has_five():
                    self.winner = counter.color_name()
                    return True

        return False

    def _check_five_diagonally_from_right_to_left(self):
        # left-top
        for i in range(self.settings.board_size):
            counter = Counter(self)
            for k in range(self.settings.board_size - i - 1, -1, -1):
                dot = self.dots_matrix[self.settings.board_size - i - 1 - k][k]
                counter.update(dot)
                if counter.has_five():
                    self.winner = counter.color_name()
                    return True

        # right-bottom
        for i in range(self.settings.board_size):
            counter = Counter(self)
            for k in range(i, self.settings.board_size, 1):
                dot = self.dots_matrix[k][self.settings.board_size - k - 1 + i]
                counter.update(dot)
                if counter.has_five():
                    self.winner = counter.color_name()
                    return True

        return False
