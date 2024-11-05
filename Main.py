from pico2d import open_canvas, delay, close_canvas

import  play_mode

open_canvas(play_mode.DK_width, play_mode.DK_height)
play_mode.init()

while play_mode.running:
    play_mode.handle_events()
    play_mode.update()
    play_mode.render()
    delay(0.03)

play_mode.finish()

close_canvas()