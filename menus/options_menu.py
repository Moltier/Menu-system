import pygame


def options_menu(ui, settings):
    draw_options_menu(ui)
    if ui.handle_menu_transition(settings.get_resolution()):
        return
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ui.mode = "exit"

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                if ui.game_is_running:
                    ui.update_background_img(settings.get_resolution())
                    ui.mode = "pause"
                else:
                    ui.next_mode = "main menu"
                    ui.start_transition_timer()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left
                if ui.menus["options"].objects["display"].rect.collidepoint(mouse_pos):
                    ui.menus["options"].objects["display"].click()
                elif ui.menus["options"].objects["audio"].rect.collidepoint(mouse_pos):
                    ui.menus["options"].objects["audio"].click()
                elif ui.menus["options"].objects["controls"].rect.collidepoint(mouse_pos):
                    ui.menus["options"].objects["controls"].click()
                elif ui.menus["options"].objects["other"].rect.collidepoint(mouse_pos):
                    ui.menus["options"].objects["other"].click()
                elif ui.menus["options"].objects["back"].rect.collidepoint(mouse_pos):
                    ui.menus["options"].objects["back"].click()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left
                if ui.menus["options"].objects["display"].rect.collidepoint(mouse_pos):
                    if ui.menus["options"].objects["display"].down:
                        ui.menus["options"].objects["display"].down = False
                        ui.next_mode = "display"
                        ui.start_transition_timer()
                elif ui.menus["options"].objects["audio"].rect.collidepoint(mouse_pos):
                    if ui.menus["options"].objects["audio"].down:
                        ui.menus["options"].objects["audio"].down = False
                        ui.next_mode = "audio"
                        ui.start_transition_timer()
                elif ui.menus["options"].objects["controls"].rect.collidepoint(mouse_pos):
                    if ui.menus["options"].objects["controls"].down:
                        ui.menus["options"].objects["controls"].down = False
                        ui.next_mode = "controls"
                        ui.start_transition_timer()
                elif ui.menus["options"].objects["other"].rect.collidepoint(mouse_pos):
                    if ui.menus["options"].objects["other"].down:
                        ui.menus["options"].objects["other"].down = False
                        ui.next_mode = "other"
                        ui.start_transition_timer()
                elif ui.menus["options"].objects["back"].rect.collidepoint(mouse_pos):
                    if ui.menus["options"].objects["back"].down:
                        ui.menus["options"].objects["back"].down = False
                        if ui.game_is_running:
                            ui.mode = "pause"
                        else:
                            ui.next_mode = "main menu"
                            ui.start_transition_timer()

                ui.menus["options"].objects["display"].down = False
                ui.menus["options"].objects["audio"].down = False
                ui.menus["options"].objects["controls"].down = False
                ui.menus["options"].objects["other"].down = False
                ui.menus["options"].objects["back"].down = False


def draw_options_menu(ui):
    ui.SCREEN.blit(ui.background_img, (0, 0))

    for button in ui.menus["options"].objects.values():
        button.draw(ui.SCREEN)
