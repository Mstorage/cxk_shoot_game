import pygame

from pygame.sprite import Sprite


class Alien(Sprite):
    """表示单个外星人的类"""

    def __init__(self, ai_setting, screen):
        """初始化外星人属性及位置"""
        super().__init__()
        self.images = {}
        self.ai_setting = ai_setting
        self.screen = screen
        self.screen_rect = screen.get_rect()
        # 读取外星人的图片并且获得图片的外方框高度
        self.images[0] = pygame.image.load("./img/alien_50.png")
        self.images[1] = pygame.image.load("./img/alien_100.png")

        self.image = self.images[0]
        self.rect = self.image.get_rect()
        # 外星人的中点坐标，为rect长宽的中点
        self.rect.x = self.rect.width / 2
        self.rect.y = self.rect.height / 2
        # 外星人的横向移动方向，True为向右移动，False为向左移动
        self.move_direction = True
        # 初始化外星人的血量为设定值
        self.blood = ai_setting.alien_blood
        # 初始化外星人击败有效
        self.alien_dead_sounds = pygame.mixer.Sound("./sounds/niganma.mp3")

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def alien_close(self):
        self.rect.y += self.rect.height

    def check_edge(self):
        if self.rect.right >= self.screen_rect.right:
            self.move_direction = False
            self.alien_close()
        elif self.rect.left < 0:
            self.move_direction = True
            self.alien_close()

    def update(self):
        if self.move_direction:
            self.x += self.ai_setting.alien_speed
        else:
            self.x -= self.ai_setting.alien_speed
        self.rect.x = self.x

    def blit_me(self):
        """在指定位置绘制外星人"""
        self.screen.blit(self.image, self.rect)

