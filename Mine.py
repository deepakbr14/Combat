from Retro3D import *
from Palette import *       



###############################################################################
#
###############################################################################
class Mine(Object):

    TYPE_BOUNCER            = 0
    TYPE_SPINNER            = 1
    TYPE_SEEKER             = 2
    TYPE_MAX                = 3

    #dsd dcit?!
    SCORE_MINE_BOUNCER = 3
    SCORE_MINE_SPINNER = 10
    SCORE_MINE_SEEKER  = 1

    ###############################################################################
    #
    ###############################################################################
    def __init__(self, mine_type:int, model:Model, speed_mult:float, pos:pg.math.Vector3, pos_target:pg.math.Vector3, ground_y:float):
    
        super().__init__()

        self.mine_type = mine_type
        if self.mine_type == Mine.TYPE_BOUNCER:
            color = Palette.tron_white
            self.move_speed = 1.0 + (SiRandom.GetFloat() * 1.5) * speed_mult
            self.vel = (pos_target - pos).normalize() * self.move_speed
            self.vel.y = 0.5 + (SiRandom.GetFloat() * 1.75)        
            self.rot_vel = pg.math.Vector3(self.vel.x * 0.1,
                                           self.vel.y * 0.1,
                                           self.vel.z * 0.1)

        elif self.mine_type == Mine.TYPE_SPINNER:
            color = Palette.tron_teal
            self.move_speed = 0.2 + (SiRandom.GetFloat() * 0.4) * speed_mult
            self.vel = (pos_target - pos).normalize() * self.move_speed
            self.rot_vel = pg.math.Vector3(-0.1 + (SiRandom.GetFloat() * 0.2), -0.2 + (SiRandom.GetFloat() * 0.6), 0.0)

        elif self.mine_type == Mine.TYPE_SEEKER:
            color = Palette.red
            self.move_speed = 0.3 + (SiRandom.GetFloat() * 1.0) * speed_mult
            self.vel = (pos_target - pos).normalize() * self.move_speed
            self.rot_vel = pg.math.Vector3(0.0, -0.1 + (SiRandom.GetFloat() * 0.2), 0.0)

        else:
            SiLog.Unsupported(self.mine_type)  


        self.set_model(model, color)

        self.ground_y = ground_y

        self.set_pos(pos.x, pos.y, pos.z)
        self.set_rot(0.0, 0.0, 0.0)  

        s = 1.5 + (SiRandom.GetFloat() * 5.0)
        self.set_scale(s)
        self.radius = 500.0 + (40.0 * s)

        self.pos_target = pos_target

    ###############################################################################
    #
    ###############################################################################
    def update(self, camera_pos:pg.math.Vector3):
      
        super().update()


        if self.mine_type == Mine.TYPE_BOUNCER:
            self.vel.y += -0.1

            if self.pos.y < self.ground_y:
                self.pos.y = self.ground_y
                self.vel.y *= -0.95

            self.pos += self.vel
            self.rot += self.rot_vel

        elif self.mine_type == Mine.TYPE_SPINNER:

            self.rot += self.rot_vel

            self.pos.x += math.sin(self.rot.x) * 2.0
            self.pos.z += math.cos(self.rot.y) * 2.0
            self.pos += self.vel

        elif self.mine_type == Mine.TYPE_SEEKER:

            self.pos += self.vel
            self.rot += self.rot_vel

        return False


    ###############################################################################
    #
    ###############################################################################
    def get_score_value(self):

        if self.mine_type == Mine.TYPE_BOUNCER:
            return Mine.SCORE_MINE_BOUNCER
        elif self.mine_type == Mine.TYPE_SPINNER:
            return Mine.SCORE_MINE_SPINNER
        elif self.mine_type == Mine.TYPE_SEEKER:
            return Mine.SCORE_MINE_SEEKER
        else:
            SiLog.Unsupported(self.mine_type) 
