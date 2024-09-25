import pygame


class Settings:
    """用于储存游戏设定"""

    def __init__(self):
        # 基础设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        # 飞船设置
        self.speed = 6
        self.ship_blood = 3
        # 子弹设置
        self.bullet_speed = 8
        self.bullet_width = 10
        self.bullet_height = 10
        self.bullet_color = (60, 60, 60)
        self.bullet_number = 5
        self.bullet_harm = 1
        # 外星人设置
        self.alien_speed = 2
        self.alien_blood = 1
        # 设置编队模式
        self.fleet_formation = 1
