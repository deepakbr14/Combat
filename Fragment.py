from Retro3D import *
from Palette import *       



###############################################################################
#
###############################################################################
class Fragment(Object):


    ###############################################################################
    #
    ###############################################################################
    def __init__(self, model:Model, color:pg.Color, ground_y:float):
    
        super().__init__()

        self.set_model(model, color)
        self.ground_y = ground_y

        self.set_pos(0.0, 0.0, 0.0)
        self.set_rot(0.0, 0.0, 0.0)  
        self.set_scale(0.3)

        self.radius = 1.0

        self.LIFE_MAX = 25
        self.life = 0


    ###############################################################################
    #
    ###############################################################################
    def boom(self, pos:pg.math.Vector3):
      
        self.set_pos(pos.x, pos.y, pos.z)

        self.rot_vel = pg.math.Vector3(-0.06 + (SiRandom.GetFloat() * 0.12) * 2.0,
                                       -0.12 + (SiRandom.GetFloat() * 0.24) * 2.0,
                                        0.0)

        self.vel = pg.math.Vector3(-1.0 + (SiRandom.GetFloat() * 2.0),
                                    1.0 + (SiRandom.GetFloat() * 0.8),
                                   -1.0 + (SiRandom.GetFloat() * 2.0))


        self.life = self.LIFE_MAX



    ###############################################################################
    #
    ###############################################################################
    def update(self):
      
        super().update()

        self.rot += self.rot_vel
        self.pos += self.vel        

        # gravity
        self.vel.y += -0.15

        if self.pos.y < self.ground_y:
            self.pos.y = self.ground_y
            self.vel.x *= 0.5
            self.vel.y *= -0.5
            self.vel.z *= 0.5

        self.life -= 1
        if self.life < 0:
            return True

        return False



