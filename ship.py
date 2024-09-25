import pygame


class Ship:
    """初始化飞船"""

    def __init__(self, screen, ai_setting):
        self.move_right = False
        self.move_left = False
        self.screen = screen
        self.ai_setting = ai_setting

        # 加载飞船图像并获取其外加矩形
        self.image = pygame.image.load('./img/ship_cxk.png')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom
        # 飞船的x位置
        self.center_move = float(self.rect.centerx)

        self.invincible = False
        self.invincible_start_time = 0

    def update(self):
        if self.move_right and self.rect.right < self.screen_rect.right:
            self.center_move += self.ai_setting.speed
        elif self.move_left and self.rect.left > 0:
            self.center_move -= self.ai_setting.speed

        self.rect.centerx = self.center_move

        current_time = pygame.time.get_ticks()

        # 当飞船处于无敌状态时判断是否结束无敌状态
        if self.invincible and current_time - self.invincible_start_time >= 2000:
            self.invincible = False
            self.invincible_start_time = 0
            self.image = pygame.image.load('./img/ship_cxk.png')

    def blit_me(self):
        """在指定位置画出飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center_move = self.screen_rect.centerx
