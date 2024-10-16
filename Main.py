from pico2d import *

class Player:
    def __init__(self):
        self.x, self.y = 400,90
        self.frame = 0
        self.action = 0
        self.dir = 0
        self.image = load_image('Sci-fi hero 64x65.png')
    def update(self):
        if self.dir == -1:
            self.x -=5
            self.action = 11
            self.frame = (self.frame +1) %8
        elif self.dir == 1:
            self.x+=5
            self.frame = (self.frame + 1) % 8
            self.action = 11
        else:
            self.action =18
            self.frame = (self.frame +1) % 12

    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_LEFT:
                self.dir -=1
            elif event.key == SDLK_RIGHT:
                self.dir +=1
        elif event.type == SDL_KEYUP:
            self.frame = 0
            if event.key == SDLK_LEFT:
                self.dir +=1
            elif event.key == SDLK_RIGHT:
                self.dir -=1
    def draw(self):
        if self.dir == 1:
            self.image.clip_draw(self.frame * 64, self.action * 65, 64, 65, self.x, self.y, 100, 100)
        elif self.dir == -1:
            self.image.clip_composite_draw(self.frame * 64, self.action * 65, 64, 65,0,'h', self.x, self.y, 100, 100)
        else:
            self.image.clip_draw(self.frame * 64, self.action * 65, 64, 65, self.x, self.y, 100, 100)

def handle_events():
    global running

    events = get_events()
    for event in events:
        if event.type == SDL_QUIT:
            running = False
        elif event.type == SDL_KEYDOWN and event.key == SDLK_ESCAPE:
            running = False
        else:
            player.handle_event(event)


def reset_world():
    global running
    global player
    global world

    running = True
    world = []

    player = Player()
    world.append(player)

def update_world():
    for i in world:
        i.update()

def render_world():
    clear_canvas()
    for i in world:
        i.draw()
    update_canvas()

open_canvas()
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.01)
close_canvas()