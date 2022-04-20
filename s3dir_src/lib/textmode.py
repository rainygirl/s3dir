import math


class TextMode:
    def __init__(self, screen):
        self.screen = screen

    def clear_area(self, matrix, **kwargs):
        self.screen.fill_polygon([matrix], **kwargs)

    def clear(self):
        self.screen.clear()
        self.screen.refresh()

    def draw_box(self, matrix, **kwargs):

        self.screen.move(matrix[0][0], matrix[0][1])
        for i in range(0, 5):
            self.screen.draw(
                matrix[0 if i == 4 else i][0],
                matrix[0 if i == 4 else i][1],
                char="─" if i % 2 == 1 else "│",
                **kwargs,
            )

        for i, char in enumerate("┌┐┘└"):
            self.screen.print_at(char, matrix[i][0], matrix[i][1], **kwargs)

    def init_screen(self, S):
        S["position"]["sectionWidth"] = int(self.screen.width / 2) - 4
        S["position"]["remote"]["x"] = int(self.screen.width / 2) + 2
        S["rowlimit"] = int(self.screen.height) - 3

    @staticmethod
    def size_humanize(size):
        right_text = str(size)
        if size > 1024 * 1024:
            right_text = str(math.ceil(size / 1024 / 1024 * 10) / 10) + "M"
        elif size > 1024:
            right_text = str(math.ceil(size / 1024 * 10) / 10) + "K"

        return right_text
