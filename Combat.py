from Retro3D import *
from Palette import *       
from Scope import *       
from ScoreBar import *       
from Mine import *       
from Radar import *       
from Fragment import *       



###############################################################################
#
###############################################################################
class Combat(Game):

    REZ_MUSIC_SPIDER      = "Spider.wav"
    REZ_SFX_GAME_OVER     = "Explosion2.wav"
    REZ_SFX_SHOOT         = "Gun9.wav"
    REZ_SFX_TARGET_KILL_A = "TargetDeathA.wav"
    REZ_SFX_TARGET_KILL_B = "TargetDeathB.wav"
    REZ_SFX_LAUNCH_SEEKER = "MineLaunchSeeker.wav"

    REZ_FONT_WHITE_RABBIT = "WhiteRabbit.ttf"

    REZ_MODEL_CONE          = "cone" + os.sep + "cone.obj"
    REZ_MODEL_CUBE          = "cube" + os.sep + "cube.obj"
    REZ_MODEL_ICOSPHERE     = "icosphere" + os.sep + "icosphere.obj"

    REZ_IMAGE_SCOPE         = "scope.png"
    REZ_IMAGE_SCORE_BAR     = "score_bar.png"
    REZ_IMAGE_RADAR         = "radar.png"


    high_score = 0


    ###############################################################################
    #
    # need to override so you can initialize your game with your stuff
    #
    ###############################################################################
    def __init__(self, config: ConfigGame, fpath_base:str):
    
        super().__init__(config, fpath_base)

        SiRandom.Seed(0)

        #dsd support built in score board for game
        # storing player scores
        self.score = 0;
        self.speed_mult = 1.0
        	
        # camera info
        self.camera_pos = pg.math.Vector3(0.0, 1.0, -10.0)
        self.camera_rot = pg.math.Vector3(0.0, 0.0, 0.0)

        # 3d ground y
        self.ground_y = 2.0

        # player movement info
        self.player_rot_speed = 0.015

        # size of space where enemies are spawned
        self.floor_y = +0.5
        self.play_area_min = pg.math.Vector3(-100.0, self.floor_y, -100.0)
        self.play_area_max = pg.math.Vector3(100.0, self.floor_y, 100.0)
        self.play_area_diff = pg.math.Vector3(self.play_area_max.x - self.play_area_min.x,
                                        self.play_area_max.y - self.play_area_min.y,
                                        self.play_area_max.z - self.play_area_min.z)


        self.rez.set_music(Combat.REZ_MUSIC_SPIDER) 

        self.rez.add_sound(Combat.REZ_SFX_GAME_OVER)
        self.rez.add_sound(Combat.REZ_SFX_SHOOT)
        self.rez.add_sound(Combat.REZ_SFX_TARGET_KILL_A)
        self.rez.add_sound(Combat.REZ_SFX_TARGET_KILL_B)
        self.rez.add_sound(Combat.REZ_SFX_LAUNCH_SEEKER)


        # load models
        self.rez.add_model(Combat.REZ_MODEL_CONE)
        self.rez.add_model(Combat.REZ_MODEL_CUBE)
        self.rez.add_model(Combat.REZ_MODEL_ICOSPHERE)

        # load fonts
        # dsd would like to see these loaded/stored/controlled from inside of rez
        #       got a bit difficult because of the font name + font size
        self.font_fixed_med = self.rez.create_font(Combat.REZ_FONT_WHITE_RABBIT, 40)
        self.font_fixed_small = self.rez.create_font(Combat.REZ_FONT_WHITE_RABBIT, 20)

        # load images
        self.rez.add_image(Combat.REZ_IMAGE_SCOPE)
        self.rez.add_image(Combat.REZ_IMAGE_SCORE_BAR)
        self.rez.add_image(Combat.REZ_IMAGE_RADAR)

        # initalize lists for explosion fragments
        self.NUM_FRAGMENT_MAX = 20
        self.list_fragment = list()
        self.list_fragment_active = list()
        for i in range(self.NUM_FRAGMENT_MAX):
            fragment = Fragment(self.rez.get_model(Combat.REZ_MODEL_CUBE), Palette.tron_white, self.ground_y)  
            self.list_fragment.append(fragment)

        # initalize list for 'mines' (cones, cubes, icospheres)
        self.NUM_MINE_MAX = 3       #dsd 3
        self.list_mine = list()


        # setup background sky
        self.background_rect_sky = pg.Rect(0, 0, config.screen_resolution.x, config.screen_resolution.y * 0.30)
        self.background_ground_y = config.screen_resolution.y * 0.50
        self.background_rect_horizon = pg.Rect(0, config.screen_resolution.y * 0.30, config.screen_resolution.x, config.screen_resolution.y * 0.20)
        self.background_rect_ground = pg.Rect(0, config.screen_resolution.y * 0.50, config.screen_resolution.x, self.background_ground_y)

        # generate mountains via 2d lines
        self.generate_mountains()
 
        # setup hud
        self.scope = Scope(self.rez.get_image(Combat.REZ_IMAGE_SCOPE), pg.math.Vector2(config.screen_resolution.x * 0.5, config.screen_resolution.y * 0.5))
        self.score_bar = ScoreBar(self.rez.get_image(Combat.REZ_IMAGE_SCORE_BAR), pg.math.Vector2(config.screen_resolution.x * 0.9, config.screen_resolution.y * 0.1), self.font_fixed_med, self.font_fixed_small)
        self.radar = Radar(self.rez.get_image(Combat.REZ_IMAGE_RADAR), pg.math.Vector2(config.screen_resolution.x * 0.90, config.screen_resolution.y * 0.85))

        self.rez.play_music()

        # game needs to tell engine to start menu mode        
        self.game_state = Game.STATE_MENU




    ###############################################################################
    #
    # dsd line list does some retracing - guessing it's
    #     faster sending a line strip - but maybe not?
    #
    ###############################################################################
    def generate_mountains(self):

        self.mountains_pos_min = 0.0

        x = self.mountains_pos_min
        base_y = self.background_ground_y - 2
        y = base_y

        dist_x_min = 50
        dist_x_max = 300

        dist_y_min = 50
        dist_y_max = 200

        self.list_mountain_lines_primary = list()
        self.list_mountain_lines_primary.append(pg.math.Vector2(x, y))

        RETRACE_COUNT_MAX = 3
        retrace_count = 0
        was_last_slope_up = False

        # slope up of mountain
        x += SiRandom.GetInt(dist_x_min, dist_x_max)
        y -= SiRandom.GetInt(dist_y_min, dist_y_max)
        was_last_slope_up = True
        self.list_mountain_lines_primary.append(pg.math.Vector2(x, y))

        for idx in range(50):
            # calc new x,y

            if retrace_count > 0:
                retrace_count -= 1

            if y == base_y:

                # on ground

                lp = self.list_mountain_lines_primary[idx]

                frander = SiRandom.GetFloat()
                if frander < 0.5 and was_last_slope_up == False:
                    # slope up of mountain
                    x += SiRandom.GetInt(dist_x_min, dist_x_max)
                    y -= SiRandom.GetInt(dist_y_min, dist_y_max)
                    was_last_slope_up = True
                elif frander < 0.8 and retrace_count == 0 and lp.y != base_y:
                    # trace back up last slope to start a new 'behind' mountain
                    x = (lp.x + x) / 2 
                    y = (lp.y + y) / 2 
                    was_last_slope_up = False
                    retrace_count = RETRACE_COUNT_MAX
                else:
                    # straight of a valley
                    x += SiRandom.GetInt(dist_x_min, dist_x_max)
                    was_last_slope_up = False

            else: 

                # we are at a peak
                
                rander = SiRandom.GetInt(0, 2)

                if rander == 0 and retrace_count == 0:
                    # go across
                    x += SiRandom.GetInt(dist_x_min, dist_x_max)
                    was_last_slope_up = False

                elif rander == 1 and was_last_slope_up == False:
                    # go up
                    x += SiRandom.GetInt(dist_x_min, dist_x_max)
                    y -= SiRandom.GetInt(dist_y_min, dist_y_max)
                    was_last_slope_up = True

                else:
                    # go down
                    x += SiRandom.GetInt(dist_x_min, dist_x_max)
                    was_last_slope_up = False

                    y = base_y

                    
            self.list_mountain_lines_primary.append(pg.math.Vector2(x, y))

        # make sure last leg is down!
        if y != base_y:
            x += SiRandom.GetInt(dist_x_min, dist_x_max)
            y = base_y
            self.list_mountain_lines_primary.append(pg.math.Vector2(x, y))

        # dsd what idiot math is this?!
        self.mountains_pos_max = x * 0.75

        # and one line all the way back to start
        x = 0
        y = base_y
        self.list_mountain_lines_primary.append(pg.math.Vector2(x, y))

        # center mountain lines 
        self.mountains_pos = self.mountains_pos_max / 2
        for v in self.list_mountain_lines_primary:
            v.x += -self.mountains_pos



    ###############################################################################
    #
    ###############################################################################
    def move_mountains(self, dir):

        self.mountains_pos += dir

        if self.mountains_pos <= self.mountains_pos_min:
            self.mountains_pos = self.mountains_pos_min
            return

        if self.mountains_pos >= self.mountains_pos_max:
            self.mountains_pos = self.mountains_pos_max
            return

        # move the mountain lines 
        for v in self.list_mountain_lines_primary:
            v.x += dir



    ###############################################################################
    #
    # need to override if you want to get user input
    # 
    ###############################################################################
    def get_player_input(self):

        super().get_player_input()

        if self.is_key_down(pg.K_LEFT) or self.is_key_down(pg.K_RIGHT):
         
            if self.is_key_down(pg.K_LEFT):
                vel = -self.player_rot_speed;
            else:
                vel = self.player_rot_speed;

            # rotate camera
            self.camera_rot.y += vel
    
        # update mountain lines
        # (heh sounds like move mountain lions)
        if self.is_key_down(pg.K_LEFT):
            self.move_mountains(+30)
        elif self.is_key_down(pg.K_RIGHT):
            self.move_mountains(-30)

        # check player shooting
        if self.was_space_hit:

            self.scope.shoot()

            hit_something = False

            # destroy any mines in the crosshairs
            score_adj = 0
            num_hit = 0
            i = 0
            while i < len(self.list_mine):
                mine = self.list_mine[i]
                vec_to_target = (mine.pos - self.engine.camera.pos).normalize()
                vec_to_target = [vec_to_target.x, vec_to_target.y, vec_to_target.z]
                cam_forward = [self.engine.camera.forward.x, self.engine.camera.forward.y, self.engine.camera.forward.z]
                dp = np.dot(vec_to_target, cam_forward)
                if dp > 0.995:           
                    score_adj += mine.get_score_value()

                    self.speed_mult += 0.1
                    if self.speed_mult > 5.0:
                        self.speed_mult = 5.0

                    hit_something = True
                    self.__boom(mine.pos)
                    self.engine.remove_display_object(mine)
                    del self.list_mine[i]

                    num_hit += 1
                else:
                    i += 1

            if hit_something == False:
                self.rez.play_sound(Combat.REZ_SFX_SHOOT)

            if score_adj > 0:
                self.score += score_adj * num_hit
                if self.score > Combat.high_score:
                    Combat.high_score = self.score

            
        # update camera based on input
        self.engine.camera.rot = self.camera_rot


    ###############################################################################
    #
    ###############################################################################
    def __boom(self, pos:pg.math.Vector3):

        num = 7
        if num > len(self.list_fragment):
            num = len(self.list_fragment)

        for i in range(num):
            f = self.list_fragment.pop()
            f.boom(pos)
            self.list_fragment_active.append(f)
            self.engine.add_display_object(f, Engine.DISPLAY_LIST_WIREFRAME)

        rander = SiRandom.GetInt(0, 1)
        if rander == 0:
            self.rez.play_sound(Combat.REZ_SFX_TARGET_KILL_A)
        else:
            self.rez.play_sound(Combat.REZ_SFX_TARGET_KILL_B)


    ###############################################################################
    #
    # need to override so you can update 3d objects
    #
    ###############################################################################
    def update(self):
        
        # dsd use engine's delta_time for frame rate independence!

        if super().update() == False:
            return


        # create new mines if not enuf in world
        if len(self.list_mine) < self.NUM_MINE_MAX:
            pos = self.calc_starting_pos_enemy()

            # dsd wanted to do this stuff inside of the mine class
            #   but ended up in python circular import hell... need to figure this shit out
            #   had to do with the fact that i was passing combat into mine so it could play any required sounds and choose its own model.
            #   then i ended up with combat including mine and mine including combat..
            mine_type = SiRandom.GetInt(0, Mine.TYPE_MAX - 1)
            if mine_type == Mine.TYPE_BOUNCER:
                model = self.rez.get_model(Combat.REZ_MODEL_ICOSPHERE)
            elif mine_type == Mine.TYPE_SPINNER:
                model = self.rez.get_model(Combat.REZ_MODEL_CONE)
            elif mine_type == Mine.TYPE_SEEKER:
                model = self.rez.get_model(Combat.REZ_MODEL_CUBE)
                self.rez.play_sound(Combat.REZ_SFX_LAUNCH_SEEKER)
            else:
                SiLog.Unsupported(self.mine_type)
    
            mine = Mine(mine_type, model, self.speed_mult, pos, self.camera_pos, self.ground_y) 
            self.list_mine.append(mine)
            self.engine.add_display_object(mine, Engine.DISPLAY_LIST_SHADED_OUTLINE)

        # update existing mines
        i = 0
        while i < len(self.list_mine):
            mine = self.list_mine[i]
            mine.update(self.camera_pos)

            if self.has_collided_with_player(mine):                
                self.end_game()

            # this works because all of the mine are created out in +z and come towards player (at 0,0,0)
            if mine.pos.z < self.camera_pos.z - 150.0:           
                hit_something = True
                self.engine.remove_display_object(mine)
                del self.list_mine[i]
            else:
                i += 1


        # update fragments
        list_new = list()
        for f in self.list_fragment_active:
            if f.update() == True:
                self.engine.remove_display_object(f)
                self.list_fragment.append(f)
            else:
                list_new.append(f)
    
        # dsd ugh - there must be a better way
        self.list_fragment_active = list_new

        self.scope.update()

    ###############################################################################
    #
    ###############################################################################
    def end_game(self):

        if self.game_state == Game.STATE_GAME_OVER:
            return

        self.game_state = Game.STATE_GAME_OVER
        self.rez.stop_music()

        self.rez.play_sound(Combat.REZ_SFX_GAME_OVER)


    ###############################################################################
    #
    # dsd be nice to have collision system built into engine dsd doc in readme - all of these
    #
    ###############################################################################
    def has_collided_with_player(self, obj: Object):
        
        # not using sqrt on purpose (time saver!)
        dist = ((self.camera_pos.x - obj.pos.x) ** 2 + (self.camera_pos.y - obj.pos.y) ** 2 + ((self.camera_pos.z) - obj.pos.z) ** 2)
        if dist < obj.radius:
            return True

        return False



    ###############################################################################
    #
    # override this if you want something other than the default background
    # 
    ###############################################################################
    def draw_background(self):  
    
        super().draw_background()

        # sky + horizon + ground
        self.engine.draw_rect_gradient(Palette.tron_white, Palette.tron_teal, self.background_rect_sky, SiDirection.VERTICAL)
        self.engine.draw_rect_gradient(Palette.tron_teal, Palette.tron_med_blue, self.background_rect_horizon, SiDirection.VERTICAL)
        self.engine.draw_rect_gradient(Palette.tron_black, Palette.tron_med_blue, self.background_rect_ground, SiDirection.VERTICAL)

        # mountains in the distance
        pg.draw.lines(self.engine.screen, Palette.tron_white, False, self.list_mountain_lines_primary, 1)

        

    ###############################################################################
    #
    # override this if you want a HUD for your game
    #
    ###############################################################################
    def draw_hud(self):

        super().draw_hud()
        
        self.scope.draw(self.engine.screen)
        self.score_bar.draw(self.engine.screen, self.score, Combat.high_score)
        self.radar.draw(self.engine.screen, self.list_mine, self.camera_pos, self.camera_rot)

      
    ###############################################################################
    # 
    # override this is you want anything extra drawn on game over
    #
    ###############################################################################
    def draw_game_over(self):  
 
        super().draw_game_over()

        # draw crack lines

        #force fixed seed to make a steady crack pattern
        SiRandom.Seed(5)

        x = self.engine.screen_res.x // 2
        y = self.engine.screen_res.y // 2

        self.draw_crack(3, x, y)

        SiRandom.Seed(0)


    ###############################################################################
    #
    # recursive crack drawer
    #
    # NOTE: used chatgpt3+ to write this function :O
    #
    ###############################################################################
    def draw_crack(self, num_bifurcations, x, y):
        
        if num_bifurcations <= 0:
            return

        crack_len = 600

        # create multiple cracks from the starting point
        num_cracks = random.randint(2, 5)

        for i in range(num_cracks):
            last_adj_x = 0
            last_adj_y = 0

            # determine random direction for each crack
            if i % 2 == 0:
                adj_x = random.randint(-crack_len, 0)
            else:
                adj_x = random.randint(0, crack_len)

            if i % 3 == 0:
                adj_y = random.randint(-crack_len, 0)
            else:
                adj_y = random.randint(0, crack_len)

            v1 = pg.math.Vector2(x, y)
            v2 = pg.math.Vector2(x + adj_x, y + adj_y)

            pg.draw.line(self.engine.screen, Palette.red, v1, v2, 1)

            self.draw_crack(num_bifurcations - 1, v2.x, v2.y)


        
    ###############################################################################
    #
    ###############################################################################
    def calc_starting_pos_enemy(self):

        # spawn out in front of player

        # dsd ugh
        pos = pg.math.Vector3(self.camera_pos.x, self.camera_pos.y, self.camera_pos.z)
        if SiRandom.GetTrueFalse():
            pos.x += -30.0 - (SiRandom.GetFloat() * 60.0)
        else:
            pos.x += +30.0 + (SiRandom.GetFloat() * 60.0)

        pos.y = 1.5 #dsd
        pos.z += 250.0 + (SiRandom.GetFloat() * 100.0)

        return pos
        #dsd pos generation should not be on top of player
        #dsd play area?!
#        return pg.math.Vector3(self.play_area_min.x + (self.play_area_diff.x * SiRandom.GetFloat()),
 #                        self.play_area_min.y + (self.play_area_diff.y * SiRandom.GetFloat()),
  #                       self.play_area_min.z + (self.play_area_diff.z * SiRandom.GetFloat()))

