import sys
import pygame
from settings import Settings
from ui import UI
from menus.main_menu import main_menu
from menus.game_loop import game_loop
from menus.options_menu import options_menu
from menus.display_menu import display_menu
from menus.audio_menu import audio_menu
from menus.control_menu import control_menu
from program_data import ProgramData

# client_data.width = pyautogui.size().width
# client_data.height = pyautogui.size().height

# known bugs:
#   As of pygame 2.0 switching between fullscreen and window mode will put the window to the topleft corner.
#       should be fixed in 2.0.2
#
#   In full screen mode, switching to a smaller resolution not fit to the monitor leaves drawn areas from previous resolution.

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption("Menu system")
    settings = Settings()
    ui = UI(settings)
    program_data = ProgramData()

    ui.create_objects(settings)
    ui.start_mode("main menu", settings.get_resolution())

    clock = pygame.time.Clock()
    ui.start_transition_timer()

    while True:
        pygame.display.update()
        clock.tick(int(settings.framerate))

        ui.SCREEN.fill((20, 20, 20))

        if ui.mode == "game":
            game_loop(ui, settings, program_data)
        elif ui.mode == "main menu":
            main_menu(ui, settings, program_data)
        elif ui.mode == "options":
            options_menu(ui, settings)
        elif ui.mode == "display":
            display_menu(ui, settings, program_data)
        elif ui.mode == "audio":
            audio_menu(ui, settings)
        elif ui.mode == "controls":
            control_menu(ui, settings)
        elif ui.mode == "other":
            control_menu(ui, settings)  # placeholder
        elif ui.mode == "exit":
            pygame.quit()
            sys.exit()
        else:
            print(f"Unknown ui.mode: {ui.mode}")
