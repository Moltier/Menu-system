import pygame
import time
import ctypes
from menu import Menu
from Audio import sound_lib


class UI:
    text_color = (255, 255, 255)

    def __init__(self, settings):
        self.SCREEN = None
        self.mode = None
        self.next_mode = None
        self.game_is_running = False
        self.smooth_transition = True
        self.transition_base_time = 0.15
        self.transition_start_time = None
        self.alpha = 255  # (0-255)

        self.black_image = None
        self.background_img = None
        self.background_img_name = None
        self.prev_background_img_name = None

        self.menus = {}

        # Other data
        self.width_div = 6
        self.height_div = 20
        self.w_diff_div = 20
        self.h_diff_div = 8
        self.font_size_div = 30
        self.menu_button_width = None
        self.menu_button_height = None
        self.menu_button_w_diff = None
        self.menu_button_h_dist = None
        self.menu_font_size = None

        # Other
        self.set_screen_mode(settings)
        self.create_objects(settings)

    def set_screen_mode(self, settings):
        resolution = settings.get_resolution()
        vsync = 1 if settings.vertical_sync == "True" else 0  # vertical sync isnt fully implemented in pygame

        if settings.full_screen == "True":
            ctypes.windll.user32.SetProcessDPIAware()  # this fixes a problem if correct aspect ratio is choosen, otherwise messes it up.
            flags = pygame.FULLSCREEN | pygame.HWSURFACE | pygame.DOUBLEBUF
        else:
            flags = pygame.HWSURFACE | pygame.DOUBLEBUF

        self.SCREEN = pygame.display.set_mode(resolution, flags, vsync=vsync)
        if self.mode and self.menus[self.mode].background_img_name:
            self.background_img = pygame.transform.scale(
                pygame.image.load(f"Images/{self.menus[self.mode].background_img_name}"), resolution).convert()
        self.black_image = pygame.transform.scale(
            pygame.image.load("Images/black.png"), resolution).convert()

        self.update_buttons(resolution, settings.get_font_multiplier())

    def update_buttons(self, resolution, font_multiplier):
        self.menu_button_width = resolution[0] / self.width_div
        self.menu_button_height = resolution[1] / self.height_div
        self.menu_button_w_diff = self.menu_button_width / self.w_diff_div
        self.menu_button_h_dist = self.menu_button_height / self.h_diff_div
        self.menu_font_size = int(resolution[1] / self.font_size_div / 100 * font_multiplier)

    def start_mode(self, mode, resolution):
        self.mode = mode
        self.background_img_name = self.menus[self.mode].background_img_name
        self.background_img = pygame.transform.scale(
            pygame.image.load(f"Images/{self.background_img_name}"), resolution).convert()

        if self.menus[self.mode].music_name:
            pygame.mixer.music.load(f"Audio/Music/{self.menus[self.mode].music_name}")
            pygame.mixer.music.set_volume(self.menus[self.mode].music_volume)
            pygame.mixer.music.play()

    def apply_volume(self, music_vol, sound_vol):
        # Musics use global and music specific volume. Sound effects dont.
        pygame.mixer.music.set_volume(self.menus[self.mode].music_volume / 10 * (int(music_vol) - 1))

        for sound_effect in sound_lib.sound_effects.values():
            if sound_effect.volume != int(sound_vol) - 1:
                sound_effect.set_volume(int(sound_vol) - 1)

    def handle_menu_transition(self, resolution):
        if self.next_mode:
            if self.alpha == 0:
                if self.menus[self.mode].music_name != self.menus[self.next_mode].music_name:
                    pygame.mixer.music.fadeout(1000)

            self.increase_alpha(resolution)
            self.SCREEN.blit(self.black_image, (0, 0))

            return True

        elif self.alpha > 0:
            if self.background_img:
                self.decrease_alpha()
                self.SCREEN.blit(self.black_image, (0, 0))

            else:
                # use images for every single object instead of rects and lines.
                # then i can just adjust them by set_alpha
                self.mode = self.next_mode
                self.update_background_img(resolution)
                self.next_mode = None

        return False

    def update_background_img(self, resolution):
        if self.menus[self.next_mode].background_img_name != self.background_img_name:
            self.background_img_name = self.menus[self.next_mode].background_img_name
            self.background_img = pygame.transform.scale(
                pygame.image.load(f"Images/{self.background_img_name}"), resolution).convert()

    def start_transition_timer(self):
        self.transition_start_time = time.time()

    def increase_alpha(self, resolution):
        timer = time.time() - self.transition_start_time
        percent = min(int(100 / self.transition_base_time * timer), 100)
        self.alpha = round(255 / 100 * percent)
        self.black_image.set_alpha(self.alpha)
        if self.alpha == 255:
            if self.menus[self.mode].music_name:
                if self.menus[self.mode].music_name != self.menus[self.next_mode].music_name:
                    pygame.mixer.music.load(f"Audio/Music/{self.menus[self.next_mode].music_name}")
                    pygame.mixer.music.set_volume(self.menus[self.next_mode].music_volume)
                    pygame.mixer.music.play()
            else:
                pygame.mixer.music.fadeout(1000)

            self.mode = self.next_mode
            self.update_background_img(resolution)
            self.next_mode = None
            self.transition_start_time = time.time()


    def decrease_alpha(self):
        timer = time.time() - self.transition_start_time
        percent = 100 - max(int(100 / self.transition_base_time * timer), 0)
        self.alpha = int(255 / 100 * percent)
        self.black_image.set_alpha(self.alpha)

    def get_options_data(self):
        if self.mode == "display":
            return [
                ["Full screen", self.menus["display menu buttons"].objects["full screen"].text],
                ["Resolution", self.menus["display menu buttons"].objects["resolution"].text],
                ["Vertical sync", self.menus["display menu buttons"].objects["vertical sync"].text],
                ["Framerate", self.menus["display menu buttons"].objects["framerate"].text],
                ["Text size", self.menus["display menu buttons"].objects["text size"].text]
            ]
        elif self.mode == "audio":
            return [
                ["Music volume", str(self.menus["audio menu bars"].objects["music"].level)],
                ["Sound volume", str(self.menus["audio menu bars"].objects["sound"].level)]
            ]
        else:
            print("Unknown ui.mode!")

    def create_objects(self, settings):
        resolution = settings.get_resolution()
        color = (0, 100, 0)
        border_color = (40, 40, 40)
        text_color = (255, 255, 255)

        # Main menu
        x = resolution[0] // 2
        y = resolution[1] // 2

        self.menus["main menu"] = Menu(
            x, y, self.menu_button_width, self.menu_button_height, obj_dist=self.menu_button_h_dist, placement="vertical",
            color=color, border_color=border_color, text_color=text_color,
            background_img_name="galaxy.png", music_name="Imperium Galactica 1.ogg", music_volume=0.1, font_size=self.menu_font_size)
        self.menus["main menu"].add_objects(parameters=(
            {
                "name": "new game",
                "type": "button",
                "string": "New Game"
            }, {
                "name": "options",
                "type": "button",
                "string": "Options"
            }, {
                "name": "exit",
                "type": "button",
                "string": "Exit"
            }))
        

        # Options menu
        self.menus["options"] = Menu(
            x, y, self.menu_button_width, self.menu_button_height, obj_dist=self.menu_button_h_dist, placement="vertical",
            color=color, border_color=border_color, text_color=text_color,
            background_img_name="ocean.png", music_name="Imperium Galactica 2.ogg", music_volume=0.1, font_size=self.menu_font_size)
        self.menus["options"].add_objects(parameters=(
            {
                "name": "display",
                "type": "button",
                "string": "Display"
            }, {
                "name": "audio",
                "type": "button",
                "string": "Audio"
            }, {
                "name": "controls",
                "type": "button",
                "string": "Key Bindings"
            }, {
                "name": "other",
                "type": "button",
                "string": "Other"
            }, {
                "name": "back",
                "type": "button",
                "string": "Back"
            }))


        # General options menu buttons
        x = resolution[0] / 2
        y = resolution[1] / 10 * 9

        self.menus["general options"] = Menu(
            x, y, self.menu_button_width, self.menu_button_height, obj_dist=self.menu_button_w_diff, placement="horizontal",
            color=color, border_color=border_color, text_color=text_color,
            font_size=self.menu_font_size)
        self.menus["general options"].add_objects(parameters=(
            {
                "name": "save",
                "type": "button",
                "string": "Save"
            }, {
                "name": "back",
                "type": "button",
                "string": "Back"
            }, {
                "name": "reset",
                "type": "button",
                "string": "Reset"
            }, {
                "name": "default",
                "type": "button",
                "string": "Default"
            }))


        # Display menu
        text_right_pos = 59  # percent of screen width
        buttons_left_pos = 60  # percent of screen width
        x = int(resolution[0] / 100 * text_right_pos) - self.menu_button_width
        y = resolution[1] // 2

        self.menus["display"] = Menu(
            x, y, self.menu_button_width, self.menu_button_height, obj_dist=self.menu_button_h_dist, placement="vertical",
            color=color, border_color=border_color, text_color=text_color,
            background_img_name="galaxy.png", music_name="Imperium Galactica 2.ogg", music_volume=0.1, font_size=self.menu_font_size, text_positioning="right")
        self.menus["display"].add_objects(parameters=(
            {
                "name": "full screen",
                "type": "text",
                "string": "Full screen"
            }, {
                "name": "resolution",
                "type": "text",
                "string": "Resolution"
            }, {
                "name": "vertical sync",
                "type": "text",
                "string": "Vertical sync"
            }, {
                "name": "framerate",
                "type": "text",
                "string": "Framerate"
            }, {
                "name": "text size",
                "type": "text",
                "string": "Text size"
            }))


        x = int(resolution[0] / 100 * buttons_left_pos)

        self.menus["display menu buttons"] = Menu(
            x, y, self.menu_button_width, self.menu_button_height, obj_dist=self.menu_button_h_dist, placement="vertical",
            color=color, border_color=border_color, text_color=text_color,
            font_size=self.menu_font_size, text_positioning="left", dinamic=True)
        self.menus["display menu buttons"].add_objects(parameters=(
            {
                "name": "full screen",
                "type": "button",
                "string": settings.full_screen
            }, {
                "name": "resolution",
                "type": "dropdown",
                "string": settings.resolution,
                "choices": ["640x360", "1280x720", "1280x800", "1360x768", "1440x900", "1600x900", "1920x1080", "1920x1200", "2560x1440"]
            }, {
                "name": "vertical sync",
                "type": "button",
                "string": settings.vertical_sync
            }, {
                "name": "framerate",
                "type": "dropdown",
                "string": settings.framerate,
                "choices": ["30", "60"]
            }, {
                "name": "text size",
                "type": "dropdown",
                "string": settings.text_size,
                "choices": ["80%", "90%", "100%", "110%", "120%"]
            }))


        # Audio menu
        text_right_pos = 59  # percent of screen width
        buttons_left_pos = 60  # percent of screen width
        x = int(resolution[0] / 100 * text_right_pos) - self.menu_button_width
        y = resolution[1] // 2

        self.menus["audio"] = Menu(
            x, y, self.menu_button_width, self.menu_button_height, obj_dist=self.menu_button_h_dist, placement="vertical",
            color=color, border_color=border_color, text_color=text_color,
            background_img_name="galaxy.png", music_name="Imperium Galactica 2.ogg", music_volume=0.1, font_size=self.menu_font_size, text_positioning="right")
        self.menus["audio"].add_objects(parameters=(
            {
                "name": "music",
                "type": "text",
                "string": "Music volume"
            }, {
                "name": "sound",
                "type": "text",
                "string": "Sound volume"
            }))


        x = int(resolution[0] / 100 * buttons_left_pos)

        self.menus["audio menu bars"] = Menu(
            x, y, self.menu_button_width, self.menu_button_height, obj_dist=self.menu_button_h_dist, placement="vertical",
            color=color, border_color=border_color, background_color=(50,50,50), grid_color=(0,0,0),
            font_size=self.menu_font_size, text_positioning="right", dinamic=True)
        self.menus["audio menu bars"].add_objects(parameters=(
            {
                "name": "music",
                "type": "bar",
                "level": int(settings.music_volume),
                "max level": 10
            }, {
                "name": "sound",
                "type": "bar",
                "level": int(settings.sound_volume),
                "max level": 10
            }))


        # Game
        x_pos_div = 8
        y_pos_div = 8
        x = resolution[0] - resolution[0] / x_pos_div
        y = resolution[1] - resolution[1] / y_pos_div

        self.menus["game"] = Menu(
            x, y, self.menu_button_width, self.menu_button_height, placement="vertical",
            color=color, border_color=border_color, text_color=text_color,
            background_img_name="galaxy.png", music_name="Imperium Galactica 2.ogg", music_volume=0.1, font_size=self.menu_font_size)


        # Controls
        x_pos_div = 8
        y_pos_div = 8
        x = resolution[0] - resolution[0] / x_pos_div
        y = resolution[1] - resolution[1] / y_pos_div

        self.menus["controls"] = Menu(
            x, y, self.menu_button_width, self.menu_button_height, placement="vertical",
            color=color, border_color=border_color, text_color=text_color,
            background_img_name="galaxy.png", music_name="Imperium Galactica 2.ogg", music_volume=0.1, font_size=self.menu_font_size)


        # Other menus
        self.menus["other"] = Menu(
            x, y, self.menu_button_width, self.menu_button_height, placement="vertical",
            color=color, border_color=border_color, text_color=text_color,
            background_img_name="galaxy.png", music_name="Imperium Galactica 2.ogg", music_volume=0.1, font_size=self.menu_font_size)
        self.menus["other"].add_objects(parameters=(
            {
                "name": "back",
                "type": "button",
                "string": "Back"
            },))

    def reset_borders(self):
        for button in self.menus["display menu buttons"].objects.values():
            if button.dinamic:
                button.modified = False
        for bar in self.menus["audio menu bars"].objects.values():
            if bar.dinamic:
                bar.modified = False

    def update_text_objects(self, settings):
        self.update_display_buttons(settings)
        self.update_other_texts(settings)

    def update_display_buttons(self, settings):
        self.menus["display menu buttons"].objects["full screen"].update_text(new_text=settings.full_screen, new_font_size=self.menu_font_size)
        self.menus["display menu buttons"].objects["resolution"].update_text(new_text=settings.resolution, new_font_size=self.menu_font_size)
        self.menus["display menu buttons"].objects["vertical sync"].update_text(new_text=settings.vertical_sync, new_font_size=self.menu_font_size)
        self.menus["display menu buttons"].objects["framerate"].update_text(new_text=settings.framerate, new_font_size=self.menu_font_size)
        self.menus["display menu buttons"].objects["text size"].update_text(new_text=settings.text_size, new_font_size=self.menu_font_size)

    def update_audio_levels(self, settings):
        self.menus["audio menu bars"].objects["music"].update_level(settings.music_volume)
        self.menus["audio menu bars"].objects["sound"].update_level(settings.sound_volume)

    def update_other_texts(self, settings):
        self.menus["main menu"].objects["new game"].update_text(new_font_size=self.menu_font_size)
        self.menus["main menu"].objects["options"].update_text(new_font_size=self.menu_font_size)
        self.menus["main menu"].objects["exit"].update_text(new_font_size=self.menu_font_size)

        self.menus["options"].objects["display"].update_text(new_font_size=self.menu_font_size)
        self.menus["options"].objects["audio"].update_text(new_font_size=self.menu_font_size)
        self.menus["options"].objects["controls"].update_text(new_font_size=self.menu_font_size)
        self.menus["options"].objects["other"].update_text(new_font_size=self.menu_font_size)
        self.menus["options"].objects["back"].update_text(new_font_size=self.menu_font_size)

        self.menus["general options"].objects["save"].update_text(new_font_size=self.menu_font_size)
        self.menus["general options"].objects["back"].update_text(new_font_size=self.menu_font_size)
        self.menus["general options"].objects["reset"].update_text(new_font_size=self.menu_font_size)
        self.menus["general options"].objects["default"].update_text(new_font_size=self.menu_font_size)

        self.menus["display"].objects["full screen"].update_text(new_font_size=self.menu_font_size)
        self.menus["display"].objects["resolution"].update_text(new_font_size=self.menu_font_size)
        self.menus["display"].objects["vertical sync"].update_text(new_font_size=self.menu_font_size)
        self.menus["display"].objects["framerate"].update_text(new_font_size=self.menu_font_size)
        self.menus["display"].objects["text size"].update_text(new_font_size=self.menu_font_size)

        self.menus["audio"].objects["music"].update_text(new_font_size=self.menu_font_size)
        self.menus["audio"].objects["sound"].update_text(new_font_size=self.menu_font_size)

        self.menus["other menu"].objects["back"].update_text(new_font_size=self.menu_font_size)
