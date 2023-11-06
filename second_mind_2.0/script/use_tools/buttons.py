import pygame as pg
from settings import *


class Click:
    def __init__(self, x, y, w, h):
        self.rect = pg.Rect(x, y, w, h)

    def __call__(self, x, y):
        return self.rect.collidepoint(x, y)


class DefButton(Click):
    def __init__(self, x, y, w, h, text='', func=lambda: None):
        super().__init__(x, y, w, h)
        self.text = text
        self.func = func
        self.__create_def_look()

        self.draw_surf = self.def_surf

    def update(self, x, y, pressed):
        flag = self(x, y)
        self.draw_surf = self.act_surf if flag else self.def_surf

        if flag:
            if pressed:
                self.func()
            return True
        return False

    def draw(self, sc: pg.Surface):
        sc.blit(self.draw_surf, self.rect)

    def __create_def_look(self):
        text = pg.font.Font(FONT, SMALL_FONT_SIZE)
        text = text.render(self.text, True, BUTTON_TEXT_COLOR)
        tr = text.get_rect()
        tr.center = (self.rect.w / 2, self.rect.h / 2)

        self.def_surf = self.__create_color_surf(DEF_COLOR)
        self.act_surf = self.__create_color_surf(ACT_COLOR)

        self.def_surf.blit(text, tr)
        self.act_surf.blit(text, tr)

    def __create_color_surf(self, color):
        surf = pg.Surface(self.rect.size).convert_alpha()
        surf.fill((0, 0, 0, 0))
        pg.draw.rect(surf, color, (0, 0, *self.rect.size), border_radius=10)
        pg.draw.rect(surf, ROUND_COLOR, (5, 5, self.rect.w - 10, self.rect.h - 10), border_radius=10, width=3)
        return surf

