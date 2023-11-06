import pygame as pg
from script.main_loop import MainLoop
from script.use_tools.label import ManyLabel
from script.use_tools.buttons import DefButton
from script.use_tools.timer import Timer


class OkMessage:
    def __init__(self, text, timer=None):
        self.main_loop = MainLoop(fps=30, uf=self.update, df=self.draw)
        self.screen = pg.display.get_surface()

        # find size and coords
        dt = 30  # padding
        w, h = self.screen.get_size()
        label_w = w // 3 - 2 * dt
        self.label = ManyLabel(dt, dt, label_w,
                               text, font_size=self.screen.get_height() // 30)
        label_h = self.label.surface.get_height()

        # create a surface
        # in this time I like to use surface like button
        # And create a true button for ok

        button_w = label_w // 3
        button_h = h // 20
        button_x = (w // 3 - button_w) / 2
        button_y = 2 * dt + label_h

        self.button = DefButton(button_x, button_y, button_w, button_h,
                                text='Хорошо', func=self.main_loop.exit)

        surface_w = w // 3
        surface_h = label_h + 3 * dt + button_h
        surface_x = self.x = (w - surface_w) / 2
        surface_y = self.y = (h - surface_h) / 2

        self.render_surface = DefButton(surface_x, surface_y, surface_w, surface_h)
        self.label.draw(self.render_surface.act_surf)

        # timer
        if timer:
            self.timer = Timer(timer)
            self.timer.run()
        else:
            self.timer = lambda: False

    def run(self):
        self.main_loop.run()
        return True

    def draw(self):
        self.button.draw(self.render_surface.act_surf)
        self.screen.blit(self.render_surface.act_surf, self.render_surface.rect)
        pg.display.update()

    def update(self, events):
        mx, my = pg.mouse.get_pos()
        mx -= self.x
        my -= self.y
        pressed = False
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pressed = True

        self.button.update(mx, my, pressed)
        if self.timer():
            self.main_loop.exit()


class YesNoMessage(OkMessage):
    def __init__(self, text):
        super(YesNoMessage, self).__init__(text)

        self.answer = False

        # create a new button and search new coordinates
        w = self.render_surface.rect.w
        button_w, button_h = self.button.rect.size
        button_y = self.button.rect.top
        del self.button

        dt = w - 2 * button_w
        dt /= 3

        self.button_yes = DefButton(dt, button_y, button_w, button_h,
                                    text='Да', func=lambda: self.__set_answer(True))
        self.button_no = DefButton(2 * dt + button_w, button_y, button_w, button_h,
                                   text='Нет', func=lambda: self.__set_answer(False))

        self.buttons = (self.button_no, self.button_yes)

    def run(self):
        self.main_loop.run()
        return self.answer

    def draw(self):
        for i in self.buttons:
            i.draw(self.render_surface.act_surf)
        self.screen.blit(self.render_surface.act_surf, self.render_surface.rect)
        pg.display.update()

    def update(self, events):
        mx, my = pg.mouse.get_pos()
        mx -= self.x
        my -= self.y
        pressed = False
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                pressed = True

        for i in self.buttons:
            i.update(mx, my, pressed)

    def __set_answer(self, value):
        self.answer = value
        self.main_loop.exit()
