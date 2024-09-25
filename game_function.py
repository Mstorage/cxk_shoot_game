import sys

import pygame
from bullet import Bullet
from alien import Alien
from time import sleep


def check_keydown_event(ship, event, bullets, ai_setting, screen):
    """读取按键按下"""
    if event.key == pygame.K_RIGHT:
        ship.move_right = True
    elif event.key == pygame.K_LEFT:
        ship.move_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(bullets, ai_setting, screen, ship)


def check_keyup_event(ship, event):
    """读取按键"""
    if event.key == pygame.K_RIGHT:
        ship.move_right = False
    elif event.key == pygame.K_LEFT:
        ship.move_left = False


def check_event(ai_setting, screen, ship, bullets):
    """读取并响应鼠标键盘输入事件"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_event(ship, event, bullets, ai_setting, screen)

        elif event.type == pygame.KEYUP:
            check_keyup_event(ship, event)


def fire_bullet(bullets, ai_setting, screen, ship):
    """发射子弹，前提是没有超过setting中的限制"""
    if len(bullets) <= ai_setting.bullet_number:
        new_bullet = Bullet(ai_setting, screen, ship)
        bullets.add(new_bullet)
        new_bullet.fire_bullet_sounds.play()


def creat_alien(aliens, ai_setting, screen, alien_number_x, alien_number_y):
    """在指定位置放一个外星图片人"""
    new_alien = Alien(ai_setting, screen)
    alien_width = new_alien.rect.width
    alien_height = new_alien.rect.height

    # 新建的外星人在两边个空半个图片长度的空间内按顺序排列
    new_alien.x = alien_number_x * alien_width + 2 * alien_width
    new_alien.y = alien_number_y * alien_height
    new_alien.rect.x = new_alien.x
    new_alien.rect.y = new_alien.y
    aliens.add(new_alien)


def creat_fleet(aliens, ai_setting, screen, ship, formation_number):
    """创建敌人舰队"""
    alien = Alien(ai_setting, screen)
    alien_numbers_x = get_alien_numbers_x(alien.rect.width, ai_setting)
    alien_numbers_y = get_alien_numbers_y(alien.rect.height, ai_setting, ship.rect.height)

    if formation_number == 1:
        # 循环创建舰队装满一行
        for alien_number_y in range(alien_numbers_y - 8):
            for alien_number_x in range(alien_numbers_x):
                creat_alien(aliens, ai_setting, screen, alien_number_x, alien_number_y)

    elif formation_number == 2:
        # 在偶数偶数列创建舰队
        for alien_number_y in range(alien_numbers_y):
            for alien_number_x in range(alien_numbers_x):
                if alien_number_x % 2 == 0 and alien_number_y % 2 == 0:
                    creat_alien(aliens, ai_setting, screen, alien_number_x, alien_number_y)

    elif formation_number == 3:
        # 在偶数偶数列创建舰队
        for alien_number_y in range(alien_numbers_y):
            for alien_number_x in range(alien_numbers_x):
                if alien_number_x == alien_number_y:
                    creat_alien(aliens, ai_setting, screen, alien_number_x, alien_number_y)


def get_alien_numbers_x(alien_width, ai_setting):
    """获取一行能放下的外星人的个数"""
    alien_space_x = ai_setting.screen_width - 200
    alien_numbers_x = int(alien_space_x / alien_width)
    return alien_numbers_x


def get_alien_numbers_y(alien_height, ai_setting, ship_height):
    """获取整个屏幕能放下多少行外星人"""
    alien_space_y = ai_setting.screen_height - alien_height - 2 * ship_height
    alien_numbers_y = int(alien_space_y / alien_height)
    return alien_numbers_y


# def check_alien_edge(ai_setting, aliens):
#    for alien in aliens.sprites():
#        if alien.check_edge()


def screen_update(ai_setting, screen, ship, bullets, aliens):
    """更新屏幕数据"""
    # screen.fill(ai_setting.bg_color)
    img = pygame.image.load('img/bg.png')
    rect = img.get_rect()
    screen.blit(img, rect)

    # 重绘子弹和飞船
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blit_me()

    # 绘制外星人
    # aliens.draw(screen)
    for alien in aliens.sprites():
        alien.check_edge()
        alien.blit_me()

    # 游戏显示刷新
    pygame.display.flip()


def bullet_update(bullets, aliens):
    bullets.update()

    # 检查是否子弹的位置和外星人发生了重叠
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, False)
    for collisions_bullets, collisions_aliens in collisions.items():
        for collisions_alien in collisions_aliens:
            collisions_alien.blood -= 1

    # 删除已经消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom < 0:
            bullets.remove(bullet)


def alien_update(aliens, screen, ai_setting, ship, state, bullets):
    """更新外星人的位置"""
    aliens.update()
    # 删除血量降到0的外星人,并发出击败音效
    for alien in aliens.copy():
        if alien.blood <= 0:
            aliens.remove(alien)
            alien.alien_dead_sounds.play()

    if len(aliens) == 0:
        creat_fleet(aliens, ai_setting, screen, ship, ai_setting.fleet_formation)
        ai_setting.bullet_speed = 15
        ai_setting.alien_speed = 5
        state.formation += 1
        ai_setting.fleet_formation = state.formation
    # 检查是否有外星人与飞船发生碰撞
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(state, bullets, ship, aliens, ai_setting, screen)
    # 检查是否有外星人到达屏幕底部
    check_aliens_bottom(state, bullets, ship, ai_setting, screen, aliens)


def ship_hit(state, bullets, ship, aliens, ai_setting, screen):
    """当飞船被击中时"""
    # 当飞船不是无敌状态下
    if not ship.invincible:
        if state.ship_blood > 0:
            state.ship_blood -= 1
        else:
            sys.exit()

        # 被击中后清空所有子弹和外星人，暂停0.5秒后使飞船进入无敌时间2秒
        bullets.empty()
        # creat_fleet(aliens, ai_setting, screen, ship, state.formation - 1)
        sleep(0.5)
        # ship.center_ship()
        # 飞船的状态被标记为无敌，无敌时间开始计时
        ship.invincible = True
        ship.invincible_start_time = pygame.time.get_ticks()
        # 飞船图片变成被击中的样子
        ship.image = pygame.image.load('./img/ship_cxk_hitted.png')


def check_aliens_bottom(state, bullets, ship, ai_setting, screen, aliens):
    """检查是否有外星人到达屏幕底部"""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(state, bullets, ship, aliens, ai_setting, screen)
            break
