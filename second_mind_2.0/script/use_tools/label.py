import pygame as pg
from settings import LABEL_FONT, LABEL_COLOR, LABEL_FONT_SIZE


class Label:
    def __init__(self, x, y, text, color=None, font=None, font_size=None):
        self.x = x
        self.y = y
        self.color = color if color else LABEL_COLOR
        self.font = font if font else LABEL_FONT
        self.font_size = font_size if font_size else LABEL_FONT_SIZE

        self.surface = self.__set_text(text) if text else pg.Surface((1, 1))

    def __set_text(self, text):
        surface = pg.font.Font(self.font, self.font_size)
        surface = surface.render(text, True, self.color)
        return surface

    def draw(self, sc: pg.Surface):
        sc.blit(self.surface, (self.x, self.y))


class ManyLabel(Label):
    def __init__(self, x, y, width, text, color=None, font=None, font_size=None):
        super().__init__(x, y, text=None, color=color, font=font, font_size=font_size)
        self.width = width
        self.surface = self.__set_text(text) if text else pg.Surface((1, 1))

    def __set_text(self, text: str):
        font = pg.font.Font(self.font, self.font_size)
        space = font.render(' ', False, (0, 0, 0))
        space_w = space.get_width()
        op_del = space.get_height() * 0.5

        words = text.split(' ')
        words = [font.render(i, True, self.color) for i in words]
        rows = []
        buf = []
        for i in range(len(words)):
            if words[i].get_width() + space_w + sum(map(lambda x: x.get_width(), buf)) > self.width:
                rows.append(buf)
                buf = [words[i]]
            else:
                buf.append(words[i])
        if buf:
            rows.append(buf)

        # create surface
        surface_height = int(len(rows) * (space.get_height() + op_del))
        surface = pg.Surface((self.width, surface_height)).convert_alpha()
        surface.fill((0, 0, 0, 0))
        y = 0

        for row in rows:
            x = 0
            for word in row:
                surface.blit(word, (x, y))
                x += word.get_width() + space_w
            y += op_del + space.get_height()

        return surface
