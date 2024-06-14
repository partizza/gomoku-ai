from dot import Dot


class Counter:

    def __init__(self, board):
        self.color = None
        self.count = 0
        self.settings = board.settings

    def update(self, dot):
        if not dot.active:
            self.color = None
            self.count = 0
        elif dot.active and self.color == dot.color:
            self.count += 1
        else:
            self.color = dot.color
            self.count = 1

    def has_five(self):
        return self.count >= 5

    def color_name(self):
        if self.color == self.settings.dot_color_black:
            return 'Black'
        elif self.color == self.settings.dot_color_white:
            return 'White'
        else:
            return 'Unnamed'
