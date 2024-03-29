# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 15:15:47 2023

@author: kiddra
"""
import tcod
import render.colors as colors
import traceback
import exceptions
import input_handlers
import setup_game
    
def save_game(handler: input_handlers.BaseEventHandler, filename: str) -> None:
    """If the current event handler has an active Engine then save it."""
    if isinstance(handler, input_handlers.EventHandler):
        handler.engine.save_as(filename)
        print("Game saved.")

def main() -> None:
    screen_width = 116
    screen_height = 70

    tileset = tcod.tileset.load_tilesheet(
        "images/dejavu10x10_gs_tc.png", 32, 8, tcod.tileset.CHARMAP_TCOD
        #"images/dejavu16x16_gs_tc.png", 16,16, tcod.tileset.CHARMAP_TCOD
    )
    
    handler: input_handlers.BaseEventHandler = setup_game.MainMenu()
    
    with tcod.context.new_terminal(
        screen_width,
        screen_height,
        tileset=tileset,
        title="Dynastar",
        vsync=True,
    ) as context:
        root_console = tcod.console.Console(screen_width, screen_height, order="F")
        try:
            while True:
                root_console.clear()
                handler.on_render(console=root_console)
                context.present(root_console)
                #Full screen
                #context.sdl_window.fullscreen = tcod.sdl.video.WindowFlags.FULLSCREEN_DESKTOP
                
                try:
                    for event in tcod.event.wait():
                        context.convert_event(event)
                        handler = handler.handle_events(event)
                except Exception:  # Handle exceptions in game.
                    traceback.print_exc()  # Print error to stderr.
                    # Then print the error to the message log.
                    if isinstance(handler, input_handlers.EventHandler):
                        handler.engine.message_log.add_message(
                            traceback.format_exc(), colors.error
                        )
        except exceptions.QuitWithoutSaving:
            raise
        except SystemExit:  # Save and quit.
            save_game(handler, "savegame.sav")
            raise
        except BaseException:  # Save on any other unexpected exception.
            save_game(handler, "savegame.sav")
            raise

if __name__ == "__main__":
    main()