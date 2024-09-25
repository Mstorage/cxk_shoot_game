import pygame


class GameState:
    """跟踪游戏的进展并统计得分"""
    def __init__(self, ai_setting):
        self.ship_blood = None
        self.ai_setting = ai_setting
        self.formation = ai_setting.fleet_formation
        self.reset_state()

    def reset_state(self):
        self.ship_blood = self.ai_setting.ship_blood

