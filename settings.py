class Settings:
    """管理设置的类"""

    def __init__(self):
        """游戏设置初始化"""

        #加载屏幕设置
        self.screen_width = 1100
        self.screen_height = 700
        self.bg_color = (230,230,230)

        #加载蛇的设置
        self.snake_size = 10
        self.snake_speed = 10
        self.snake_head_color = (255,0,0)
        self.snake_body_color = (125,0,0)
        self.direction_x = 1
        self.direction_y = 0

        #加载食物设置
        self.food_size = 30
        self.food_color = (60,0,0)
        