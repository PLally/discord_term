import discord


class MessageArea:
    def __init__(self, parent, height, width, y, x):
        self.parent = parent
        self.win = parent.derwin(height, width, y, x)
        self.messages = []
        self.position = 0

    def redraw(self):
        self.win.erase()
        height, width = self.win.getmaxyx()

        row = 0
        for i, msg in enumerate(self.messages):
            content = f"{msg.author}: {msg.content}"
            for line in content.split("\n"):
                self.win.addstr(height - (row + 2), 1, line[:width - 5])
                row += 1
                if row - self.position > height - 5:
                    return

    def on_message(self, message):
        if not isinstance(message, discord.Message):
            return
        self.messages.insert(0, f"{message.author}: {message.clean_content}"[:30].replace("\n", " \\n ").ljust(30))
        self.redraw()

