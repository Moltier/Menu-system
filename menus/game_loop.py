import pygame


def game_loop(ui, settings, program_data):
    draw_game(ui, program_data)
    if ui.handle_menu_transition(settings.get_resolution()):
        return
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ui.mode = "exit"

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                ui.mode = "main menu"
                ui.start_transition_timer()
                # should bring up a sub menu. Basically the options menu, but inside the game loop.

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left
                pass
                # if ui.menus[program_data.status].objects["ready"].rect.collidepoint(mouse_pos):
                #     ui.menus[program_data.status].objects["ready"].click()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left
                pass
                # if ui.menus["placeholder"].objects["placeholder"].rect.collidepoint(mouse_pos):
                #     ui.status = "exiting"

                # for obj in ui.menus["placeholder"].objects.values():
                #     obj.release()


def draw_game(ui, program_data):
    ui.SCREEN.blit(ui.background_img, (0, 0))