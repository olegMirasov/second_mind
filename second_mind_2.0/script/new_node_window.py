import pygame as pg
from script.main_loop import MainLoop
from script.use_tools.label import ManyLabel
from script.use_tools.buttons import DefButton
from script.use_tools.message import OkMessage, YesNoMessage
from script.use_tools.timer import Timer, FuncTimer
from settings import NEW_NODE_COLOR, WRITE_WINDOW_COLOR, FONT, TEXT_COLOR, ACTIVE_WINDOW_COLOR


class Node:
    def __init__(self, prev=None, next=None):
        self.prev = prev
        self.next = next


class ListCursor:
    STATUS_VALUES = ('ahead', 'behind')

    def __init__(self, parent):
        self.parent = parent
        self.__status = 'behind'

    def reset(self):
        self.status = 'behind'

    @property
    def status(self):
        return self.__status

    @status.setter
    def status(self, status):
        if status in self.STATUS_VALUES:
            self.__status = status


class MyList:
    def __init__(self):
        self.first = None
        self.last = None
        self.active = None

        self.cursor = ListCursor(self)

    # === ADD LOGIC ===
    def add(self, node: Node):
        if self.is_empty():
            self.__add_first(node)
            return
        if self.active == self.last:
            self.__add_last(node)
            return
        if self.active == self.first:
            self.__add_second(node)
            return
        self.__add_middle(node)

    def __add_first(self, node: Node):
        self.first = self.last = self.active = node
        self.cursor.reset()

    def __add_last(self, node: Node):
        if self.cursor.status == 'behind':
            node.prev = self.last
            self.last.next = node
            self.last = self.active = node
            return

        active = self.last.prev
        if active:
            self.cursor.status = 'ahead'
            self.__add_middle(node)
        else:
            self.last.prev = self.first = node
            node.next = self.last
            self.active = node
            self.cursor.reset()

    def __add_second(self, node: Node):
        if self.cursor.status == 'ahead':
            self.first.prev = node
            node.next = self.first
            self.first = node
            self.active = node
            self.cursor.reset()
            return

        active = self.first.next
        if active:
            self.cursor.status = 'behind'
            self.__add_middle(node)
        else:
            self.first.next = node
            node.prev = self.first
            self.last = node
            self.active = node

    def __add_middle(self, node):
        prev = self.active.prev
        next = self.active.next
        if self.cursor.status == 'behind':
            node.next = next
            node.prev = self.active
            next.prev = node
            self.active.next = node
            self.active = node
        else:
            node.prev = prev
            node.next = self.active
            prev.next = node
            self.active.prev = node
            self.active = node
            self.cursor.reset()

    # === REMOVE LOGIC ===
    def remove(self):
        if self.is_empty():
            return
        if self.active == self.last:
            self.__remove_last()
            return
        if self.active == self.first:
            self.__remove_first()
            return
        self.__remove_middle()

    def __remove_first(self):
        if self.cursor.status == 'ahead':
            return
        if self.last == self.first:
            self.reset_list()
            return
        next = self.first.next
        next.prev = None
        self.active = self.first = next
        self.cursor.status = 'ahead'

    def __remove_last(self):
        flag = self.cursor.status == 'behind'

        if self.last == self.first:
            if flag:
                self.reset_list()
            return

        if flag:
            prev = self.last.prev
            prev.next = None
            self.last.prev = None
            self.active = self.last = prev
        else:
            self.active = self.last.prev
            self.cursor.status = 'behind'
            self.__remove_middle()

    def __remove_middle(self):
        remove_obj = self.active
        if self.cursor.status == 'ahead':
            remove_obj = self.active.prev

        if remove_obj == self.first:
            self.cursor.status = 'behind'
            self.active = self.first
            self.__remove_first()
            return

        # try
        _next = remove_obj.next
        _prev = remove_obj.prev
        _next.prev = _prev
        _prev.next = _next
        self.active = _prev

    def lefter(self, cursor=True):
        if self.is_empty():
            return
        if self.active == self.first:
            if cursor:
                self.cursor.status = 'ahead'
            return

        prev = self.active.prev
        if prev:
            self.active = prev

    def righter(self, cursor=True):
        if self.is_empty():
            return
        if self.active == self.last:
            if cursor:
                self.cursor.status = 'behind'
            return

        _next = self.active.next
        if _next:
            self.active = _next

    def is_empty(self):
        if self.first:
            return False
        return True

    def reset_list(self):
        self.first = self.last = self.active = None
        self.cursor.reset()


class DefaultChar:
    AA = True  # antializing
    COLOR = TEXT_COLOR
    BG = None  # (255, 0, 0)
    DT = 0

    def __init__(self, x, y, parent, char):
        self.parent = parent
        self.char = char

        self.surface = self.parent.font.render(self.char, self.AA, self.COLOR, self.BG)
        # pg.draw.rect(pg.display.get_surface(), (255, 0, 0), self.surface.get_rect(), 1)

        self.rect = self.surface.get_rect()
        self.rect.topleft = (x, y)

    def draw(self, sc: pg.Surface):
        sc.blit(self.surface, self.rect)

    def get_my_params(self):
        return self.rect.topleft

    def get_next_params(self):
        w = self.rect.w
        x = self.rect.left
        y = self.rect.top
        return x + w + self.DT, y

    def set_new_coords(self, x, y):
        self.rect.topleft = (x, y)


class Char(DefaultChar, Node):
    def __init__(self, x, y, parent, char):
        DefaultChar.__init__(self, x, y, parent, char)
        Node.__init__(self)


class Cursor(DefaultChar):
    def __init__(self, x, y, parent):
        super().__init__(x, y, parent, ' ')
        self.surface.fill((0, 0, 0, 0))
        pg.draw.line(self.surface, TEXT_COLOR, (0, 0), (0, self.rect.height), 2)
        self.timer = Timer(0.5)
        self.timer.run()

        self.active = True

    def draw(self, sc):
        if self.active:
            super().draw(sc)

    def update(self):
        if self.timer():
            self.active = not self.active
            # self.timer.reebot()


class Row(MyList, Node):
    def __init__(self, x, y, w, h, parent: 'RowCombiner'):
        MyList.__init__(self)
        Node.__init__(self)
        self.rect = pg.Rect(x, y, w, h)
        self.parent = parent
        self.font = self.parent.font
        self.writer = True
        self.activate()

        self.delta_x = self.parent.delta_x
        self.delta_y = self.parent.delta_y
        self.surface = pg.Surface(self.rect.size).convert_alpha()
        self.surface.fill((0, 0, 0, 0))

        self.fix_timer = FuncTimer(self.__fix_char_position, sec=1).run()

        self.side_dict = {'left': self.lefter, 'right': self.righter}
        self.key_dict = self.__get_key_dict()
        self.char_indent = 0

    def __get_key_dict(self):
        temp = {42: self.delete_char,
                40: self.new_line,
                76: self.remove_right,
                79: lambda: self.move(side='right'),
                80: lambda: self.move(side='left'),
                82: lambda: self.parent.change_move_flag('up'),
                81: lambda: self.parent.change_move_flag('down'),
                255: lambda: None, }
        return temp

    def activate(self):
        self.writer = True
        self.parent.i_active(self)
        self.update_char_cursor()

    def deactivate(self):
        self.writer = False

    def draw(self, sc: pg.Surface):
        # self.surface.fill((0, 0, 255))
        buf = self.first
        while buf:
            buf.draw(sc)
            buf = buf.next
        # sc.blit(self.surface, self.rect)

    def set_row_position(self, x, y):
        self.char_indent = y

    def update(self, events):
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                mx -= self.delta_x
                my -= self.delta_y
                if self.rect.collidepoint(mx, my):
                    self.activate()
                    self.parent.set_active_row(self)
        if not self.writer:
            return
        for event in events:
            if event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = event.pos
                mx -= self.delta_x
                my -= self.delta_y
                self.set_active_char_by_coord(mx, my)
            if event.type == pg.KEYDOWN:
                if event.scancode in self.key_dict.keys():
                    self.key_dict[event.scancode]()
                else:
                    x, y = self.get_next_coord()
                    char = Char(x, y, self, event.unicode)
                    self.add(char)
                self.__fix_char_position()

        self.update_char_cursor()

        # self.fix_timer()

    def set_active_char_by_coord(self, mx, my=0):
        if self.is_empty():
            return
        temp: Char = self.first
        find_flag = True
        while temp:
            if not temp.rect.left <= mx <= temp.rect.right:
                temp = temp.next
                continue

            self.active = temp
            find_flag = False
            if mx - temp.rect.left < temp.rect.right - mx:
                self.cursor.status = 'ahead'
            else:
                self.cursor.status = 'behind'
            break

        if find_flag:
            self.active = self.last
            self.cursor.status = 'behind'

    def remove_right(self):
        if self.last == self.active and self.cursor.status == 'behind':
            return
        self.righter()
        self.delete_char()

    def __check_out(self):
        if self.last:
            if self.last.rect.right > self.parent.end_row:
                self.__rec_row()

    def __rec_row(self):
        pass

    def update_char_cursor(self):
        if self.is_empty():
            result = self.__get_my_start_coord()
        elif self.cursor.status == 'behind':
            result = self.active.get_next_params()
        else:
            result = self.active.get_my_params()

        self.parent.char_cursor.set_new_coords(*result)

    def move(self, side):
        self.side_dict[side]()
        self.update_char_cursor()

    def delete_char(self):
        self.remove()
        self.update_char_cursor()
        if self.is_empty():
            self.parent.remove_row(self)

    def __fix_char_position(self):
        buf: Char = self.first
        next_pos = self.__get_my_start_coord()
        while buf:
            buf.set_new_coords(*next_pos)
            next_pos = buf.get_next_params()
            buf = buf.next
        self.update_char_cursor()

    def new_line(self):
        self.parent.add_new_line = True

    def clean(self):
        self.reset_list()
        self.parent.char_cursor.set_new_coords(*self.__get_my_start_coord())

    def __get_my_start_coord(self):
        x, y = self.rect.topleft
        #x -= self.parent.padding
        #y -= self.parent.padding
        return x, y

    def get_next_coord(self):
        if not self.active:
            return self.__get_my_start_coord()

        if self.cursor.status == 'behind':
            result = self.active.get_next_params()
        else:
            result = self.active.get_my_params()
        return result

    def get_next_row_coord(self):
        return self.rect.x, self.rect.bottom


class RowCombiner(MyList):
    def __init__(self, parent):
        MyList.__init__(self)
        self.parent = parent
        self.font_size = parent.font_size
        self.rect = self.parent.rect

        self.delta_x = self.rect.x
        self.delta_y = self.rect.y

        self.padding = 20
        self.end_row = self.rect.right - self.padding
        self.row_width = self.rect.width - 2 * self.padding

        self.font = pg.font.Font(FONT, self.font_size)

        self.char_cursor = Cursor(self.padding, self.padding, self)
        self.row_indent: float = 0.3
        self.row_height = self.char_cursor.rect.height*(1 + self.row_indent)
        self.new_line()

        self.add_new_line = False
        self.move_flag = False
        self.move_dict = {'up': self.lefter, 'down': self.righter, False: lambda: None}

    def new_cursor_coord(self, params):
        self.char_cursor.set_new_coords(*params.values())

    def i_active(self, row):

        buf: Row = self.first
        while buf:
            if buf != row:
                buf.deactivate()
            buf = buf.next

    def set_active_row(self, row):
        self.active = row

    def change_move_flag(self, direction: str):
        # direction in ('up', 'down')
        self.move_flag = direction

    def lefter(self, *args, **kwargs):
        mx, my = self.char_cursor.rect.center
        super().lefter(cursor=False)
        self.active.activate()
        self.active.set_active_char_by_coord(mx, my)

    def righter(self, *args, **kwargs):
        mx, my = self.char_cursor.rect.center
        super().righter(cursor=False)
        self.active.activate()
        self.active.set_active_char_by_coord(mx, my)

    def __fix_row_position(self):
        pos = self.padding, self.padding
        temp: Row = self.first
        while temp:
            temp.rect.topleft = pos
            pos = temp.get_next_row_coord()
            temp = temp.next

    def remove_row(self, row):
        self.remove()
        if self.is_empty():
            self.new_line()
        self.active.activate()
        self.active.set_active_char_by_coord(2000)  # for char cursor move to the end
        self.__fix_row_position()

    def update(self, events):
        self.char_cursor.update()

        self.add_new_line = False
        self.move_flag = False

        buf: Row = self.first
        while buf:
            buf.update(events)
            buf = buf.next

        if self.add_new_line:
            self.new_line()

        self.move_dict[self.move_flag]()
        self.__fix_row_position()

    def new_line(self):
        if self.is_empty():
            params = self.padding, self.padding
        else:
            params = self.active.get_next_row_coord()

        row = Row(*params, self.row_width, self.row_height, self)
        self.add(row)
        self.__fix_row_position()

    def clean(self):
        self.reset_list()
        self.new_line()
        self.char_cursor.set_new_coords(self.padding, self.padding)

    def draw(self, sc):
        buf: Row = self.first
        while buf:
            buf.draw(sc)
            buf = buf.next

    def draw_cursor(self, sc):
        self.char_cursor.draw(sc)


class WriteWindow:
    def __init__(self, x, y, w, h, parent, font_size=34):
        self.rect = pg.Rect(x, y, w, h)
        self.parent = parent
        self.surface = pg.Surface((w, h))
        self.active = False
        self.font_size = font_size
        self.row_combiner = RowCombiner(self)

        # try

        # debag
        self.surface.fill(WRITE_WINDOW_COLOR)
        self.render_surface = pg.Surface(self.surface.get_size())

    def __call__(self, x, y, pressed):
        return self.rect.collidepoint(x, y) and pressed

    def update(self, x, y, pressed, events):
        if self(x, y, pressed):
            self.i_active()
        if not self.active:
            return
        self.row_combiner.update(events)

    def draw(self, sc: pg.Surface):
        if not self.active:
            sc.blit(self.surface, self.rect)
            return
        # debag
        self.render_surface.fill(ACTIVE_WINDOW_COLOR)  # if not self.active else ACTIVE_WINDOW_COLOR)
        self.row_combiner.draw(self.render_surface)
        self.row_combiner.draw_cursor(self.render_surface)
        # self.surface.blit(self.render_surface, (0, 0))
        '''if self.active:
            self.row_combiner.draw_cursor(self.render_surface)'''
        sc.blit(self.render_surface, self.rect)

    def draw_units(self):
        pass

    def i_active(self):
        self.active = True
        self.parent.set_active(self)
        self.surface.fill(WRITE_WINDOW_COLOR)

    def disactivate(self):
        self.active = False
        self.row_combiner.draw(self.surface)

    def clean(self):
        self.row_combiner.clean()
        self.surface.fill(WRITE_WINDOW_COLOR)


class NewNode:
    def __init__(self, app):
        self.app = app
        self.main_loop = MainLoop(uf=self.update, df=self.draw, fps=0)
        self.main_loop.set_debug(True)

        # create write windows
        dt = 20
        height_write_area = self.app.h - dt * 4 - self.app.h * 0.15
        width_write_window = self.app.w // 3 * 2

        height_title = int(height_write_area * 0.3)
        height_text = int(height_write_area * 0.6)
        height_tags = int(height_write_area * 0.1)

        title_font_size = int(self.app.h / 15)
        other_font_size = int(self.app.h / 20)

        self.title = WriteWindow(dt, dt, width_write_window, height_title, self, font_size=title_font_size)
        self.text = WriteWindow(dt, dt * 2 + self.title.rect.h, width_write_window,
                                height_text, self, font_size=other_font_size)
        self.tags = WriteWindow(dt, dt * 3 + self.title.rect.h + self.text.rect.h,
                                width_write_window, height_tags, self, font_size=other_font_size)

        self.write_windows = (self.title, self.text, self.tags)

        # create labels
        font_height = self.app.h // 30
        label_width = self.app.w // 4

        title_label = ManyLabel(self.title.rect.right + dt, self.title.rect.top,
                                width=label_width,
                                text='Введите заголовок. Он должен отражать суть заметки',
                                font_size=font_height)

        text_label = ManyLabel(self.text.rect.right + dt, self.text.rect.top,
                               width=label_width,
                               text='Напишите заметку. Заметка должна быть короткой, но емкой',
                               font_size=font_height)

        tags_label = ManyLabel(self.tags.rect.right + dt, self.tags.rect.top,
                               width=label_width,
                               text='Добавте тэги через запятую, например: "уроки, йога, улица"',
                               font_size=font_height,)

        self.labels = (title_label, text_label, tags_label)

        # create buttons
        db = self.app.h * 0.12
        button_top = self.tags.rect.bottom + dt * 2
        button_w = db * 1.5

        save_button = DefButton(dt, button_top, button_w, db, 'Сохранить', func=self.save_note)
        clean_button = DefButton(dt*10 + button_w, button_top, button_w, db, 'Очистить', func=self.clean_note)
        cancel_button = DefButton(button_w * 2 + dt * 11, button_top, button_w, db, 'Отменить', func=self.cancel_note)

        self.buttons = (save_button, clean_button, cancel_button)

    def update(self, events):
        mouse_pressed = False
        mx, my = pg.mouse.get_pos()
        for i in events:
            if i.type == pg.MOUSEBUTTONDOWN:
                if i.button == 1:
                    mouse_pressed = True
            if i.type == pg.QUIT:
                self.cancel_note()

        for i in self.write_windows:
            i.update(mx, my, mouse_pressed, events)

        for i in self.buttons:
            i.update(mx, my, mouse_pressed)

    def draw(self):
        self.app.screen.fill(NEW_NODE_COLOR)
        for i in self.write_windows:
            i.draw(self.app.screen)
        for i in self.labels:
            i.draw(self.app.screen)
        for i in self.buttons:
            i.draw(self.app.screen)
        pg.display.update()

    def set_active(self, active_object):
        for i in self.write_windows:
            if i != active_object:
                i.disactivate()

    def save_note(self):
        res_ok = 'Заметка сохранена'
        res_fail = 'Что то пошло не так. Попробуйте еще раз'
        OkMessage(res_ok, timer=2).run()
        self.main_loop.exit()

    def clean_note(self):
        clean = YesNoMessage('Вы уверены что хотите очистить заметку? Все несохраненные данные будут утеряны').run()
        if clean:
            for i in self.write_windows:
                i.clean()

    def cancel_note(self):
        cancel = YesNoMessage('Вы уверены что хотите выйти? Все несохраненные данные будут утеряны').run()
        if cancel:
            self.main_loop.exit()
