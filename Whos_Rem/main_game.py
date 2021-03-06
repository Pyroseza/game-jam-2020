import arcade
import pyautogui
from main import *


class Main:

    size = pyautogui.size()

    def __init__(self):
        self.settings = Settings(self)
        self.menu = MainMenu(self)
        self.song_selection = SongSelection(self)
        self.window = arcade.Window(
            self.width, self.height,
            title="3 Strings", fullscreen=False, update_rate=1/32)
        self.play_screen = GameScreen(self)

    @property
    def brightness(self):
        return self.settings.brightness

    @property
    def volume(self):
        return self.settings.volume

    @property
    def width(self):
        return self.size[0]

    @property
    def height(self):
        return self.size[1]


if __name__ == "__main__":
    main = Main()
    main.window.show_view(main.menu)
    arcade.run()
