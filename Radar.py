from Retro3D import *
from Palette import *      
from Mine import *      



###############################################################################
#
###############################################################################
class Radar:


    ###############################################################################
    #
    ###############################################################################
    def __init__(self, image:pg.image, pos_base:pg.math.Vector2):
    
        self.image = image
        self.rect = self.image.get_rect()
        self.pos_base = pg.Vector2(pos_base.x - self.rect.width / 2, pos_base.y - self.rect.height / 2)
        self.pos_center = pg.Vector2(pos_base.x, pos_base.y)

        self.point = pg.Vector2(0.0, 0.0)


    ###############################################################################
    #
    ###############################################################################
    def draw(self, screen:pg.Surface, list_mine:list, cam_pos:pg.math.Vector3, cam_rot:pg.math.Vector3):
        
        screen.blit(self.image, self.pos_base)

        rot_y = (360 - cam_rot.y) + 180
        
        for mine in list_mine:
            if mine.mine_type == Mine.TYPE_SEEKER:
                self.__draw_obj(mine, screen, cam_pos, rot_y, Palette.red, 6)
            else:
                self.__draw_obj(mine, screen, cam_pos, rot_y, Palette.tron_white, 3)


            # dsd draw further out - make max range easy to change
    ###############################################################################
    #
    ###############################################################################
    def __draw_obj(self, obj:Object, screen:pg.Surface, cam_pos:pg.math.Vector3, rot_y: float, color:pg.Color, size:int):

            p = pg.Vector2()
    
            # using x,z of 3d as x,y of 2d
            p.x = ((obj.pos.x - cam_pos.x) * 0.1) * 3.0
            p.y = ((obj.pos.z - cam_pos.z) * 0.1) * -3.0

            # don't draw points outside of radar
            # dsd simathdist
            mag = ((p.x) ** 2) + ((p.y) ** 2)
            if mag > 11500.0:
                return

            # rotate point
            self.point.x = p.x*math.cos(rot_y) - p.y*math.sin(rot_y)
            self.point.y = p.y*math.cos(rot_y) + p.x*math.sin(rot_y)

            self.point.x += self.pos_base.x + self.rect.width / 2
            self.point.y += self.pos_base.y + self.rect.height / 2

            pg.draw.circle(screen, color, self.point, size)    

