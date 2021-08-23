import pygame


def main_menu(ui, settings):
    draw_main_menu(ui)
    if ui.handle_menu_transition(settings.get_resolution()):
        return
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ui.mode = "exit"

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                ui.mode = "exit"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left
                if ui.menus["main menu"].objects["new game"].rect.collidepoint(mouse_pos):
                    ui.menus["main menu"].objects["new game"].click()
                elif ui.menus["main menu"].objects["options"].rect.collidepoint(mouse_pos):
                    ui.menus["main menu"].objects["options"].click()
                elif ui.menus["main menu"].objects["exit"].rect.collidepoint(mouse_pos):
                    ui.menus["main menu"].objects["exit"].click()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left
                if ui.menus["main menu"].objects["new game"].rect.collidepoint(mouse_pos):
                    if ui.menus["main menu"].objects["new game"].down:
                        ui.menus["main menu"].objects["new game"].down = False
                        ui.next_mode = "game"
                        ui.start_transition_timer()

                elif ui.menus["main menu"].objects["options"].rect.collidepoint(mouse_pos):
                    if ui.menus["main menu"].objects["options"].down:
                        ui.menus["main menu"].objects["options"].down = False
                        ui.next_mode = "options"
                        ui.start_transition_timer()

                elif ui.menus["main menu"].objects["exit"].rect.collidepoint(mouse_pos):
                    if ui.menus["main menu"].objects["exit"].down:
                        ui.mode = "exit"

                ui.menus["main menu"].objects["new game"].down = False
                ui.menus["main menu"].objects["options"].down = False
                ui.menus["main menu"].objects["exit"].down = False


def draw_main_menu(ui):
    ui.SCREEN.blit(ui.background_img, (0, 0))

    for button in ui.menus["main menu"].objects.values():
        button.draw(ui.SCREEN)
