"""
Subcontroller module for Alien Invaders

This module contains the subcontroller to manage a single level or wave in the Alien
Invaders game.  Instances of Wave represent a single wave.  Whenever you move to a
new level, you are expected to make a new instance of the class.

The subcontroller Wave manages the ship, the aliens and any laser bolts on screen.  
These are model objects.  Their classes are defined in models.py.

Most of your work on this assignment will be in either this module or models.py.
Whether a helper method belongs in this module or models.py is often a complicated
issue.  If you do not know, ask on Piazza and we will answer.

# Sean Yoo (sy435)
# 12/3/2018
"""
from game2d import *
from consts import *
from models import *
import random

# PRIMARY RULE: Wave can only access attributes in models.py via getters/setters
# Wave is NOT allowed to access anything in app.py (Subcontrollers are not permitted 
# to access anything in their parent. To see why, take CS 3152)


class Wave(object):
    """
    This class controls a single level or wave of Alien Invaders.
    
    This subcontroller has a reference to the ship, aliens, and any laser bolts on screen. 
    It animates the laser bolts, removing any aliens as necessary. It also marches the
    aliens back and forth across the screen until they are all destroyed or they reach
    the defense line (at which point the player loses). When the wave is complete, you 
    should create a NEW instance of Wave (in Invaders) if you want to make a new wave of 
    aliens.
    
    If you want to pause the game, tell this controller to draw, but do not update.  See 
    subcontrollers.py from Lecture 24 for an example.  This class will be similar to
    than one in how it interacts with the main class Invaders.
    
    #UPDATE ME LATER
    INSTANCE ATTRIBUTES:
        _ship:   the player ship to control [Ship]
        _aliens: the 2d list of aliens in the wave [rectangular 2d list of Alien or None] 
        _bolts:  the laser bolts currently on screen [list of Bolt, possibly empty]
        _dline:  the defensive line being protected [GPath]
        _lives:  the number of lives left  [int >= 0]
        _time:   The amount of time since the last Alien "step" [number >= 0]
    
    As you can see, all of these attributes are hidden.  You may find that you want to
    access an attribute in class Invaders. It is okay if you do, but you MAY NOT ACCESS 
    THE ATTRIBUTES DIRECTLY. You must use a getter and/or setter for any attribute that 
    you need to access in Invaders.  Only add the getters and setters that you need for 
    Invaders. You can keep everything else hidden.
    
    You may change any of the attributes above as you see fit. For example, may want to 
    keep track of the score.  You also might want some label objects to display the score
    and number of lives. If you make changes, please list the changes with the invariants.
    
    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        _ismovingright: true if aliens should move right [bool]
        _alienstep: number of alien steps since last alien shot [int >= 0] 
        _alienshotrate: rate at which aliens should fire [int 0...BOLT_RATE]
        _emptyaliens: true if there are no aliens in _aliens [bool]
        _lost: true if player has lost [bool]
        _shippew: Sound object for ship shot [instance of Sound]
        _shipdestroyed: Sound object for ship destroyed [instance of Sound]
        _mute: true if muted [bool]
        _alienspeed: number of seconds between alien steps [0 <= float <= 1]
        _score: score of current game [int>=0]
    """
    
    # GETTERS AND SETTERS (ONLY ADD IF YOU NEED THEM)

    def getship(self):
        """
        Returns the ship.

        This method returns the attribute _ship directly.  Any changes 
        made will modify the ship.
        """
        return self._ship

    def getlives(self):
        """
        Returns the attribute _lives.

        This method returns the attribute _lives directly.  Any changes 
        made will modify the number of lives.
        """
        return self._lives
    
    def setlives(self, lives):
        """
        Takes parameter lives and puts it into attribute _lives.

        Parameter lives: New number of lives
        Precondition: lives is an int [int >= 0]
        """
        assert lives >= 0 and type(lives)
        self._lives = lives

    def getemptyaliens(self):
        """
        Returns the attribute _emptyaliens.

        This method returns the attribute _emptyaliens directly. Any 
        changes made will mody _emptyaliens directly.
        """
        return self._emptyaliens

    def getlost(self):
        """
        Returns the attribute _lost.

        This method returns the attribute _emptyaliens directly. Any 
        changes made will mody _emptyaliens directly.
        """
        return self._lost
    
    def getmute(self):
        """
        Returns _mute attribute.
        """
        return self._mute

    def setmute(self):
        """
        Toggles _mute
        """
        self._mute = not self._mute

    def getshipdestroyed(self):
        """
        Returns _shipdestroyed attribute
        """
        return self._shipdestroyed

    def setalienspeed(self, speed):
        """
        Sets _alienspeed at given parameter speed.

        Parameter speed: speed of alien step
        Precondition: speed is a float [speed > 0]
        """
        self._alienspeed = speed

    def getscore(self):
        """
        Returns attribute _score
        """
        return self._score

    def setscore(self, score):
        """
        Takes parameter score and puts it into attribute _score.

        Parameter score: New score
        Precondition: score is an int [int >= 0]
        """
        assert score >= 0 and type(score)
        self._score = score

    # INITIALIZER (standard form) TO CREATE SHIP AND ALIENS
    def __init__(self):
        """
        Initializes a new Wave class.

        Wave is an object. This method initializes the following attributes:
        _ship, _aliens, _bolts, _dline, _lives, _time, _ismovingright,
        _alienstep, _alienshotrate, _lost, _emptyaliens, _shippew, _mute
        """
        self._score = 0
        self.fillrows()
        self._bolts = []
        self.createship()
        self._lives = 3
        self._emptyaliens = False
        self._lost = False
        self._dline = GPath(linecolor = 'black', 
            points = [0, DEFENSE_LINE, GAME_WIDTH, DEFENSE_LINE], 
            linewidth = 1)
        self._ismovingright = True
        self._time = 0
        self._alienstep = 0
        self._alienshotrate = random.randint(1, BOLT_RATE)
        self._shippew = Sound('pew1.wav')
        self._mute = False
        self._shipdestroyed = Sound('blast1.wav')
        self._alienspeed = ALIEN_SPEED

    def fillrows(self):
        """
        Initializes the attribute for _aliens

        This method is a helper for __init__. It fills attribute _aliens
        with ALIEN_ROWS rows of ALIENS_IN_ROW aliens. With a given number
        of images of aliens, every two rows has aliens with same image. If all
        images are used, the subsequent row starts with the first image and so 
        on.
        """
        self._aliens = []

        imnum = 0

        for i in range(ALIEN_ROWS):
            ypos = GAME_HEIGHT - ((ALIEN_CEILING + (ALIEN_HEIGHT/2)) + 
                (ALIEN_ROWS-1-i) * (ALIEN_V_SEP+ALIEN_HEIGHT))
            row = []

            for j in range(ALIENS_IN_ROW):
                xpos = (ALIEN_H_SEP + (ALIEN_WIDTH/2)) + j * (ALIEN_H_SEP+
                ALIEN_WIDTH)
                alien = Alien(xpos, ypos, ALIEN_IMAGES[imnum])
                row.append(alien)
            
            self._aliens.append(row)
            
            if i%2 == 1:
                if imnum+1 > len(ALIEN_IMAGES)-1:
                    imnum = 0
                else:
                    imnum = imnum+1

    def createship(self):
        """
        Creates a new Ship class and adds it to attribute _ship.
        """
        ship = Ship(GAME_WIDTH/2, SHIP_BOTTOM)
        self._ship = ship

    # UPDATE METHOD TO MOVE THE SHIP, ALIENS, AND LASER BOLTS
    def update(self, iinput, dt):
        """
        Animates a single frame in the game.

        Parameter iinput: instance of GInput
        Precondition: iinput is instance of GInput

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        if self._ship != None:
            if iinput.is_key_down('right'):
                if self._ship.getx() < GAME_WIDTH-(SHIP_WIDTH/2):
                    self._ship.setx(self._ship.getx() + SHIP_MOVEMENT)
            elif iinput.is_key_down('left'):
                if self._ship.getx() > SHIP_WIDTH/2:
                    self._ship.setx(self._ship.getx() - SHIP_MOVEMENT)
        
        if iinput.is_key_down('w') and self._ship != None:
            self.firebolt()
        
        if self._alienstep >= self._alienshotrate:
            self.alienshotsequence()

        self.movebolts()
        self.checksshipcollision()
        self.removealiens()
        self._time = self._time + dt
        self.checkifempty()
        self.movealiens()
    
    def checksshipcollision(self):
        """
        Checks if any bolts from aliens collides with ship.

        This method checks for collisions between bolt fired by alien and
        ship. If one exists, the round is over so all bolts are erased and
        the _ship is set to None.
        """
        if self._ship != None:
            for bolt in self._bolts:
                if self._ship.collides(bolt):
                    del bolt
                    self._ship = None
                    self._bolts = []
                    break
        
    def checkifempty(self):
        """
        Checks if there is an alien in _aliens

        THis method checks if there is an alien in _aliens. If none,
        then it sets _emptyaliens to True. Otherwise to False.
        """
        self._emptyaliens = True
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    self._emptyaliens = False

    def movealiens(self):
        """
        Runs moveright() or moveleft() and adds 1 to _alienstep.

        If _aliens has at least one alien, this method checks the direction
        of movement and runs moveright() and moveleft() accordingly.
        """
        if self._emptyaliens == False:
            if self._ismovingright == True:
                if self._time >= self._alienspeed:
                    self.moveright()
                    self._alienstep = self._alienstep + 1
            elif self._ismovingright == False:
                if self._time >= self._alienspeed:
                    self.moveleft()
                    self._alienstep = self._alienstep + 1

    def removealiens(self):
        """
        Checks collision of any bolt and alien and removes both if evident.

        This methods cycles through all the bolts and check if any alien 
        collides with them. If there is a collision, the bolt is removed 
        from _bolts and the space that the alien took up in _aliens 
        is set to None. If alien is removed, the _alienspeed attribute
        is multiplied by a factor of 0.97. The score is also increased.
        """
        for i in range(len(self._aliens)):
            for j in range(len(self._aliens[i])):
                for bolt in self._bolts:
                    if self._aliens[i][j] != None:
                        if self._aliens[i][j].collides(bolt):
                            if self._mute == False:
                                self._aliens[i][j].playsound()
                            self._alienspeed = self._alienspeed * 0.97
                            self._score = self._score + (len(
                                self._aliens)-i)*10
                            self._aliens[i][j] = None
                            self._bolts.remove(bolt)

    def alienshotsequence(self):
        """
        Performs randomized shot sequence for alien.

        This method resets the _alienstep attribute to zero and
        sets a new shot rate for attribute _alienshotrate. It then
        finds a nonempty random column and fires a bolt from the
        bottom most alien.
        """
        self._alienstep = 0
        self._alienshotrate = random.randint(1, BOLT_RATE)
        col = self.findnonemptycol()
        self.alienfirebolt(col)

    def findnonemptycol(self):
        """
        Find a randomized nonempty column of aliens.
        """
        col = None
        while col == None:
            randcol = random.randint(0, len(self._aliens[0])-1)
            for row in self._aliens:
                if row[randcol] != None:
                    col = randcol
        return col

    def alienfirebolt(self, aliencol):
        """
        Fires a bolt from the bottom most alien.

        This method takes a column index of an alien and finds the
        bottom most alien and fires a bolt from this alien. If bolt is
        made and fired, the playsound() method is also called in the bolt.

        Parameter: aliencol is an index of an alien column
        Precondition: aliencol is a valid index of a nonempty column of 
        aliens of type int.
        """
        assert type(aliencol) == int
        assert (aliencol >= 0 and aliencol < len(self._aliens[0]))

        index = None
        i = 0
        alienfound = False
        while i < len(self._aliens) and alienfound == False:
            if self._aliens[i][aliencol] != None:
                index = i
                alienfound = True
            i = i + 1

        if index == None:
            return False
        else:
            x = self._aliens[index][aliencol].getx()
            y = self._aliens[index][aliencol].gety() - (ALIEN_HEIGHT/2)
            bolt = Bolt(x, y, -BOLT_SPEED, False)
            self._bolts.append(bolt)
            if self._mute == False:
                bolt.playsound()

    def firebolt(self):
        """
        Fires a bolt from ship if no other bolts belong to player.

        This method first checks if any of the bolts in _bolts belong
        to the player. If not, then it makes a bolt and fires it from
        the top of the ship and adds it to attribute _bolt. If bolt is 
        made and fired, the play() function for Sound object in 
        _shippew is run.
        """
        playerbolt = False
        for bolt in self._bolts:
            if bolt.isplayer():
                playerbolt = True
        if playerbolt == False:
            x = self._ship.getx()
            y = self._ship.gety() + (SHIP_HEIGHT/2)
            bolt = Bolt(x, y, BOLT_SPEED, True)
            self._bolts.append(bolt)
            if self._mute == False:
                self._shippew.play()

    def movebolts(self):
        """
        Moves all bolts a distance of their velocity and removes those out of 
        bounds.

        This method cycles through all of the bolts in _bolts and determines 
        if they are out of bounds. If it is, then it sets its attribute 
        _outofbounds to True. If not, then it moves the bolt a distance 
        of its velocity. The method then cycles through all 
        of the bolts again and removes those that are out of bounds.
        """
        for bolt in self._bolts:
            if bolt.gety() > GAME_HEIGHT+(BOLT_HEIGHT/
            2) or bolt.gety() < 0-(BOLT_HEIGHT/2):
                bolt.setout()
            else:
                bolt.move()
        
        i = 0
        while i < len(self._bolts):
            if self._bolts[i].isout():
                del self._bolts[i]
            else:
                i += 1

    def findlastcolalien(self):
        """
        Finds and returns an alien in the last column.

        This method cycles through all of the aliens and
        returns an alien in the last column.
        """
        x = 0
        lastalien = self._aliens[0][0]
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    if alien.x > x:
                        x = alien.getx()
                        lastalien = alien
        
        return lastalien

    def findfirstcolalien(self):
        """
        Finds and returns an alien in the first column.

        This method cycles through all of the aliens and
        returns an alien in the first column.
        """
        x = GAME_WIDTH
        firstalien = None
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    if alien.getx() < x:
                        x = alien.getx()
                        firstalien = alien
        return firstalien

    def moveright(self):
        """
        Moves all aliens ALIEN_H_WALK distance to the right.

        This method moves all aliens a distance of ALIEN_H_WALK to the right.
        It first finds an alien in the last column and determines if it reached
        the right side of the field. If it does, then it moves all aliens down 
        a distance of ALIEN_V_WALK and sets attribute _ismovingright to False. 
        Attribute _time is set to 0.
        """
        lastalien = self.findlastcolalien()
        if lastalien != None:
            if lastalien.getx() < GAME_WIDTH-(ALIEN_H_SEP+(ALIEN_WIDTH/2)):
                for rows in self._aliens:
                    for alien in rows:
                        if alien != None:
                            alien.setx(alien.getx() + ALIEN_H_WALK)
            else:
                self._ismovingright = False
                for rows in self._aliens:
                    for alien in rows:
                        if alien != None:
                            alien.sety(alien.gety() - ALIEN_V_WALK)
                            if alien.gety() <= DEFENSE_LINE + (ALIEN_HEIGHT/2):
                                self._lost = True
        self._time = 0

    def moveleft(self):
        """
        Moves all aliens ALIEN_H_WALK distance to the left.

        This method moves all aliens a distance of ALIEN_H_WALK to the left.
        It first finds an alien in the first column and determines if it 
        reached the left side of the field. If it does, then it moves all 
        aliens down a distance of ALIEN_V_WALK and sets attribute 
        _ismovingright to True. Attribute _time is set to 0.
        """
        firstalien = self.findfirstcolalien()
        if firstalien != None:
            if firstalien.getx() > ALIEN_H_SEP + (ALIEN_WIDTH/2):
                for rows in self._aliens:
                    for alien in rows:
                        if alien != None:
                            alien.setx(alien.getx() - ALIEN_H_WALK)
            else:
                self._ismovingright = True
                for rows in self._aliens:
                    for alien in rows:
                        if alien != None:
                            alien.sety(alien.gety() - ALIEN_V_WALK)
                            if alien.gety() <= DEFENSE_LINE + (ALIEN_HEIGHT/2):
                                self._lost = True
        self._time = 0

    # DRAW METHOD TO DRAW THE SHIP, ALIENS, DEFENSIVE LINE AND BOLTS
    def draw(self, view):
        """
        Draws the game objects to the given view.
        """
        for row in self._aliens:
            for alien in row:
                if alien != None:
                    alien.draw(view)

        for bolt in self._bolts:
            bolt.draw(view)
        
        if self._ship != None:
            self._ship.draw(view)
        self._dline.draw(view)
    # HELPER METHODS FOR COLLISION DETECTION
