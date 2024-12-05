import pico2d
import play_mode
import game_framework
import start_mode as start_mode
pico2d.open_canvas(play_mode.DK_width, play_mode.DK_height)
game_framework.run(start_mode)
pico2d.close_canvas()