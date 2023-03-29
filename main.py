from Retro3D import *
from Combat import *
from Palette import *


if __name__ == '__main__':

    # Retro3D engine will use this config to setup basic stuff for your game
    config = ConfigGame()
    config.screen_resolution = pg.math.Vector2(1600, 900)
    config.menu_background_color_top = Palette.tron_teal
    config.menu_background_color_bottom = Palette.tron_black
    config.light_direction = pg.math.Vector3(1.0, 0.0, 0.0)
    config.title = "Combat";
    config.author = "Deepak Deo"
    config.year = "1977"

    config.instructions =  "<Left Arrow>    Turn Left\n\n"
    config.instructions += "<Right Arrow>   Turn Right\n\n"
    config.instructions += "<Space Bar>     Shoot\n\n\n"
    config.instructions += "Don't let the enemies hit you on the way out!\n\n"
    config.instructions += "Points\n"
    config.instructions += "-------------------------\n"
    config.instructions += "Bouncing Balls      " + str(Mine.SCORE_MINE_BOUNCER) + "\n"
    config.instructions += "Dancing Cones       " + str(Mine.SCORE_MINE_SPINNER) + "\n"
    config.instructions += "Death Cubes             " + str(Mine.SCORE_MINE_SEEKER) + "\n\n"
    config.instructions += "Points multiplier if you kill more than one at a time!"

    config.credits = ""
    config.credits += "Sound\n"
    config.credits += "    Music (Spider) by Rob Southworth\n"
    config.credits += "    Fx by Red Sky Sounds\n"
    config.credits += "\n" 
    config.credits += "Fonts\n" 
    config.credits += "     White Rabbit font by Matthew Welch\n"
    config.credits += "\n" 
    config.credits += "Palettes\n" 
    config.credits += "    Tron 1982 by Hilary Baumann\n"
    config.credits += "\n" 
    config.credits += "Software\n" 
    config.credits += "    2d Engine by Pygame\n"
    config.credits += "\n" 
    config.credits += "YouTube\n" 
    config.credits += "    Create, Package & Publish your OWN Python Library by Joshua Lowe\n"
    config.credits += "    Let's code 3D Engine in Python from Scratch by Coder Space\n"
    config.credits += "    Essence of linear algebra by 3Blue1Brown\n"
    config.credits += "    Perspective Projection Matrix by pikuma\n"
    config.credits += "    Rotating Points Using Rotation Matrices by patrickJMT\n"
    config.credits += "    The Math behind (most) 3D games by Brendan Galea\n"
    config.credits += "    Code-It-Yourself! 3D Graphics Engine by javidx9\n"
    config.credits += "\n" 
    config.credits += "Books\n" 
    config.credits += "    Real-Time Rendering by Moller and Haines\n"
    

    game = Combat(config, os.path.dirname(__file__) + os.sep + "rez" + os.sep)
    game.run()


