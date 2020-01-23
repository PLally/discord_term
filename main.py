import curses
import discord
import sys
from lib import NavigationWindow, ChannelNavigationWindow, MessageArea


TOKEN = open("token").read()


class TerminalClient(discord.Client):
    def __init__(self, stdscr, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.screen = stdscr
        self.guild_nav = None
        self.channel_nav = None
        self.message_area = None
        self.init_windows()
        self.current_nav = None
        curses.curs_set(False)
    
    @property
    def height(self):
        height, width = self.screen.getmaxyz()
        return height

    @property
    def width(self):
        height, width = self.screen.getmaxyz()
        return width
    
    def init_windows(self):
        self.screen.clear()
        height, width = self.screen.getmaxyx()
        self.guild_nav = NavigationWindow(self.screen, height-2, int(width*0.20)-2, 1, 1)
        self.channel_nav = ChannelNavigationWindow(self.screen, height-2, int(width*0.20)-2, 1, 1)
        self.message_area = MessageArea(self.screen, height-2, int(width*0.70), 1, int(width*0.20)+1)

    async def on_ready(self):
        for i, guild in enumerate(self.guilds):
            self.guild_nav.add_item(guild)

        self.guild_nav.refresh()

        self.guild_nav.refresh()
        self.current_nav = self.guild_nav
        self.loop.add_reader(sys.stdin, self.on_input)

    def on_input(self):
        char = self.screen.getch()

        if char == curses.KEY_RIGHT and self.current_nav == self.guild_nav:
            self.current_nav = self.channel_nav
            self.guild_nav.win.erase()
            guild = self.guild_nav.items[self.guild_nav.pointer]
            self.channel_nav.set_guild(guild)
            self.current_nav.redraw()
        elif char == curses.KEY_LEFT and self.current_nav == self.channel_nav:
            self.current_nav = self.guild_nav
            self.channel_nav.win.erase()
            self.current_nav.redraw()
        elif char == curses.KEY_RIGHT and self.current_nav == self.channel_nav:
            channel = self.channel_nav.items[self.channel_nav.pointer]

            async def update_msgs(message_area, channel):
                message_area.messages = await channel.history(limit=100).flatten()
                message_area.redraw()
                message_area.win.refresh()
            if isinstance(channel, discord.TextChannel):
                self.loop.create_task(update_msgs(self.message_area, channel))
        else:
            self.current_nav.on_input(char)
        self.current_nav.refresh()


def main(stdscr=None):
    client = TerminalClient(stdscr)

    client.run(TOKEN, bot=True)
    curses.endwin()


curses.wrapper(main)
