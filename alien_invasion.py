import pygame

from ship import Ship
from settings import Settings
from pygame.sprite import Group
import game_function as gf
from game_state import GameState
from alien import Alien


def run_game():
    # 初始化游戏并创建一个屏幕对象
    ai_setting = Settings()
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption("打飞机")

    # 创建我们的飞船
    ship = Ship(screen, ai_setting)
    # 创建储存子弹的组
    bullets = Group()
    # 创建外星人
    aliens = Group()
    gf.creat_fleet(aliens, ai_setting, screen, ship, 2)
    # 创建游戏状态类对象
    state = GameState(ai_setting)

    print("游戏开始")

    # 开始游戏的主循环
    while True:
        gf.check_event(ai_setting, screen, ship, bullets)
        ship.update()
        gf.alien_update(aliens, screen, ai_setting, ship, state, bullets)
        gf.bullet_update(bullets, aliens)

        gf.screen_update(ai_setting, screen, ship, bullets, aliens)
        # 让最近绘制的屏幕可见


run_game()
