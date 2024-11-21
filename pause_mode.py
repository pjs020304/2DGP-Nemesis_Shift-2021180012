from sdl2 import SDL_KEYDOWN, SDLK_ESCAPE, SDL_QUIT, SDLK_SPACE, SDLK_0, SDLK_1, SDLK_2

import game_framework
from pico2d import get_time, clear_canvas, get_events, update_canvas, load_image

import game_world
import play_mode

from pico2d import load_image

class Pannel:
    def __init__(self, image_name, x_position, y_position, size_x, size_y):
        self.image = load_image(image_name)
        self.x_position, self.y_position = x_position, y_position
        self.size_x, self.size_y = size_x, size_y
    def draw(self):
        self.image.draw(self.x_position, self.y_position, self.size_x, self.size_y)

    def update(self):
        pass


def init():
    global pannels
    pannels = [Pannel('Resource\\UI_continue.png', play_mode.DK_width//2, play_mode.DK_height//2+200, 600, 100), Pannel('Resource\\dk_UI_option.png',play_mode.DK_width//2, play_mode.DK_height//2, 600, 100), Pannel('Resource\\DK_UI_quit.png',play_mode.DK_width//2, play_mode.DK_height//2-200, 600, 100)]


    for pannel in pannels:
        game_world.add_obj(pannel, 1)


def finish():
    for pannel in pannels:
        game_world.remove_object(pannel)

def handle_events():
    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.pop_mode()

def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def update():
    pass

def pause():
    pass
def resume():
    pass