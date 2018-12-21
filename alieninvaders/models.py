"""
Models module for Alien Invaders

This module contains the model classes for the Alien Invaders game. Anything that you
interact with on the screen is model: the ship, the laser bolts, and the aliens.

Just because something is a model does not mean there has to be a special class for
it.  Unless you need something special for your extra gameplay features, Ship and Aliens
could just be an instance of GImage that you move across the screen. You only need a new 
class when you add extra features to an object. So technically Bolt, which has a velocity, 
is really the only model that needs to have its own class.

With that said, we have included the subclasses for Ship and Aliens.  That is because
there are a lot of constants in consts.py for initializing the objects, and you might
want to add a custom initializer.  With that said, feel free to keep the pass underneath 
the class definitions if you do not want to do that.

You are free to add even more models to this module.  You may wish to do this when you 
add new features to your game, such as power-ups.  If you are unsure about whether to 
make a new class or not, please ask on Piazza.

# Sean Yoo (sy435)
# 12/3/2018
"""
from consts import *
from game2d import *

# PRIMARY RULE: Models are not allowed to access anything in any module other than 
# consts.py.  If you need extra information from Gameplay, then it should be
# a parameter in your method, and Wave should pass it as a argument when it
# calls the method.


class Ship(GImage):
    """
    A class to represent the game ship.
    
    At the very least, you want a __init__ method to initialize the ships dimensions.
    These dimensions are all specified in consts.py.
    
    You should probably add a method for moving the ship.  While moving a ship just means
    changing the x attribute (which you can do directly), you want to prevent the player
    from moving the ship offscreen.  This is an ideal thing to do in a method.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like animation). If you add attributes, list them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getx(self):
        """
        Returns the attribute x.

        This method returns the attribute x directly.  Any changes 
        made will modify x.
        """
        return self.x

    def gety(self):
        """
        Returns the attribute y.

        This method returns the attribute y directly.  Any changes 
        made will modify y.
        """
        return self.y

    def setx(self, x):
        """
        Sets attribute x with given x.

        This method will take a given x and set the attribute x.
        
        Parameter: x is an x coordinate
        Precondition: x is a num, 0 <= x <= GAME_WIDTH
        """
        assert (type(x) == int or type(x) == float)
        assert (x>=0 and x <= GAME_WIDTH)
        self.x = x
    
    # INITIALIZER TO CREATE A NEW SHIP
    def __init__(self, x, y):
        """
        Initializes a new Ship class.

        Parameter x: x position of Ship
        Precondition: x is an int, 0 + (SHIP_WIDTH/2) <= x <= GAME_WIDTH - 
        (SHIP_WIDTH/2)

        Parameter y: y position of Ship
        Precondition: y is an int, 0 + (SHIP_HEIGHT/2) <= y <= GAME_HEIGHT - 
        (SHIP_HEIGHT/2)
        """
        assert (type(x) == int or type(x) == float) and (0 + (
            SHIP_WIDTH/2) <= x 
        <= GAME_WIDTH - (SHIP_WIDTH/2))
        assert (type(y) == int or type(y) == float) and (0 + (
            SHIP_HEIGHT/2) <= y 
        <= GAME_HEIGHT - (SHIP_HEIGHT/2))
        super().__init__(x=x, y=y, width=SHIP_WIDTH, height=
        SHIP_HEIGHT, source='ship.png')
    
    # METHODS TO MOVE THE SHIP AND CHECK FOR COLLISIONS
    def collides(self, bolt):
        """
        Returns: True if the bolt was fired by the alien and collides with this 
        ship
            
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        notfiredbyplayer = not bolt.isplayer()
        a = self.contains((bolt.x-(BOLT_WIDTH/2), bolt.y+(BOLT_HEIGHT/2)))
        b = self.contains((bolt.x-(BOLT_WIDTH/2), bolt.y-(BOLT_HEIGHT/2)))
        c = self.contains((bolt.x+(BOLT_WIDTH/2), bolt.y+(BOLT_HEIGHT/2)))
        d = self.contains((bolt.x-(BOLT_WIDTH/2), bolt.y-(BOLT_HEIGHT/2)))
        if notfiredbyplayer and (a or b or c or d):
            return True
        return False
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY


class Alien(GImage):
    """
    A class to represent a single alien.
    
    At the very least, you want a __init__ method to initialize the alien dimensions.
    These dimensions are all specified in consts.py.
    
    You also MIGHT want to add code to detect a collision with a bolt. We do not require
    this.  You could put this method in Wave if you wanted to.  But the advantage of 
    putting it here is that Ships and Aliens collide with different bolts.  Ships 
    collide with Alien bolts, not Ship bolts.  And Aliens collide with Ship bolts, not 
    Alien bolts. An easy way to keep this straight is for this class to have its own 
    collision method.
    
    However, there is no need for any more attributes other than those inherited by
    GImage. You would only add attributes if you needed them for extra gameplay
    features (like giving each alien a score value). If you add attributes, list
    them below.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _sound: Sound for when destroyed [Sound]
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def getx(self):
        """
        Returns the attribute x.

        This method returns the attribute x directly.  Any changes 
        made will modify x.
        """
        return self.x

    def gety(self):
        """
        Returns the attribute y.

        This method returns the attribute y directly.  Any changes 
        made will modify y.
        """
        return self.y

    def setx(self, x):
        """
        Sets attribute x with given x.

        This method will take a given x and set the attribute x.
        
        Parameter: x is an x coordinate
        Precondition: x is a num, 0 <= x <= GAME_WIDTH
        """
        assert (type(x) == int or type(x) == float)
        assert (x>=0 and x <= GAME_WIDTH)
        self.x = x

    def sety(self, y):
        """
        Sets attribute y with given y.

        This method will take a given y and set the attribute y.
        
        Parameter: y is a y coordinate
        Precondition: y is a num, 0 <= y <= GAME_HEIGHT
        """
        assert (type(y) == int or type(y) == float)
        assert (y>=0 and y <= GAME_HEIGHT)
        self.y = y
    
    # INITIALIZER TO CREATE AN ALIEN
    def __init__(self, x, y, src):
        """
        Initializes a new Alien class.

        Alien is a subclass of GImage. Extra attribute _sound is set as a
        Sound object with wavefile 'pop1.wave'.

        Parameter x: x position of Alien
        Precondition: x is an int, 0 + (ALIEN_WIDTH/2) <= x <= GAME_WIDTH - 
        (ALIEN_WIDTH/2)

        Parameter y: y position of Alien
        Precondition: y is an int, 0 + (ALIEN_HEIGHT/2) <= y <= GAME_HEIGHT - 
        (ALIEN_HEIGHT/2)

        Parameter src: src of image for Alien
        Precondition: src is a string
        """
        assert (type(x) == int or type(x) == float) and (0 + (
            ALIEN_WIDTH/2) <= x 
        <= GAME_WIDTH - (ALIEN_WIDTH/2))
        assert (type(y) == int or type(y) == float) and (0 + (
            ALIEN_HEIGHT/2) <= y 
        <= GAME_HEIGHT - (ALIEN_HEIGHT/2))
        assert type(src) == str
        super().__init__(x=x, y=y, width=ALIEN_WIDTH, height=
        ALIEN_HEIGHT, source=src)

        self._sound = Sound('pop1.wav')
    
    # METHOD TO CHECK FOR COLLISION (IF DESIRED)

    def collides(self, bolt):
        """
        Returns: True if the bolt was fired by the player and collides with 
        this alien
            
        Parameter bolt: The laser bolt to check
        Precondition: bolt is of class Bolt
        """
        firedbyplayer = bolt.isplayer()
        a = self.contains((bolt.x-(BOLT_WIDTH/2), bolt.y+(BOLT_HEIGHT/2)))
        b = self.contains((bolt.x-(BOLT_WIDTH/2), bolt.y-(BOLT_HEIGHT/2)))
        c = self.contains((bolt.x+(BOLT_WIDTH/2), bolt.y+(BOLT_HEIGHT/2)))
        d = self.contains((bolt.x-(BOLT_WIDTH/2), bolt.y-(BOLT_HEIGHT/2)))
        if firedbyplayer and (a or b or c or d):
            return True
        return False
    
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY
    def playsound(self):
        """
        Plays Sound object in _sound
        """
        self._sound.play()


class Bolt(GRectangle):
    """
    A class representing a laser bolt.
    
    Laser bolts are often just thin, white rectangles.  The size of the bolt is 
    determined by constants in consts.py. We MUST subclass GRectangle, because we
    need to add an extra attribute for the velocity of the bolt.
    
    The class Wave will need to look at these attributes, so you will need getters for 
    them.  However, it is possible to write this assignment with no setters for the 
    velocities.  That is because the velocity is fixed and cannot change once the bolt
    is fired.
    
    In addition to the getters, you need to write the __init__ method to set the starting
    velocity. This __init__ method will need to call the __init__ from GRectangle as a 
    helper.
    
    You also MIGHT want to create a method to move the bolt.  You move the bolt by adding
    the velocity to the y-position.  However, the getter allows Wave to do this on its
    own, so this method is not required.
    
    INSTANCE ATTRIBUTES:
        _velocity: The velocity in y direction [int or float]
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _isplayerbolt: true if bolt belongs to player [bool]
        _isoutofbounds: true if bolt is out of bounds [bool]
        _sound: instance of Sound object [Sound]
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)
    def gety(self):
        """
        Returns the attribute y.

        This method returns the attribute y directly.  Any 
        changes made will modify y.
        """
        return self.y
    
    def isout(self):
        """
        Returns the attribute _isoutofbounds.

        This method returns the attribute _isoutofbounds 
        directly.  Any changes made will modify _isoutofbounds.
        """
        return self._isoutofbounds

    def setout(self):
        """
        Sets attribute _isoutofbounds to True.
        """
        self._isoutofbounds = True

    def isplayer(self):
        """
        Returns the attribute _isplayerbolt.

        This method returns the attribute _isplayerbolt directly. Any changes
        made will modify _isplayerbolt.
        """
        return self._isplayerbolt
    
    # INITIALIZER TO SET THE VELOCITY
    def __init__(self, x, y, vel, isplayerbolt):
        """
        Initializes a new Bolt class.

        Bolt is a subclass of GRectangle. Extra attribute _velocity is set for 
        the speed of bolt and _isplayerbolt is set to indicate whether 
        or not bolt belongs to player.

        Parameter x: x position of Bolt
        Precondition: x is an int, 0 + (BOLT_WIDTH/2) <= x <= GAME_WIDTH - 
        (BOLT_WIDTH/2)

        Parameter y: y position of Bolt
        Precondition: y is an int, 0 + (BOLT_HEIGHT/2) <= y <= GAME_HEIGHT - 
        (BOLT_HEIGHT/2)

        Parameter vel: velocity of Bolt
        Precondition: vel is a number

        Parameter isplayerbolt: determines whether or not bolt belongs to 
        player
        Precondition: isplayerbolt is a boolean, True or False
        """
        assert (type(x) == int or type(x) == float) and (0 + (0 + (
            BOLT_WIDTH/2) <= x 
        <= GAME_WIDTH - (BOLT_WIDTH/2)))
        assert (type(y) == int or type(y) == float) and (0 + (0 + (
            BOLT_HEIGHT/2) <= y 
        <= GAME_HEIGHT - (BOLT_HEIGHT/2)))
        assert (type(vel) == int or type(vel) == float)
        assert type(isplayerbolt) == bool

        super().__init__(x=x, y=y, width=BOLT_WIDTH, height=
        BOLT_HEIGHT, fillcolor='red')
        self._velocity = vel
        self._isplayerbolt = isplayerbolt
        self._isoutofbounds = False
        self._sound = Sound('pew2.wav')
    # ADD MORE METHODS (PROPERLY SPECIFIED) AS NECESSARY

    def playsound(self):
        """
        Runs play() in attribute _sound
        """
        self._sound.play()

    def move(self):
        """
        The Bolt is moved up a distance of _velocity.

        This method increases its y attribute by a its _velocity
        attribute.
        """
        self.y = self.y + self._velocity
# IF YOU NEED ADDITIONAL MODEL CLASSES, THEY GO HERE