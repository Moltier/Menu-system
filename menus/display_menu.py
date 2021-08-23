import pygame


def display_menu(ui, settings):
    mouse_pos = pygame.mouse.get_pos()
    draw_display_menu(ui, mouse_pos)
    if ui.handle_menu_transition(settings.get_resolution()):
        return

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ui.mode = "exit"

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                ui.next_mode = "options"
                ui.start_transition_timer()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left
                if ui.menus["display menu buttons"].objects["resolution"].dropdown_active \
                        or ui.menus["display menu buttons"].objects["framerate"].dropdown_active \
                        or ui.menus["display menu buttons"].objects["text size"].dropdown_active:
                    pass
                elif ui.menus["display menu buttons"].objects["full screen"].rect.collidepoint(mouse_pos):
                    ui.menus["display menu buttons"].objects["full screen"].click()
                elif ui.menus["display menu buttons"].objects["vertical sync"].rect.collidepoint(mouse_pos):
                    ui.menus["display menu buttons"].objects["vertical sync"].click()
                elif ui.menus["display menu buttons"].objects["resolution"].rect.collidepoint(mouse_pos):
                    ui.menus["display menu buttons"].objects["resolution"].click()
                elif ui.menus["display menu buttons"].objects["framerate"].rect.collidepoint(mouse_pos):
                    ui.menus["display menu buttons"].objects["framerate"].click()
                elif ui.menus["display menu buttons"].objects["text size"].rect.collidepoint(mouse_pos):
                    ui.menus["display menu buttons"].objects["text size"].click()

                elif ui.menus["general options"].objects["save"].rect.collidepoint(mouse_pos):
                    ui.menus["general options"].objects["save"].click()
                elif ui.menus["general options"].objects["back"].rect.collidepoint(mouse_pos):
                    ui.menus["general options"].objects["back"].click()
                elif ui.menus["general options"].objects["reset"].rect.collidepoint(mouse_pos):
                    ui.menus["general options"].objects["reset"].click()
                elif ui.menus["general options"].objects["default"].rect.collidepoint(mouse_pos):
                    ui.menus["general options"].objects["default"].click()

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left
                if ui.menus["display menu buttons"].objects["resolution"].dropdown_active:
                    ui.menus["display menu buttons"].objects["resolution"].collision(mouse_pos)
                elif ui.menus["display menu buttons"].objects["framerate"].dropdown_active:
                    ui.menus["display menu buttons"].objects["framerate"].collision(mouse_pos)
                elif ui.menus["display menu buttons"].objects["text size"].dropdown_active:
                    ui.menus["display menu buttons"].objects["text size"].collision(mouse_pos)

                else:
                    if ui.menus["display menu buttons"].objects["full screen"].rect.collidepoint(mouse_pos):
                        if ui.menus["display menu buttons"].objects["full screen"].down:
                            ui.menus["display menu buttons"].objects["full screen"].update_text("True" if ui.menus["display menu buttons"].objects["full screen"].text == "False" else "False")
                    elif ui.menus["display menu buttons"].objects["vertical sync"].rect.collidepoint(mouse_pos):
                        if ui.menus["display menu buttons"].objects["vertical sync"].down:
                            ui.menus["display menu buttons"].objects["vertical sync"].update_text("True" if ui.menus["display menu buttons"].objects["vertical sync"].text == "False" else "False")

                    elif ui.menus["display menu buttons"].objects["resolution"].rect.collidepoint(mouse_pos):
                        if ui.menus["display menu buttons"].objects["resolution"].down:
                            ui.menus["display menu buttons"].objects["resolution"].dropdown_active = not ui.menus["display menu buttons"].objects["resolution"].dropdown_active
                    elif ui.menus["display menu buttons"].objects["framerate"].rect.collidepoint(mouse_pos):
                        if ui.menus["display menu buttons"].objects["framerate"].down:
                            ui.menus["display menu buttons"].objects["framerate"].dropdown_active = not ui.menus["display menu buttons"].objects["framerate"].dropdown_active
                    elif ui.menus["display menu buttons"].objects["text size"].rect.collidepoint(mouse_pos):
                        if ui.menus["display menu buttons"].objects["text size"].down:
                            ui.menus["display menu buttons"].objects["text size"].dropdown_active = not ui.menus["display menu buttons"].objects["text size"].dropdown_active

                    elif ui.menus["general options"].objects["save"].rect.collidepoint(mouse_pos):
                        if ui.menus["general options"].objects["save"].down:
                            settings.save(ui.mode, ui.get_options_data())

                            if settings.prev_full_screen != settings.full_screen or settings.prev_resolution != settings.resolution:
                                ui.set_screen_mode(settings)
                                if settings.prev_resolution != settings.resolution:
                                    ui.create_objects(settings)
                                    settings.prev_resolution = settings.resolution
                                settings.prev_full_screen = settings.full_screen

                            if settings.prev_text_size != settings.text_size:
                                ui.update_buttons(settings.get_resolution(), settings.get_font_multiplier())
                                ui.update_text_objects(settings)
                                settings.prev_text_size = settings.text_size
                            ui.reset_borders()

                    elif ui.menus["general options"].objects["back"].rect.collidepoint(mouse_pos):
                        if ui.menus["general options"].objects["back"].down:
                            ui.menus["general options"].objects["back"].down = False
                            ui.next_mode = "options"
                            ui.start_transition_timer()

                    elif ui.menus["general options"].objects["reset"].rect.collidepoint(mouse_pos):
                        if ui.menus["general options"].objects["reset"].down:
                            settings.load_data(ui.mode)
                            ui.update_display_buttons(settings)
                            ui.reset_borders()

                    elif ui.menus["general options"].objects["default"].rect.collidepoint(mouse_pos):
                        if ui.menus["general options"].objects["default"].down:
                            settings.reset_to_default(ui.mode)
                            ui.update_display_buttons(settings)

                    ui.menus["display menu buttons"].objects["full screen"].down = False
                    ui.menus["display menu buttons"].objects["vertical sync"].down = False
                    ui.menus["display menu buttons"].objects["resolution"].down = False
                    ui.menus["display menu buttons"].objects["framerate"].down = False
                    ui.menus["display menu buttons"].objects["text size"].down = False

                    ui.menus["general options"].objects["save"].down = False
                    ui.menus["general options"].objects["back"].down = False
                    ui.menus["general options"].objects["reset"].down = False
                    ui.menus["general options"].objects["default"].down = False


def draw_display_menu(ui, mouse_pos):
    ui.SCREEN.blit(ui.background_img, (0, 0))
    for text_obj in ui.menus["display"].objects.values():
        text_obj.draw(ui.SCREEN)

    for button in ui.menus["display menu buttons"].objects.values():
        button.draw(ui.SCREEN)

    for button in ui.menus["general options"].objects.values():
        button.draw(ui.SCREEN)

    if ui.menus["display menu buttons"].objects["resolution"].dropdown_active:
        ui.menus["display menu buttons"].objects["resolution"].draw_dropdown(ui.SCREEN, mouse_pos)
    elif ui.menus["display menu buttons"].objects["framerate"].dropdown_active:
        ui.menus["display menu buttons"].objects["framerate"].draw_dropdown(ui.SCREEN, mouse_pos)
    elif ui.menus["display menu buttons"].objects["text size"].dropdown_active:
        ui.menus["display menu buttons"].objects["text size"].draw_dropdown(ui.SCREEN, mouse_pos)
