import pygame
from Audio import sound_lib


class Object:
    modified_color = (255, 127, 80)

    def __init__(self, x, y, w, h, image_name=None, image_alpha=None, color=None, border_color=None):
        self.rect = pygame.Rect(0, 0, w, h)
        self.rect.center = (x, y)
        self.color = color
        self.dark_color = [int(n*0.25) for n in self.color] if self.color else None
        self.border_color = border_color
        self.highlighted_color = [int(n * 1.5) if n * 1.5 <= 255 else int(n * 0.25) for n in self.color] if self.color else None
        self.modified = False

        self.image_name = image_name
        self.image_alpha = image_alpha
        self.image = None
        self.update_img(self.image_name, self.image_alpha)

    def update_img(self, image_name=None, image_alpha=None):
        if image_name:
            self.image_name = image_name
            self.image = pygame.transform.scale(pygame.image.load(f"Images/{self.image_name}"), (self.rect.w, self.rect.h)).convert()

        if image_alpha:
            self.image_alpha = image_alpha
            self.image.set_alpha(self.image_alpha)

    def draw(self, SCREEN, y_scroll=0, rect_highlight=False, dark=False):
        rect = self.rect.copy()
        rect.y += y_scroll
        if dark:
            pygame.draw.rect(SCREEN, self.dark_color, rect)
        elif rect_highlight:
            pygame.draw.rect(SCREEN, self.highlighted_color, rect)

        if self.color:
            pygame.draw.rect(SCREEN, self.color, rect)
        elif self.image_name:
            SCREEN.blit(self.image, rect)

        if self.modified:
            pygame.draw.rect(SCREEN, Object.modified_color, rect, width=2)
        elif self.border_color:
            pygame.draw.rect(SCREEN, self.border_color, rect, width=2)


class Button(Object):
    font_family = "comicsansms"

    def __init__(self, x, y, w, h, dinamic=False, image_name=None, image_alpha=None, color=None, border_color=None,
                 text="", text_color=(255, 255, 255),
                 font_size=20, text_positioning="center"):
        super().__init__(x, y, w, h, image_name, image_alpha, color, border_color)
        self.dinamic = dinamic
        self.active = True
        self.down = False
        self.font_size = font_size
        self.font = pygame.font.SysFont(Button.font_family, self.font_size)
        self.text = text
        self.text_color = text_color
        self.text_dark_color = [int(x * 0.25) for x in self.text_color]
        self.rendered_text = self.font.render(self.text, True, self.text_color)
        self.text_highlight_color = (0,255,0)
        self.highlighted_rendered_text = self.font.render(self.text, True, self.text_highlight_color)
        self.dark_rendered_text = self.font.render(self.text, True, self.text_dark_color)

        self.text_alpha = 255

        self.text_positioning = text_positioning
        self.text_rect = None
        self.update_text_pos()

    def click(self):
        sound_lib.sound_effects["click"].play()
        self.down = True

    def release(self):
        self.down = False

    def update_pos(self, x=None, y=None):
        if x:
            self.rect.x = x
        if y:
            self.rect.y = y
        self.update_text_pos()

    def update_text_pos(self):
        text_width = self.rendered_text.get_width()
        text_height = self.rendered_text.get_height()
        if self.text_positioning == "center":
            self.text_rect = pygame.Rect(self.rect.centerx - text_width / 2, self.rect.centery - text_height / 2, text_width, text_height)
        elif self.text_positioning == "left":
            self.text_rect = pygame.Rect(self.rect.x + self.font_size / 3, self.rect.centery - text_height / 2, text_width, text_height)
        elif self.text_positioning == "right":
            self.text_rect = pygame.Rect(self.rect.x + self.rect.width - text_width - self.font_size / 3, self.rect.centery - text_height / 2, text_width, text_height)

    def update_text(self, new_text=None, new_color=None, new_font_size=None):
        new_data = False
        if new_text is not None and new_text != self.text:
            new_data = True
            self.text = new_text
        if new_color and new_color != self.text_color:
            new_data = True
            self.text_color = new_color
            self.text_dark_color = [int(x * 0.25) for x in self.text_color]
        if new_font_size and new_font_size != self.font_size:
            new_data = True
            self.font_size = new_font_size
            self.font = pygame.font.SysFont(Button.font_family, self.font_size)

        if new_data:
            if self.dinamic:
                self.modified = True
        else:
            return

        self.rendered_text = self.font.render(self.text, True, self.text_color)

        if new_text or new_font_size:
            self.highlighted_rendered_text = self.font.render(self.text, True, self.text_highlight_color)
        self.dark_rendered_text = self.font.render(self.text, True, self.text_dark_color)

        self.update_text_pos()

    def draw(self, SCREEN, y_scroll=0, rect_highlight=False, text_highlight=False, dark=False):
        rect = self.rect.copy()
        rect.y += y_scroll
        if dark:
            pygame.draw.rect(SCREEN, self.dark_color, rect)
        elif rect_highlight:
            pygame.draw.rect(SCREEN, self.highlighted_color, rect)

        if self.color:
            pygame.draw.rect(SCREEN, self.color, rect)
        elif self.image_name:
            SCREEN.blit(self.image, rect)

        if self.modified:
            pygame.draw.rect(SCREEN, Object.modified_color, rect, width=2)
        elif self.border_color:
            pygame.draw.rect(SCREEN, self.border_color, rect, width=2)

        self.draw_text(SCREEN, y_scroll, text_highlight)

    def draw_text(self, SCREEN, y_scroll=0, text_highlight=False):
        text_rect = self.text_rect.copy()
        text_rect.y += y_scroll

        if self.down:
            SCREEN.blit(self.dark_rendered_text, text_rect)
        elif text_highlight:
            SCREEN.blit(self.highlighted_rendered_text, text_rect)
        else:
            SCREEN.blit(self.rendered_text, text_rect)


class Dropdown(Button):
    def __init__(self, x, y, w, h, choices, text, dinamic=False, image_name=None, image_alpha=None,
                 color=None, border_color=None, text_color=(255, 255, 255),
                 font_size=20, text_positioning="center", dropdown_area_color=(0,0,255)):
        super().__init__(x, y, w, h, dinamic, image_name, image_alpha,
                         color, border_color, text, text_color, font_size, text_positioning)
        self.active = True
        self.choices = choices
        self.diff = 0  # difference between dropdown menu lines
        self.dropdown_area = None
        self.rendered_text = self.font.render(self.text, True, self.text_color)

        self.update_text_pos()

        self.dropdown_active = False
        self.dropdown_area_color = dropdown_area_color
        self.dropdown_objects = []
        self.create_dropdown_objects()

        # Késöbbi fejlesztés lehetne, hogy a dropdown menü odafigyeljen hogy képernyőn belül maradjon,
        # és ha túlmenne, akkor görgethető legyen.

    def create_dropdown_objects(self):
        height = (self.rect.h + self.diff) * len(self.choices) - self.diff
        self.dropdown_area = Object(
            self.rect.centerx,
            self.rect.centery + (self.rect.h + height) / 2,
            self.rect.w, height,
            self.dropdown_area_color, border_color=(50,50,50))

        for i, choice in enumerate(self.choices):
            rect = self.rect.copy()
            rect.y += (i + 1) * rect.h + i * self.diff
            self.dropdown_objects.append(Button(
                rect.centerx, rect.centery, rect.w, rect.h, color=self.color, text=choice, font_size=self.font_size,
                text_positioning=self.text_positioning))

    def collision(self, mouse_pos):
        self.dropdown_active = False
        for obj in self.dropdown_objects:
            if obj.rect.collidepoint(mouse_pos) and obj.text != self.text:
                self.update_text(new_text=obj.text)
                return

    def draw_dropdown(self, SCREEN, mouse_pos, y_scroll=0):
        self.dropdown_area.draw(SCREEN)

        for obj in self.dropdown_objects:
            rect_highlight = obj.rect.collidepoint(mouse_pos)
            if obj.text == self.text:
                obj.draw(SCREEN, y_scroll, rect_highlight=rect_highlight, text_highlight=True)
            else:
                obj.draw(SCREEN, y_scroll, rect_highlight=rect_highlight)


class Bar(Object):
    def __init__(self, x, y, w, h, dinamic=True, image_name=None, image_alpha=None,
                 color=None, border_color=None, background_color=None, grid_color=None,
                 max_level=10, level=1):
        super().__init__(x, y, w, h, image_name, image_alpha, color, border_color)
        self.active = True
        self.dinamic = dinamic
        self.down = False
        self.max_level = max_level + 1
        self.level = level
        self.background_rect = pygame.Rect(x, y, w, h)
        self.background_rect.center = (x, y)
        self.background_color = background_color
        self.rect = self.background_rect.copy()
        self.rect.w = self.rect.w / self.max_level * self.level
        self.grid_color = grid_color

    def click(self):
        sound_lib.sound_effects["click"].play()
        self.down = True

    def release(self):
        self.down = False

    def set_bar_size(self, x):
        new_level = int(self.max_level / self.background_rect.w * (x - self.background_rect.x)) + 1
        self.update_level(new_level)

    def update_level(self, new_level):
        if new_level and new_level != self.level:
            self.modified = True
            self.level = new_level
            self.rect.w = self.background_rect.w / self.max_level * int(self.level)

    def draw_bar(self, SCREEN, y_scroll=0):
        background_rect = self.background_rect.copy()
        background_rect.y += y_scroll
        rect = self.rect.copy()
        rect.y += y_scroll

        if self.background_color:
            pygame.draw.rect(SCREEN, self.background_color, background_rect)
        if self.color:
            pygame.draw.rect(SCREEN, self.color, rect)
        if self.grid_color:
            start_pos = list(background_rect.topleft)
            end_pos = list(background_rect.bottomleft)
            width = (background_rect.w / self.max_level)
            for x in range(1, self.max_level):
                end_pos[0] = start_pos[0] = int(background_rect.x + width * x)
                pygame.draw.line(SCREEN, self.grid_color,
                                 start_pos, end_pos, width=1)
        if self.modified:
            pygame.draw.rect(SCREEN, Object.modified_color, background_rect, width=2)
        elif self.border_color:
            pygame.draw.rect(SCREEN, self.border_color, background_rect, width=2)