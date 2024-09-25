import pygame

from pygame.sprite import Sprite


class Bullet(Sprite):
    """一个对飞船子弹管理的类"""

    def __init__(self, ai_settings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen
        # 构建子弹形状并获取中心点和顶点坐标
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top
        # 设置子弹的基本属性
        self.position_y = float(self.rect.y)
        self.color = ai_settings.bullet_color
        self.speed = ai_settings.bullet_speed
        # 初始化子弹伤害为设定值
        self.harm = ai_settings.bullet_harm
        # 初始化子弹音效
        self.fire_bullet_sounds = pygame.mixer.Sound("./sounds/ji.mp3")

    def update(self):
        """更新子弹的位置"""
        self.position_y -= self.speed
        self.rect.y = self.position_y

    def draw_bullet(self):
        """画出子弹图形"""
        pygame.draw.rect(self.screen, self.color, self.rect)

