world = [[], []]

def add_obj(o, depth):
    world[depth].append(o)

def update():
    for layer in world:
        for o in layer:
            o.update()
def render():
    for layer in world:
        for o in layer:
            o.draw()

def remove_object(o):
    for layer in world:
        if o in layer:
            layer.remove(o)
            return # 지우기 끝남
    print('존재하지 않는 객체를 지우려고 시도함')