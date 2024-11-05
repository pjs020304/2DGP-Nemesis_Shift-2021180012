from pico2d import *
import game_world

class Player:
    def __init__(self):
        self.x, self.y = 400,90
        self.size_x, self.size_y = 120, 120
        self.frame = 0
        self.action = 0
        self.dir = 0
        self.image = load_image('Sci-fi hero 64x65.png')

        # 떨어짐 체크
        self.vertical = 0
        self.fall = False
        self.min_x, self.max_x = 0, 1000

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


        # 중력 적용
        if self.fall:
            self.y += self.vertical
            self.vertical -= gravity
            self.action = 9
            self.frame = (self.frame + 1) % 6

        # 땅과의 충돌 체크
        on_ground = False
        for block in blocks:
            if block.collide(block):
                self.y = block.y + (block.size_y//2) +25  # 블록 위에 위치
                self.vertical = 0
                self.fall = False
                self.min_x, self.max_x = block.x - (block.size_x//2), block.x + (block.size_x//2)
                on_ground = True
                break
        if not on_ground and self.y <= 90:
            self.y = 90
            self.vertical = 0
            self.fall = False

        if self.x <self.min_x or self.x > self.max_x:
            self.fall = True
            self.min_x, self.max_x = 0, 1000



    def handle_event(self, event):
        if event.type == SDL_KEYDOWN:
            if event.key == SDLK_a:
                self.dir -=1
            if event.key == SDLK_d:
                self.dir +=1
            if event.key == SDLK_SPACE and self.fall == False:
                self.frame = 0
                self.fall = True
                self.vertical = 36
        elif event.type == SDL_KEYUP:
            self.frame = 0
            if event.key == SDLK_a:
                self.dir +=1
            if event.key == SDLK_d:
                self.dir -=1

        elif event.type == SDL_MOUSEMOTION:
            self.mx, self.my = event.x , DK_height - 1 - event.y
    def draw(self):
        if dir != 0:
            if self.x < self.mx:
                self.image.clip_draw(self.frame * 64, self.action * 65, 60, 65, self.x, self.y, self.size_x, self.size_y)
            elif self.x >= self.mx:
                self.image.clip_composite_draw(self.frame * 64, self.action * 65, 60, 65,0,'h', self.x, self.y, self.size_x, self.size_y)
        else:
            self.image.clip_draw(self.frame * 64, self.action * 65, 60, 65, self.x, self.y, self.size_x, self.size_y)


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
                self.x[2] -= self.speed
                self.x[3] -= self.speed*2
                self.x[4] -= self.speed*3
        elif player.dir == -1:
            if player.x <= 300:
                self.x[2] += self.speed
                self.x[3] += self.speed*2
                self.x[4] += self.speed*3
        else:
            pass
    def draw(self):
        self.layer1.draw(self.x[0], self.y[0], 1600, 800)
        self.layer2.draw(self.x[1], self.y[1],1600, 800)
        self.layer3.draw(self.x[2], self.y[2],2400, 800)
        self.layer4.draw(self.x[3], self.y[3],2400, 800)
        self.layer5.draw(self.x[4], self.y[4],2400, 800)
        pass





class Block:
    def __init__(self, frame_x, action_y, width, height, position_x, position_y, size_x, size_y):
        self.frame, self.action =frame_x, action_y
        self.width, self.height = width, height
        self.x, self.y = position_x, position_y
        self.size_x, self.size_y = size_x, size_y

        # self.image = load_image('DARK Edition Tileset No background.png')
        self.image = load_image('layer 1.png')

    def collide(self, block):
        if block.x-(block.size_x //2) < player.x < block.x + (block.size_x //2):
            if block.y< player.y< block.y+(block.size_y //2):
                return True
        return False
    def update(self):
        if player.dir == 1:
            if player.x >= 700:
                self.x -=7
        elif player.dir == -1:
            if player.x <= 300:
                self.x += 7

        pass
    def draw(self):
        self.image.clip_draw(self.frame, self.action, self.width, self.height, self.x, self.y, self.size_x, self.size_y)








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
    global gravity
    global blocks

    gravity = 3
    running = True

    background = BackGround()
    game_world.add_obj(background,0)

    player = Player()
    game_world.add_obj(player,1)

    blocks = [Block(0, 62, 45, 18, DK_width//2, DK_height//2, 300, 100), Block(0, 62, 45, 18, DK_width//2, DK_height//4, 150, 100)]
    for block in blocks:
        game_world.add_obj(block, 0)
        pass



def update_world():
    game_world.update()

def render_world():
    clear_canvas()
    game_world.render()
    update_canvas()

DK_width, DK_height = 1000, 700

open_canvas(DK_width, DK_height)
reset_world()

while running:
    handle_events()
    update_world()
    render_world()
    delay(0.03)
close_canvas()