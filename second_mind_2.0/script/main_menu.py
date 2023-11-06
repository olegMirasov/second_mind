import pygame as pg
from script.main_loop import MainLoop
from script.use_tools.buttons import DefButton
from script.use_tools.message import OkMessage
from settings import MENU_COLOR
from script.new_node_window import NewNode


class MainMenu:
    def __init__(self, app):
        self.app = app
        self.main_loop = MainLoop(uf=self.update, df=self.draw, fps=0)
        self.main_loop.set_debug(True)

        # create buttons
        # find size buttons
        dw = self.app.w // 10
        w = (self.app.w - 4 * dw) // 3

        dh = self.app.h // 3
        h = dh

        # create buttons
        new_note = DefButton(dw, dh, w, h, 'Новая заметка', func=self.__new_note)
        search = DefButton(dw * 2 + w, dh, w, h, 'Поиск', func=self.__search_note)
        mesh = DefButton(dw*3 + 2*w, dh, w, h, 'Сетка', func=self.__show_mesh)

        ds = self.app.w // 12
        exit_button = DefButton(self.app.w - 2 * ds - 40, 40, 2 * ds, ds, 'Выход', func=self.main_loop.exit)
        self.buttons = [new_note, search, mesh, exit_button]

        self.main_loop.run()

    def update(self, events):
        pressed = False
        for i in events:
            if i.type == pg.QUIT:
                self.main_loop.exit()

            if i.type == pg.MOUSEBUTTONDOWN and i.button == 1:
                pressed = True

        mx, my = pg.mouse.get_pos()
        flag = False
        for i in self.buttons[::-1]:
            if not flag:
                flag = i.update(mx, my, pressed)
            if flag:
                i.update(mx, my, False)

    def draw(self):
        self.app.screen.fill(MENU_COLOR)
        for i in self.buttons:
            i.draw(self.app.screen)

        pg.display.update()

    def __new_note(self):
        NewNode(self.app).main_loop.run()

    def __search_note(self):
        OkMessage('Раздел в разработке', timer=2).run()

    def __show_mesh(self):
        OkMessage('Раздел в разработке', timer=2).run()
