import csv


class Settings:
    grid_proportion_range = range(50, 101)

    def_vertical_sync = "True"
    def_framerate = "60"
    def_general_text_size = "100%"

    def_music_volume = "6"
    def_sound_volume = "6"

    # def_grid_proportion = "100"

    def __init__(self):
        # self.grid_proportion = 100
        self.prev_full_screen = None
        self.prev_resolution = None
        self.prev_general_text_size = None
        self.full_screen = None
        self.resolution = None
        self.vertical_sync = None  # doesnt do anything atm
        self.framerate = None
        self.general_text_size = None

        # Audio
        self.music_volume = None
        self.sound_volume = None

        for file_name in ("display", "audio"):
            self.load_data(file_name)

    # @property
    # def grid_proportion(self):
    #     return self._grid_proportion
    #
    # @grid_proportion.setter
    # def grid_proportion(self, grid_proportion):
    #     if grid_proportion in Settings.grid_proportion_range:
    #         self._grid_proportion = grid_proportion
    #     else:
    #         raise ValueError('Proportion is out of range (50-100)!')

    def load_data(self, file_name):
        with open(f"Data/Settings/{file_name}.csv", 'r') as csv_file:
            for name, value in csv.reader(csv_file):
                self.set_data(name, value)
                self.set_prev_data(name, value)

    def get_resolution(self):
        return [int(x) for x in self.resolution.split('x')]

    def get_font_multiplier(self, type):
        if type == "general":
            return int(self.general_text_size[:-1])

    def reset_to_default(self, options_menu):
        if options_menu == "display":
            self.vertical_sync = Settings.def_vertical_sync
            self.framerate = Settings.def_framerate
            self.general_text_size = Settings.def_general_text_size
        elif options_menu == "audio":
            self.music_volume = Settings.def_music_volume
            self.sound_volume = Settings.def_sound_volume

    def save(self, file_name, settings_data):
        with open(f"Data/Settings/{file_name}.csv", 'w', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            for line in settings_data:
                name, value = line
                csv_writer.writerow(line)
                self.set_data(name, value)

    def set_data(self, name, value):
        if name == "Full screen":
            self.full_screen = value
        elif name == "Resolution":
            self.resolution = value
        elif name == "Vertical sync":
            self.vertical_sync = value
        elif name == "Framerate":
            self.framerate = value
        elif name == "General text size":
            self.general_text_size = value

        elif name == "Music volume":
            self.music_volume = value
        elif name == "Sound volume":
            self.sound_volume = value

    def set_prev_data(self, name, value):
        if name == "Full screen":
            self.prev_full_screen = value
        elif name == "Resolution":
            self.prev_resolution = value
        elif name == "Gereral text size":
            self.prev_general_text_size = value