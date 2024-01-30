import pygame.font
class ScoreBoard:
    """管理得分的类"""

    def __init__(self,es_game):
        """初始化得分板"""

        #加载屏幕
        self.screen = es_game.screen
        self.screen_rect = self.screen.get_rect()

        #加载设置及统计信息
        self.settings = es_game.settings
        self.stats = es_game.stats
        self.es_game = es_game

        #加载显示得分的颜色及字体
        self.text_color = (30,30,30)
        self.font = pygame.font.SysFont(None,28)

        #渲染图像
        self.prep_score()

    def prep_score(self):
        """渲染分数图像"""
        #获取图像
        score_str = f"Score:{str(self.stats.score)}"
        self.image = self.font.render(score_str,True,self.text_color,self.settings.bg_color)
        self.rect = self.image.get_rect()
        #初始化位置
        self.rect.right = self.screen_rect.right - 30
        self.rect.top = 10
    
    def show_score(self):
        """将得分展示在屏幕"""
        self.screen.blit(self.image,self.rect)
