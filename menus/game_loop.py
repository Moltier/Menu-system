import pygame


def game_loop(ui, settings):
    draw_game(ui)
    if ui.handle_menu_transition(settings.get_resolution()):
        return
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ui.mode = "exit"

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                ui.update_background_img("galaxy", settings.get_resolution())
                ui.mode = "pause"

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left
                if ui.menus["other"].objects["back"].rect.collidepoint(mouse_pos):
                    ui.menus["other"].objects["back"].click()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left
                if ui.menus["other"].objects["back"].rect.collidepoint(mouse_pos):
                    if ui.menus["other"].objects["back"].down:
                        ui.menus["other"].objects["back"].down = False
                        ui.next_mode = "main menu"
                        ui.start_transition_timer()

                ui.menus["other"].objects["back"].down = False


def draw_game(ui):
    ui.SCREEN.blit(ui.background_img, (0, 0))

    for button in ui.menus["other"].objects.values():
        button.draw(ui.SCREEN)
