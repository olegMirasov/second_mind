import pygame as pg
from script.main_loop import MainLoop
from script.main_menu import MainMenu


class App:
    def __init__(self):
        pg.init()
        info = pg.display.Info()
        self.w = info.current_w - 100
        self.h = info.current_h - 100
        self.screen = pg.display.set_mode((self.w, self.h))

        self.main_loop = MainLoop(fps=30)

    def start(self):
        MainMenu(self)

    def update(self, events):
        for i in events:
            if i.type == pg.QUIT:
                self.main_loop.exit()

    def draw(self):
        self.screen.fill((25, 250, 25))
        pg.display.update()


if __name__ == '__main__':
    my_app = App()
    my_app.start()

    print('[INFO] Program is finished')
