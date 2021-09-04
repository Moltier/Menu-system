import pygame


def audio_menu(ui, settings):
    draw_audio_menu(ui)
    if ui.handle_menu_transition(settings.get_resolution()):
        return
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ui.mode = "exit"

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                ui.next_mode = "options"
                ui.start_transition_timer()

        elif event.type == pygame.MOUSEMOTION:
            for obj in ui.menus["audio menu bars"].objects.values():
                if obj.down:
                    obj.set_bar_size(mouse_pos[0])

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left
                for obj in ui.menus["audio menu bars"].objects.values():
                    if obj.background_rect.collidepoint(mouse_pos):
                        obj.click()
                        return
                for obj in ui.menus["general options"].objects.values():
                    if obj.rect.collidepoint(mouse_pos):
                        obj.click()
                        return

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left
                if ui.menus["audio menu bars"].objects["music"].background_rect.collidepoint(mouse_pos):
                    if ui.menus["audio menu bars"].objects["music"].down:
                        ui.menus["audio menu bars"].objects["music"].set_bar_size(mouse_pos[0])
                elif ui.menus["audio menu bars"].objects["sound"].background_rect.collidepoint(mouse_pos):
                    if ui.menus["audio menu bars"].objects["sound"].down:
                        ui.menus["audio menu bars"].objects["sound"].set_bar_size(mouse_pos[0])

                elif ui.menus["general options"].objects["save"].rect.collidepoint(mouse_pos):
                    if ui.menus["general options"].objects["save"].down:
                        ui.reset_borders()
                        settings.save(ui.mode, ui.get_options_data())
                        ui.apply_volume(settings.music_volume, settings.sound_volume)

                elif ui.menus["general options"].objects["back"].rect.collidepoint(mouse_pos):
                    if ui.menus["general options"].objects["back"].down:
                        ui.next_mode = "options"
                        ui.start_transition_timer()

                elif ui.menus["general options"].objects["reset"].rect.collidepoint(mouse_pos):
                    if ui.menus["general options"].objects["reset"].down:
                        settings.load_data(ui.mode)
                        ui.update_audio_levels(settings)
                        ui.reset_borders()

                elif ui.menus["general options"].objects["default"].rect.collidepoint(mouse_pos):
                    if ui.menus["general options"].objects["default"].down:
                        settings.reset_to_default(ui.mode)
                        ui.update_audio_levels(settings)

                for obj in ui.menus["audio menu bars"].objects.values():
                    obj.release()
                for obj in ui.menus["general options"].objects.values():
                    obj.release()


def draw_audio_menu(ui):
    ui.SCREEN.blit(ui.background_img, (0, 0))

    for text_obj in ui.menus["audio"].objects.values():
        text_obj.draw(ui.SCREEN)
    for bar in ui.menus["audio menu bars"].objects.values():
        bar.draw_bar(ui.SCREEN)

    for button in ui.menus["general options"].objects.values():
        button.draw(ui.SCREEN)
