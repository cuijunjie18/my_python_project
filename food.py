import pygame
class Food:
    """管理食物的类"""

    def __init__(self,es_game):
        """初始化食物资源"""

        #加载屏幕资源
        self.screen = es_game.screen
        self.screen_rect = self.screen.get_rect()

        #加载食物
        self.image = pygame.image.load('images/apple.bmp')
        self.rect = self.image.get_rect()

        #初始化食物的位置
        self.rect.x = 0
        self.rect.y = 0

    def blitme_food(self):
        """在屏幕上绘制食物"""
        self.screen.blit(self.image,self.rect)