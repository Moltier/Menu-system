import pygame

pygame.mixer.init()


class Sound:
    def __init__(self, file_name):
        self.name = file_name
        self.volume = None  # this will be usefull, once every sound effects can have their own volume in settings
        self.sound = pygame.mixer.Sound(f'Audio/Sound effects/{file_name}')

    def play(self):
        self.sound.play()

    def set_volume(self, volume):
        self.volume = volume
        self.sound.set_volume(self.volume / 10)


class Music:
    def __init__(self, file_name, loop=True):
        self.name = None
        self.loop = loop
        pygame.mixer.music.load(f'Audio/Music/{file_name}')


    def start_music(self):
        pygame.mixer.music.play(-1 if self.loop else 0)

    def stop_music(self):
        pygame.mixer.music.stop()

    def set_volume(self, volume):
        pygame.mixer.music.set_volume(0.005 * volume)
