#导入必要模块
import pygame
import sys
from pygame.sprite import Sprite
from random import randint
from time import sleep
#导入设置
from settings import Settings

#导入游戏对象
from snake_head import SnakeHead
from snake_body import SnakeBody
from food import Food

#导入统计信息
from game_stats import GameStats

class EatSnake:
    """管理贪吃蛇游戏的类"""

    def __init__(self):
        """游戏资源初始化"""
        #创建游戏时钟及设置
        self.clock = pygame.time.Clock()
        self.settings = Settings()

        #建立游戏窗口
        self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        pygame.display.set_caption("Eat Snake")

        #建立统计信息
        self.stats = GameStats()

        #建立初始游戏移动方向
        self.direction_x = self.settings.direction_x
        self.direction_y = self.settings.direction_y

        #建立蛇头
        self.snake_head = SnakeHead(self)

        #建立蛇身
        self.snake_body = pygame.sprite.Group()

        #初始化蛇身
        self.init_link_snake_body()

        #建立食物
        self.food = Food(self)
        self.food_make()

        #游戏状态
        self.game_active = True

    def run_game(self):
        """游戏运行的主程序"""
        while True:
            self._check_event()
            if self.game_active:
                self._snake_update()
                self._check_head_body_collide()
                self._check_eat_food()
                self.update_screen()
            self.clock.tick(60)

    def _check_event(self):
        """检测键盘及鼠标事件"""
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._check_key_down(event)
            elif event.type == pygame.QUIT:
                sys.exit()

    def _check_key_down(self,event):
        if event.key == pygame.K_UP and self.direction_y != 1:
            self.direction_x = 0
            self.direction_y = -1
        elif event.key == pygame.K_DOWN and self.direction_y != -1:
            self.direction_x = 0
            self.direction_y = 1
        elif event.key == pygame.K_LEFT and self.direction_x != 1:
            self.direction_x = -1
            self.direction_y = 0
        elif event.key == pygame.K_RIGHT and self.direction_x != -1:
            self.direction_x = 1
            self.direction_y = 0
        elif event.key == pygame.K_SPACE:
            self.game_active = False
        elif event.key == pygame.K_q:
            sys.exit()

    def init_link_snake_body(self):
        """连接蛇身与蛇头"""
        self.rect = self.snake_head.rect
        for i in range(self.stats.snake_length):
           self._create_new_body()

    def _create_new_body(self):
        """生成新的蛇身"""
        new_body = SnakeBody(self)
        new_body.direction_x = self.direction_x
        new_body.direction_y = self.direction_y
        new_body.x = self.rect.x - self.settings.snake_size - 10
        new_body.y = self.rect.y
        new_body.rect.x = self.rect.x - self.settings.snake_size - 10
        new_body.rect.y = self.rect.y
        self.snake_body.add(new_body)
        self.rect = new_body.rect

    def _snake_update(self):
        """更新蛇"""
        self._change_direction()
        #更新蛇头与蛇身
        self._update_snake_body()
        self.snake_head.update()

    def _change_direction(self):
        """改变蛇头的方向"""
        self.snake_head.direction_x = self.direction_x
        self.snake_head.direction_y = self.direction_y

    def _update_snake_body(self):
        """更新蛇身的位置"""
        temp = self.snake_body.sprites()
        i = len(temp) - 1
        while i:
            temp[i].direction_x = temp[i-1].direction_x
            temp[i].direction_y = temp[i-1].direction_y
            temp[i].x = temp[i-1].x
            temp[i].y = temp[i-1].y
            i -= 1
        temp[0].direction_x = self.direction_x
        temp[0].direction_y = self.direction_y
        temp[0].x = self.snake_head.rect.x
        temp[0].y = self.snake_head.rect.y
        self.snake_body.update()

    def _check_head_body_collide(self):
        """检测蛇的头与身体的碰撞"""
        if pygame.sprite.spritecollideany(self.snake_head,self.snake_body):
            sleep(0.5)
            self.game_active = False

    def food_make(self):
        """随机生成食物"""
        self.food.rect.x = randint(20,self.settings.screen_width-2*self.settings.snake_size)
        self.food.rect.y = randint(20,self.settings.screen_height-2*self.settings.snake_size)
        while pygame.sprite.spritecollideany(self.food,self.snake_body):
            self.food.rect.x = randint(0,self.settings.screen_width)
            self.food.rect.y = randint(0,self.settings.screen_height)

    def _check_eat_food(self):
        """检测食物与蛇头的碰撞"""
        if self.snake_head.rect.colliderect(self.food.rect):
            self.stats.snake_length += 1
            self.food_make()
            self._increase_body()

    def _increase_body(self):
        """吃到食物后加长身体"""
        new_body = SnakeBody(self)
        temp = self.snake_body.sprites()
        number = len(temp)
        new_body.rect.x = temp[number-1].x - self.settings.snake_size*temp[number-1].direction_x
        new_body.rect.y = temp[number-1].y - self.settings.snake_size*temp[number-1].direction_y
        self.snake_body.add(new_body)
    
    def update_screen(self):
        """更新屏幕"""
        #填充屏幕颜色
        self.screen.fill(self.settings.bg_color)
        #绘制蛇头
        self.snake_head.draw_head()
        #绘制蛇身
        for body in self.snake_body.sprites():
            body.draw_body()
        #绘制食物
        self.food.blitme_food()
        #刷新最新屏幕
        pygame.display.flip()

if __name__ == '__main__':
    es_game = EatSnake()
    es_game.run_game()
