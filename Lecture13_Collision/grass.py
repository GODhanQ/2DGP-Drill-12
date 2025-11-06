from pico2d import *

class Grass:
    def __init__(self):
        self.image = load_image('grass.png')
        self.do_collision = True

    def update(self):
        pass

    def draw(self):
        self.image.draw(400, 30)
        self.image.draw(1200, 30)
        draw_rectangle(*self.get_bb())


    def get_bb(self):
        return 0, 0, 1600, 50

    def handle_collision(self, group, other):
        if group == 'grass:ball':
            pass