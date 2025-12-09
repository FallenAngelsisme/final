import pygame as pg

class MonsterAttackAnimation:
    def __init__(self, path, frame_w, frame_h, num_frames, move_distance=25):
        self.sheet = pg.image.load(path).convert_alpha()
        self.frames = []
        self.frame_count = num_frames
        
        for i in range(num_frames):
            rect = pg.Rect(i * frame_w, 0, frame_w, frame_h)
            self.frames.append(self.sheet.subsurface(rect))

        self.index = 0
        self.timer = 0
        self.speed = 0.07     # 每格播放時間
        self.finished = False

        # 位移
        self.move_distance = move_distance
        self.move_progress = 0  # 0~1
        self.forward = True     # 往前 → 再往後

    def update(self, dt):
        if self.finished:
            return

        # 走動畫
        self.timer += dt
        if self.timer > self.speed:
            self.timer = 0
            self.index += 1
            if self.index >= self.frame_count:
                self.index = 0
                self.finished = True

        # 控制往前衝 / 退回
        if self.forward:
            self.move_progress += dt * 3
            if self.move_progress >= 1:
                self.move_progress = 1
                self.forward = False
        else:
            self.move_progress -= dt * 3
            if self.move_progress <= 0:
                self.move_progress = 0

    def draw(self, screen, x, y):
        dx = int(self.move_distance * self.move_progress)
        frame = self.frames[self.index]
        screen.blit(frame, (x + dx, y))

    def reset(self):
        self.index = 0
        self.move_progress = 0
        self.forward = True
        self.finished = False
