from Retro3D import *
from Palette import *       



###############################################################################
#
###############################################################################
class ScoreBar:


    ###############################################################################
    #
    ###############################################################################
    def __init__(self,  image:pg.image, pos_base:pg.math.Vector2, font_med:pg.font, font_small:pg.font):  #dsd spacing on all function param pairs
    
        self.image = image
        rect = self.image.get_rect()
        self.pos_text = pg.Vector2(pos_base.x, pos_base.y - 15)
        self.pos_base = pg.Vector2(pos_base.x - rect.width / 2, pos_base.y - rect.height / 2)

        self.font_score = font_med
        self.font_high_score = font_small

    ###############################################################################
    #
    ###############################################################################
    def draw(self, screen: pg.Surface, score: int, high_score: int):
       
        # draw score bar
        screen.blit(self.image, self.pos_base)

        # draw score
        # NOTE: "{:,}".format(5000000) formats the int with commas
        text_surface = self.font_score.render("{:,}".format(score), True, Palette.tron_white)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.pos_text.x, self.pos_text.y)
        screen.blit(text_surface, text_rect)

        # draw high score
        text_surface = self.font_high_score.render("HIGH SCORE", True, Palette.tron_teal)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.pos_text.x - 65, self.pos_text.y + 50)
        screen.blit(text_surface, text_rect)

        text_surface = self.font_high_score.render("{:,}".format(high_score), True, Palette.tron_black)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (self.pos_text.x + 45, self.pos_text.y + 50)
        screen.blit(text_surface, text_rect)
