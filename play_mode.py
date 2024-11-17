from pico2d import *
import game_world
import game_framework
import pause_mode
import player
import blocks
import background
import monster

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
    global collider_trig
    global pandas

    collider_trig = False
    gravity = 1
    running = True

    backgrounds = background.BackGround()
    game_world.add_obj(backgrounds,0)

    player = player.Player()
    game_world.add_obj(player,1)
    game_world.add_collision_pair('player:block', player, None)

    blocks = [
        blocks.Block(30, 176, 82, 22, 600, 175+100, 300, 100),
        blocks.Block(30, 176, 82, 22, DK_width//2, DK_height//4, 500, 100)
    ]
    for block in blocks:
        game_world.add_obj(block, 0)
        pass
    for block in blocks:
        game_world.add_collision_pair('player:block', None, block)

    pandas = [monster.Panda(0, 12, 103, 33, 8, DK_width//2, DK_height//4+50, 100, 100, DK_width//2+250, DK_width//2 - 250)]
    for panda in pandas:
        game_world.add_obj(panda, 1)

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