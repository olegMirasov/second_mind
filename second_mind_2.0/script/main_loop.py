import pygame as pg


class FPSViewer:
    def __init__(self, mainloop):
        self.clock = mainloop.clock
        self.screen = pg.display.get_surface()
        self.font = pg.font.Font(None, 50)

    def __call__(self, *args, **kwargs):
        FPS = self.clock.get_fps()
        FPS = str(round(FPS))
        FPS = self.font.render(FPS, False, (255, 255, 255), (0, 0, 0))
        self.screen.blit(FPS, (0, 0))
        pg.display.update(0, 0, 300, 50)


class NoFPSViewer:
    def __init__(self, *args, **kwargs):
        pass

    def __call__(self, *args, **kwargs):
        pass


class MainLoop:
    def __init__(self, fps=60, uf=None, df=None):
        self.__running = True
        self.clock = pg.time.Clock()
        self.fps = fps

        self.__update = uf
        self.__draw = df

        self.debug = False
        self.viewer = NoFPSViewer(self)

    def run(self):
        if not self.__draw or not self.__update:
            raise ValueError('You should add a draw and/or update function at MainLoop!')
        while self.__running:
            events = pg.event.get()
            self.__update(events)
            self.__draw()
            self.clock.tick(self.fps)

            if self.debug:
                self.viewer()

    def exit(self):
        self.__running = False

    def add_update_func(self, func):
        """
        :param func: Callable, waiting pg events argument
        :return: None
        """

        self.__update = func

    def add_draw_func(self, func):
        """
        :param func: Callable, not argument. Used for drawing logic in upper class
        :return: None
        """
        self.__draw = func

    def set_debug(self, value: bool):
        buf = {True: FPSViewer, False: NoFPSViewer}
        self.debug = value
        self.viewer = buf[self.debug](self)


