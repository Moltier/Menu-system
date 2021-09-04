from object import Object, Button, Dropdown, Bar


class Menu:
    def __init__(self, x, y, w, h, obj_dist=0, placement="Vertical", color=None, border_color=None,
                 text_color=None, dropdown_area_color=None, background_color=None, grid_color=None,
                 background_img_name=None, music_name=None, music_volume=0,
                 font_size=None, text_positioning="center", dinamic=False):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.obj_dist = obj_dist
        self.color = color
        self.border_color = border_color
        self.text_color = text_color
        self.dropdown_area_color = dropdown_area_color
        self.background_color = background_color
        self.grid_color = grid_color
        self.objects = {}
        self.background_img_name = background_img_name
        self.music_name = music_name
        self.music_volume = music_volume
        self.font_size = font_size
        self.placement = placement
        self.text_positioning = text_positioning
        self.dinamic = dinamic

        self.objects = {}

    def add_objects(self, parameters):
        pos_multiplier = -((len(parameters) - 1) / 2)

        for parameter in parameters:
            x = self.x if self.placement == "vertical" else self.x + (self.w + self.obj_dist) * pos_multiplier
            y = self.y if self.placement == "horizontal" else self.y + (self.h + self.obj_dist) * pos_multiplier
            pos_multiplier += 1

            if parameter["type"] == "object":
                self.objects[parameter["name"]] = Object(
                    x, y, self.w, self.h, color=self.color, border_color=self.border_color,
                    image_name=parameter["image name"], image_alpha=parameter["image alpha"])

            elif parameter["type"] == "text":
                self.objects[parameter["name"]] = Button(
                    x, y, self.w, self.h, text_color=self.text_color,
                    text=parameter["string"], font_size=self.font_size, text_positioning=self.text_positioning,
                    image_name=parameter["image name"], image_alpha=parameter["image alpha"])

            elif parameter["type"] == "button":
                self.objects[parameter["name"]] = Button(
                    x, y, self.w, self.h, dinamic=self.dinamic,
                    color=self.color, border_color=self.border_color, text_color=self.text_color,
                    text=parameter["string"], font_size=self.font_size, text_positioning=self.text_positioning,
                    image_name=parameter["image name"], image_alpha=parameter["image alpha"])

            elif parameter["type"] == "dropdown":
                self.objects[parameter["name"]] = Dropdown(
                    x, y, self.w, self.h, dinamic=self.dinamic, color=self.color, border_color=self.border_color,
                    text_color=self.text_color, dropdown_area_color=self.dropdown_area_color,
                    text=parameter["string"],
                    choices=parameter["choices"],
                    font_size=self.font_size, text_positioning="left")

            elif parameter["type"] == "bar":
                self.objects[parameter["name"]] = Bar(
                    x, y, self.w, self.h, dinamic=self.dinamic, color=self.color, border_color=self.border_color,
                    background_color=self.background_color, grid_color=self.grid_color,
                    level=parameter["level"], max_level=parameter["max level"])
