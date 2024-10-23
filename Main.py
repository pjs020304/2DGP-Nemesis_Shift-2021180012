from pico2d import *

class Player:
    def __init__(self):
        self.x, self.y = 400,90
        self.frame = 0
        self.action = 0
        self.dir = 0
        self.image = load_image('Sci-fi hero 64x65.png')
        self.mx, self.my = 0,0
    def update(self):
        if self.dir == -1:
            if self.x >= 300:
                self.x -=7
            self.action = 11
            self.frame = (self.frame +1) %8

        elif self.dir == 1:
            if self.x<=700:
                self.x+=7
            self.frame = (self.frame + 1) % 8
            self.action = 11
        else:
            self.action =18
            self.frame = (self.frame +1) % 12
    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_a:
                self.dir -=1
            elif event.key == SDLK_d:
                self.dir +=1
        elif event.type == SDL_KEYUP:
            self.frame = 0
            if event.key == SDLK_a:
                self.dir +=1
            elif event.key == SDLK_d:
                self.dir -=1
        elif event.type == SDL_MOUSEMOTION:
            self.mx, self.my = event.x , DK_height - 1 - event.y
    def draw(self):
        if dir != 0:
            if self.x < self.mx:
                self.image.clip_draw(self.frame * 64, self.action * 65, 64, 65, self.x, self.y, 150, 150)
            elif self.x >= self.mx:
                self.image.clip_composite_draw(self.frame * 64, self.action * 65, 64, 65,0,'h', self.x, self.y, 150, 150)
        else:
            self.image.clip_draw(self.frame * 64, self.action * 65, 64, 65, self.x, self.y, 150, 150)


class BackGround:
    def __init__(self):
        self.layer1 = load_image('layer 1.png')
        self.layer2 = load_image('layer 2.png')
        self.layer3 = load_image('layer 3.png')
        self.layer4 = load_image('layer 4.png')
        self.layer5 = load_image('layer 5.png')
        self.x = [DK_width//2, DK_width//2, DK_width//2, DK_width//2, DK_width//2]
        self.y = [DK_height//2,DK_height//2,DK_height//2,DK_height//2,DK_height//2]
        self.speed = 1
    def update(self):
        if player.dir == 1:
            if player.x >= 700:
                self.x[1] -= self.speed
                self.x[3] -= self.speed*2
                self.x[4] -= self.speed*3
        elif player.dir == -1:
            if player.x <= 300:
                self.x[1] += self.speed
                self.x[3] += self.speed*2
                self.x[4] += self.speed*3
        else:
            pass
    def draw(self):
        self.layer1.draw(self.x[0], self.y[0], 1600, 800)
        self.layer2.draw(self.x[1], self.y[1],1600, 800)
        self.layer3.draw(self.x[2], self.y[2],1600, 800)
        self.layer4.draw(self.x[3], self.y[3],1600, 800)
        self.layer5.draw(self.x[4], self.y[4],1600, 800)

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

    background = BackGround()
    world.append(background)

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

DK_width, DK_height = 1024, 768

open_canvas(DK_width, DK_height)
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.03)
close_canvas()