import pygame


def control_menu(ui, settings):
    draw_control_menu(ui)
    if ui.handle_menu_transition(settings.get_resolution()):
        return
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ui.mode = "exit"

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                ui.next_mode = "options"
                ui.next_background_img_name = "ocean"
                ui.start_transition_timer()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left
                if ui.menus["other"].objects["back"].rect.collidepoint(mouse_pos):
                    ui.menus["other"].objects["back"].click()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left
                if ui.menus["other"].objects["back"].rect.collidepoint(mouse_pos):
                    if ui.menus["other"].objects["back"].down:
                        ui.next_mode = "options"
                        ui.start_transition_timer()

                for obj in ui.menus["other"].objects.values():
                    obj.release()


def draw_control_menu(ui):
    ui.SCREEN.blit(ui.background_img, (0, 0))

    for button in ui.menus["other"].objects.values():
        button.draw(ui.SCREEN)