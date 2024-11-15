from pico2d import *
import game_world
import game_framework
import pause_mode
import player
import blocks
import background


def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            game_framework.quit()
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            game_framework.push_mode(pause_mode)
        else:
            player.handle_event(event)

def init():
    global running
    global player
    global gravity
    global blocks
    global DK_width, DK_height

    gravity = 1
    running = True

    backgrounds = background.BackGround()
    game_world.add_obj(backgrounds,0)

    player = player.Player()
    game_world.add_obj(player,1)
    game_world.add_collision_pair('player:block', player, None)

    blocks = [
        blocks.Block(0, 62, 45, 18, DK_width, DK_height//2, 300, 100),
        blocks.Block(0, 62, 45, 18, DK_width//2, DK_height//4, 150, 100)
    ]
    for block in blocks:
        game_world.add_obj(block, 0)
        pass
    for block in blocks:
        game_world.add_collision_pair('player:block', None, block)


def update():
    game_world.update()
    game_world.handle_collisions()
def draw():
    clear_canvas()
    game_world.render()
    update_canvas()

def finish():
    pass
DK_width, DK_height = 1000, 700

def pause():
    pass
def resume():
    pass