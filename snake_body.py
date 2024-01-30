import pygame
from pygame.sprite import Sprite
class SnakeBody(Sprite):
    """管理蛇身的类"""
    
    def __init__(self,es_game):
        """加载蛇身资源"""
        super().__init__()

        #加载屏幕资源
        self.screen = es_game.screen
        self.screen_rect = self.screen.get_rect()

        #加载设置
        self.settings = es_game.settings

        #获取蛇身并初始化其位置
        self.rect = pygame.Rect(0,0,self.settings.snake_size,self.settings.snake_size)
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        #记录当前蛇身方向
        self.direction_x = 1
        self.direction_y = 0

    def update(self):
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_body(self):
        """在屏幕上绘制蛇身"""
        pygame.draw.rect(self.screen,self.settings.snake_body_color,self.rect)