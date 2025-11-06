import time

from pico2d import *
import game_world
import game_framework

PIXEL_PER_METER = (1.0 / 0.03)  # 1pixel = 3cm, 1m = 33.33 pixel
GRAVITY = 9.8  # 중력 가속도 (m/s²)

class Ball:
    image = None

    def __init__(self, x = 400, y = 300, throwin_speed = 15, throwin_angle = 45):
        if Ball.image == None:
            Ball.image = load_image('ball21x21.png')
        self.x, self.y = x, y
        self.xv = throwin_speed * math.cos(math.radians(throwin_angle))  # m/s
        self.yv = abs(throwin_speed * math.sin(math.radians(throwin_angle)))   # m/s
        self.stopped = True if throwin_speed == 0.0 else False
        self.do_collision = True
        self.collision_timer = time.time()

    def draw(self):
        self.image.draw(self.x, self.y)
        draw_rectangle(*self.get_bb())

    def update(self):
        if self.stopped:
            return
        # 위치 업데이트
        self.x += self.xv * game_framework.frame_time * PIXEL_PER_METER
        self.y += self.yv * game_framework.frame_time * PIXEL_PER_METER

        # y 축 속도에 중력 가속도 적용
        self.yv -= GRAVITY * game_framework.frame_time  # m/s

        if self.x < 0 or self.x > 1600:
            self.xv = -self.xv

        vector_length = math.sqrt(self.xv ** 2 + self.yv ** 2)
        if vector_length < 0.1:
            self.stopped = True
            print("Ball stopped moving")

        if self.do_collision == False:
            # 약 1초 후에 충돌 활성화
            duration = time.time() - self.collision_timer
            if duration > 0.1:
                self.do_collision = True
                print("Ball collision activated")



    def get_bb(self):
        return self.x - 10, self.y - 10, self.x + 10, self.y + 10

    def handle_collision(self, group, other):
        if group == 'boy:ball':
            game_world.remove_object(self)

        if group == 'grass:ball':
            self.xv = self.xv * 0.6
            self.yv = -self.yv * 0.6

            self.do_collision = False
            print("Ball collided with grass, bouncing")
            self.collision_timer = time.time()