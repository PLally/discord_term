import curses
from .util import get_channel_names


class NavigationWindow:
    def __init__(self, parent, height, width, x, y):
        self.parent = parent
        self.win = parent.derwin(height, width, x, y)
        self.win.border()
        self.selected_item = 0
        self.items = []  # items must have a name attribute
        self.pointer = 0

    def get_item_name(self, i=None):
        i = self.pointer if i is None else i
        return self.items[i].name

    def refresh(self):
        self.parent.refresh()
        return self.win.refresh()

    def redraw(self):
        self.win.border()
        for i, item in enumerate(self.items):
            name = self.get_item_name(i)
            self.win.addstr(i+1, 1, name)

    def add_item(self, item):
        if len(self.items) > 50:
            return
        self.items.append(item)
        self.win.addstr(len(self.items), 1, item.name)

    def move(self, direction):
        prev = self.pointer
        self.pointer = max(0, min(len(self.items) - 1, self.pointer + direction))
        if self.pointer == prev:
            return

        self.win.addstr(self.pointer + 1, 1, self.get_item_name(), curses.A_UNDERLINE)
        self.win.addstr(prev+1, 1, self.get_item_name(prev))

    def on_input(self, char):
        if char == curses.KEY_DOWN:
            self.move(1)
        elif char == curses.KEY_UP:
            self.move(-1)


class ChannelNavigationWindow(NavigationWindow):
    def __init__(self, parent, height, width, x, y):
        self.channel_names = {}
        super().__init__(parent, height, width, x, y)

    def add_item(self, item):
        if len(self.items) > 50:
            return
        self.items.append(item)
        name = self.channel_names.get(item.id, item.name)
        self.win.addstr(len(self.items), 1, name)

    def set_guild(self, guild):
        self.items = []
        for chan in get_channel_names(guild):
            self.channel_names[chan[0].id] = chan[1]
            self.add_item(chan[0])

    def get_item_name(self, i=None):
        i = self.pointer if i is None else i
        return self.channel_names[self.items[i].id]
