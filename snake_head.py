import pygame
class SnakeHead:
    """管理蛇头的类"""

    def __init__(self,es_game):
        """蛇头资源初始化"""

        #加载屏幕
        self.screen = es_game.screen
        self.screen_rect = self.screen.get_rect()

        #加载设置
        self.settings = es_game.settings

        #获取蛇头信息
        self.rect = pygame.Rect(0,0,self.settings.snake_size,self.settings.snake_size)
        
        #初始化蛇头位置
        self.rect.center = self.screen_rect.center
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        #获取蛇头移动方向
        self.direction_x = es_game.direction_x
        self.direction_y = es_game.direction_y

    def update(self):
        """更新蛇头位置"""
        self.x += self.direction_x*self.settings.snake_speed
        self.y += self.direction_y*self.settings.snake_speed
        if self.x >= self.settings.screen_width:
            self.x -= self.settings.screen_width
        if self.x <= 0:
            self.x += self.settings.screen_width
        if self.y >= self.settings.screen_height:
            self.y -=self.settings.screen_height
        if self.y <= 0:
            self.y += self.settings.screen_height
        self.rect.x = self.x
        self.rect.y = self.y

    def draw_head(self):
        """绘制蛇头"""
        pygame.draw.rect(self.screen,self.settings.snake_head_color,self.rect)
