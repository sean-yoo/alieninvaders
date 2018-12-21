"""
Primary module for Alien Invaders

This module contains the main controller class for the Alien Invaders application. There
is no need for any additional classes in this module.  If you need more classes, 99% of
the time they belong in either the wave module or the models module. If you are unsure
about where a new class should go, post a question on Piazza.

# Sean Yoo (sy435)
# 12/3/2018
"""
from consts import *
from game2d import *
from wave import *


# PRIMARY RULE: Invaders can only access attributes in wave.py via getters/setters
# Invaders is NOT allowed to access anything in models.py

class Invaders(GameApp):
    """
    The primary controller class for the Alien Invaders application

    This class extends GameApp and implements the various methods necessary for processing
    the player inputs and starting/running a game.

        Method start begins the application.

        Method update either changes the state or updates the Play object

        Method draw displays the Play object and any other elements on screen

    Because of some of the weird ways that Kivy works, you SHOULD NOT create an
    initializer __init__ for this class.  Any initialization should be done in
    the start method instead.  This is only for this class.  All other classes
    behave normally.

    Most of the work handling the game is actually provided in the class Wave.
    Wave should be modeled after subcontrollers.py from lecture, and will have
    its own update and draw method.

    The primary purpose of this class is to manage the game state: which is when the
    game started, paused, completed, etc. It keeps track of that in an attribute
    called _state.

    INSTANCE ATTRIBUTES:
        view:   the game view, used in drawing (see examples from class)
                [instance of GView; it is inherited from GameApp]
        input:  the user input, used to control the ship and change state
                [instance of GInput; it is inherited from GameApp]
        _state: the current state of the game represented as a value from consts.py
                [one of STATE_INACTIVE, STATE_NEWWAVE, STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, STATE_COMPLETE]
        _wave:  the subcontroller for a single wave, which manages the ships and aliens
                [Wave, or None if there is no wave currently active]
        _text:  the currently active message
                [GLabel, or None if there is no message to display]

    STATE SPECIFIC INVARIANTS:
        Attribute _wave is only None if _state is STATE_INACTIVE.
        Attribute _text is only None if _state is STATE_ACTIVE.

    For a complete description of how the states work, see the specification for the
    method update.

    You may have more attributes if you wish (you might want an attribute to store
    any score across multiple waves). If you add new attributes, they need to be
    documented here.

    LIST MORE ATTRIBUTES (AND THEIR INVARIANTS) HERE IF NECESSARY
        lastkeys: key count from _input [num int or float]
        _wavenum: wave level of game [int>=1]
        _lives: number of lives in game session [int >=0]
        _score: score in game session[int >= 0]
        _muted: true if game is muted [bool]
    """
    # DO NOT MAKE A NEW INITIALIZER!
    def _getstate(self):
        """
        Returns the state of game.

        This getter method is to protect access to the state.
        """
        return self._state

    def _getwave(self):
        """
        Returns the _wave of game.

        This getter method is to protect access to _wave.
        """
        return self._wave
    # THREE MAIN GAMEAPP METHODS
    def start(self):
        """
        Initializes the application.

        This method is distinct from the built-in initializer __init__ (which you
        should not override or change). This method is called once the game is running.
        You should use it to initialize any game specific attributes.

        This method should make sure that all of the attributes satisfy the given
        invariants. When done, it sets the _state to STATE_INACTIVE and create a message
        (in attribute _text) saying that the user should press to play a game.
        """
        self._state = STATE_INACTIVE
        self._wave = None
        self.lastkeys = 0
        self._wavenum = 0
        self._lives = None
        self._score = 0
        self._muted = False

        welcome = GLabel(text = "Press 'S' to Play", x = 
        GAME_WIDTH/2, y = GAME_HEIGHT/2)
        if self._state == STATE_INACTIVE:
            self._text = welcome

    def update(self,dt):
        """
        Animates a single frame in the game.

        It is the method that does most of the work. It is NOT in charge of playing the
        game.  That is the purpose of the class Wave. The primary purpose of this
        game is to determine the current state, and -- if the game is active -- pass
        the input to the Wave object _wave to play the game.

        As part of the assignment, you are allowed to add your own states. However, at
        a minimum you must support the following states: STATE_INACTIVE, STATE_NEWWAVE,
        STATE_ACTIVE, STATE_PAUSED, STATE_CONTINUE, and STATE_COMPLETE.  Each one of these
        does its own thing and might even needs its own helper.  We describe these below.

        STATE_INACTIVE: This is the state when the application first opens.  It is a
        paused state, waiting for the player to start the game.  It displays a simple
        message on the screen. The application remains in this state so long as the
        player never presses a key.  In addition, this is the state the application
        returns to when the game is over (all lives are lost or all aliens are dead).

        STATE_NEWWAVE: This is the state creates a new wave and shows it on the screen.
        The application switches to this state if the state was STATE_INACTIVE in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_ACTIVE: This is a session of normal gameplay.  The player can move the
        ship and fire laser bolts.  All of this should be handled inside of class Wave
        (NOT in this class).  Hence the Wave class should have an update() method, just
        like the subcontroller example in lecture.

        STATE_PAUSED: Like STATE_INACTIVE, this is a paused state. However, the game is
        still visible on the screen.

        STATE_CONTINUE: This state restores the ship after it was destroyed. The
        application switches to this state if the state was STATE_PAUSED in the
        previous frame, and the player pressed a key. This state only lasts one animation
        frame before switching to STATE_ACTIVE.

        STATE_DEFEAT: The wave is over, and is lost.

        STATE_WIN: The wave is over and is won

        You are allowed to add more states if you wish. Should you do so, you should
        describe them here.

        Parameter dt: The time in seconds since last update
        Precondition: dt is a number (int or float)
        """
        self._determineState()

        if self._getstate() == STATE_NEWWAVE:
            self._initwave()

        if self._getstate() == STATE_ACTIVE:
            self._wave.update(self.input, dt)

        if self._getstate() == STATE_PAUSED:
            self._text = GLabel(text = "Press 'S' to Continue", x = 
            GAME_WIDTH/2, y = GAME_HEIGHT/2)
        
        if self._getstate() == STATE_CONTINUE:
            self._continue()
        
        if self._getstate() == STATE_DEFEAT:
            self._text = GLabel(text = "Press 'S' to Play Again", x = 
            GAME_WIDTH/2, y = GAME_HEIGHT/2)

        if self._getstate() == STATE_WIN:
            self._text = GLabel(text = "WAVE " + 
            str(self._wavenum + 1) +" COMPLETE", 
                x = GAME_WIDTH/2, y = GAME_HEIGHT/2)

    def draw(self):
        """
        Draws the game objects to the view.

        Every single thing you want to draw in this game is a GObject.  To draw a GObject
        g, simply use the method g.draw(self.view).  It is that easy!

        Many of the GObjects (such as the ships, aliens, and bolts) are attributes in
        Wave. In order to draw them, you either need to add getters for these attributes
        or you need to add a draw method to class Wave.  We suggest the latter.  See
        the example subcontroller.py from class.
        """
        # IMPLEMENT ME
        if self._text:
            self._text.draw(self.view)
        
        self.drawactivestate()

        if self._state == STATE_DEFEAT:
            score = GLabel(text = "Score: " + str(self._wave.getscore()), 
                x = GAME_WIDTH/2, y = GAME_HEIGHT/2 + 40)
            score.draw(self.view)
            defeat = GLabel(text = "DEFEAT", 
                x = GAME_WIDTH/2, y = GAME_HEIGHT/2 + 140, font_size= 120)
            defeat.draw(self.view)
        
        if self._state == STATE_WIN:
            score = GLabel(text = "Score: " + str(self._wave.getscore()), 
                x = GAME_WIDTH/2, y = GAME_HEIGHT/2 + 40)
            score.draw(self.view)
            defeat = GLabel(text = "CONGRATULATIONS", 
                x = GAME_WIDTH/2, y = GAME_HEIGHT/2 + 140, font_size= 60)
            defeat.draw(self.view)
            again = GLabel(text = "Press 'S' to Continue", 
                x = GAME_WIDTH/2, y = GAME_HEIGHT/2 - 30, font_size = 20)
            again.draw(self.view)

    def drawactivestate(self):
        """
        Draws components of active state.

        This method draws components that are shown in an active state.
        """
        if self._state == STATE_ACTIVE:
            self._wave.draw(self.view)
            level = GLabel(text = "Wave: " + str(self._wavenum+1), 
            x = GAME_WIDTH/2, y = GAME_HEIGHT-20)
            level.draw(self.view)
            line = GPath(linecolor = 'black', 
            points = [0, GAME_HEIGHT-60, GAME_WIDTH, GAME_HEIGHT-
            60], linewidth = 1.5)
            line.draw(self.view)

        if self._wave and self._state == STATE_ACTIVE:
            lives = GLabel(text = 'Lives: ' + str(self._wave.getlives()), 
                x = GAME_WIDTH-60, y = GAME_HEIGHT-20)
            lives.draw(self.view)
            pause = GLabel(text = "Press 'P' to pause", 
                x = GAME_WIDTH-60, y = GAME_HEIGHT-40, font_size= 10)
            pause.draw(self.view)
            muted = GLabel(text = "Press 'm' to mute", 
                x = GAME_WIDTH-60, y = GAME_HEIGHT-50, font_size= 10)
            muted.draw(self.view)
            score = GLabel(text = "Score: ", 
                x = 50, y = GAME_HEIGHT-20)
            score2 = GLabel(text =str(self._wave.getscore()), 
                x = score.x + 80, y = GAME_HEIGHT-20)
            score.draw(self.view)
            score2.draw(self.view)

    # HELPER METHODS FOR THE STATES GO HERE
    def _determineState(self):
        """
        Determines the current state and assigns it to self._state.

        This method looks for a key press, and acts accordingly depending
        on the current _state. A key press is when a key is pressed for 
        the FIRST TIME.

        This method checks if _mute is True. If it is, _wave._muted is set
        to True and _muted is set to True
        
        If state is STATE_INACTIVE, _inactive() is run.

        If state is STATE_ACTIVE, _active() is run.

        If state is STATE_PAUSED, currkeys is used to check for if user presses
        's' key for the first time. If user does, then the state is set to 
        STATE_CONTINUE and _text is set to None.

        If state is STATE_DEFEAT, currkeys is used to check for if user presses
        's' key for the first time. If user does, then the state is set to 
        STATE_NEWWAVE, _lives, _score, and _text are set to None.

        statewin() is run

        lastkeys attribute is updated.
        """
        currkeys = self.input.key_count
        mute = currkeys > self.lastkeys and self._input.is_key_down(
            'm') and self.lastkeys == 0
        if mute:
            self._wave.setmute()
            self._muted = True
        currkeys = self.input.key_count
        if self._getstate() == STATE_INACTIVE:
            self._inactive(currkeys)
        if self._getstate() == STATE_ACTIVE:
            self._active(currkeys)

        if self._getstate() == STATE_PAUSED:
            exitpause = currkeys > self.lastkeys and self._input.is_key_down(
                's') and self.lastkeys == 0
            if exitpause:
                self._state = STATE_CONTINUE
                self._text = None

        if self._getstate() == STATE_DEFEAT:
            exittext = currkeys > self.lastkeys and self._input.is_key_down(
                's') and self.lastkeys == 0
            if exittext:
                self._lives = None
                self._score = None
                self._state = STATE_NEWWAVE
                self._text = None

        self.statewin(currkeys)
        self.lastkeys = currkeys

    def statewin(self, currkeys):
        """
        Runs procedure for if _state == STATE_WIN

        This method checks if state is STATE_WIN. If it is,
        _lives and _score is updated from the _wave and currkeys
        is used to check whether not 's' is pressed for the first
        time. If it is, _state is set to STATE_NEWWAVE and _text is
        set to none.

        Parameter: currkeys is number of keys pressed.
        Precondition: currkeys is a valid number >=0
        """
        if self._getstate() == STATE_WIN:
            self._lives = self._wave.getlives()
            self._score = self._wave.getscore()
            exittext = currkeys > self.lastkeys and self._input.is_key_down(
                's') and self.lastkeys == 0
            if exittext:
                self._state = STATE_NEWWAVE
                self._text = None

    def _inactive(self, currkeys):
        """
        Runs procedure for when _state is STATE_INACTIVE

        currkeys is used to check if key 's' is pressed, 
        the first time. If it is, this method will set 
        _text to None and set state to STATE_NEWWAVE.

        Parameter: currkeys is number of keys pressed.
        Precondition: currkeys is a valid number >=0
        """
        assert (type(currkeys) == int or type(currkeys) == float)
        assert (currkeys >= 0)
        exitwelcome = currkeys > 0 and self._input.is_key_down(
            's') and self.lastkeys == 0
        if exitwelcome:
            self._state = STATE_NEWWAVE
            self._text = None

    def _active(self, currkeys):
        """
        Runs procedure for when _state is STATE_ACTIVE

        This method checks if the ship is destroyed. If it is and
        there are lives remaining, the game pauses. If no more lives,
        the game ends and _state is set to STATE_DEFEAT. If there are
        no more aliens, games ends and _state is set to STATE_WIN.
        """
        if self._wave.getship() == None:
            if self._wave.getmute() == False:
                self._wave.getshipdestroyed().play()
            self._wave.setlives(self._wave.getlives()-1)
            if self._wave.getlives() > 0:
                self._state = STATE_PAUSED
            else:
                self._state = STATE_DEFEAT
                self._wavenum = 0
        if self._wave.getemptyaliens() == True:
            self._state = STATE_WIN
            self._wavenum = self._wavenum + 1
        if self._wave.getlost() == True:
            self._state = STATE_DEFEAT
        
        pause = currkeys > 0 and self._input.is_key_down(
            'p') and self.lastkeys == 0
        if pause:
            self._state = STATE_PAUSED

    def _initwave(self):
        """
        Creates and new wave class and assigns it to self._wave and sets 
        _state to STATE_ACTIVE. Speed is set to adjusted based on _wavenum.
        """
        newwave = Wave()
        self._wave = newwave
        self._wave.setalienspeed(ALIEN_SPEED*(0.75)**(self._wavenum))
        if self._lives:
            self._wave.setlives(self._lives)
        if self._score:
            self._wave.setscore(self._score)
        if self._muted:
            self._wave.setmute()
        self._state = STATE_ACTIVE

    def _continue(self):
        """
        Creates a new ship if none exists for attribute _wave and sets _state 
        to STATE_ACTIVE
        """
        if self._wave.getship() == None:
            self._wave.createship()
        self._state = STATE_ACTIVE
