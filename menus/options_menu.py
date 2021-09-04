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
                for obj in ui.menus["options"].objects.values():
                    if obj.collidepoint(mouse_pos):
                        obj.click()
                        return

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left
                if ui.menus["options"].objects["display"].rect.collidepoint(mouse_pos):
                    if ui.menus["options"].objects["display"].down:
                        ui.next_mode = "display"
                        ui.start_transition_timer()
                elif ui.menus["options"].objects["audio"].rect.collidepoint(mouse_pos):
                    if ui.menus["options"].objects["audio"].down:
                        ui.next_mode = "audio"
                        ui.start_transition_timer()
                elif ui.menus["options"].objects["controls"].rect.collidepoint(mouse_pos):
                    if ui.menus["options"].objects["controls"].down:
                        ui.next_mode = "controls"
                        ui.start_transition_timer()
                elif ui.menus["options"].objects["other"].rect.collidepoint(mouse_pos):
                    if ui.menus["options"].objects["other"].down:
                        ui.next_mode = "other"
                        ui.start_transition_timer()
                elif ui.menus["options"].objects["back"].rect.collidepoint(mouse_pos):
                    if ui.menus["options"].objects["back"].down:
                        if ui.game_is_running:
                            ui.mode = "pause"
                        else:
                            ui.next_mode = "main menu"
                            ui.start_transition_timer()

                for obj in ui.menus["options"].objects.values():
                    obj.release()


def draw_options_menu(ui):
    ui.SCREEN.blit(ui.background_img, (0, 0))

    for button in ui.menus["options"].objects.values():
        button.draw(ui.SCREEN)
