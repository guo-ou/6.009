# -*- coding: utf-8 -*-
## 6.009 -- Fall 2017 -- Lab 9
#  Time spent on the lab:
#    Week 1: ~3-4 hours
#    Week 2: ...

###### BLOB DEFINITIONS AND CONSTANTS ######
class Blob(object):
    '''
    This is the Blob object - This contains all of the information about a specfic
    blob in the game at any time. It tracks the current texture, position,
    player status, velocity and softness. There is also the class method _render:
    This method returns the rendering information required for the Game.render function.
    '''
    def __init__(self,texture, pos, player, char):
        self.texture = texture
        self.pos = pos
        self.player = player
        self.char = char
        self.v_x = 0
        self.v_y = 0
        self.soft = None

    def _render(self):
        return {'texture': self.texture,
                          'pos': self.pos,
                          'player': self.player
                          }

class Blobs:
    '''
    This class contains information about Blob TYPES, not specific Blob Objects.
    All information about gravitation, softness, allowability will be placed in this class
    '''
    ## Possible blob types
    blob_chars = ["e","b","B","C","c","f","F","=","h","m","p","h","r","s","o","t","w"]
    ## Gravitationally affected blobs
    blob_gravs = ["f","h","m","p","o"]
    ## Soft type blobs
    soft = ["e","f","h","m","p","b","h","o"]

class Textures:
    """A collection of object textures.

    Each constant in this class describes one texture, and
    single-letter texture names are also used in level maps.
    For example, the letter "e" in a game level map indicates
    that there is a bee at that position in the game.

    To add support for a new blob type, or to add a new texture
    for an existing blob, you'll probably want to update this
    list and the TEXTURE_MAP list in ``Constants``.
    """
    Bee = "e"
    Boat = "b"
    Building = "B"
    Castle = "C"
    Cloud = "c"
    Fire = "f"
    Fireball = "F"
    Floor = "="
    Helicopter = "h"
    Mushroom = "m"
    Player = "p"
    PlayerBored = "bored"
    PlayerFlying = "h"
    PlayerLost = "defeat"
    PlayerWon = "victory"
    Rain = "r"
    Storm = "s"
    Sun = "o"
    Tree = "t"
    Water = "w"


###### GAME CONSTANTS ######
class Constants:
    """A collection of game-world constants.

    You can experiment with tweaking these constants, but
    remember to revert the changes when running the test suite!
    """
    TILE_SIZE = 128
    GRAVITY = -9
    MAX_DOWNWARDS_SPEED = 48

    PLAYER_DRAG = 6
    PLAYER_MAX_HORIZONTAL_SPEED = 48
    PLAYER_HORIZONTAL_ACCELERATION = 16
    PLAYER_JUMP_SPEED = 62
    PLAYER_JUMP_DURATION = 3
    PLAYER_BORED_THRESHOLD = 60

    STORM_LIGHTNING_ROUNDS = 5
    STORM_RAIN_ROUNDS = 10

    BEE_SPEED = 40
    MUSHROOM_SPEED = 16
    FIREBALL_SPEED = 60

    SUN_POWER = 5

    TEXTURE_MAP = {Textures.Bee: '1f41d',
                   Textures.Boat: '26f5',
                   Textures.Building: '1f3e2',
                   Textures.Castle: '1f3f0',
                   Textures.Cloud: '2601',
                   Textures.Fire: '1f525',
                   Textures.Fireball: '1f525',
                   Textures.Floor: '2b1b',
                   Textures.Helicopter: '1f681',
                   Textures.Mushroom: '1f344',
                   Textures.Player: '1f60a',
                   Textures.PlayerBored: '1f634',
                   Textures.PlayerFlying: '1f681',
                   Textures.PlayerLost: '1f61e',
                   Textures.PlayerWon: '1f60e',
                   Textures.Rain: '1f327',
                   Textures.Storm: '26c8',
                   Textures.Sun: '2600',
                   Textures.Tree: '1f333',
                   Textures.Water: '1f30a'}


###### GAME FUNCTIONALITY ######
class Rectangle:
    """A rectangle object to help with collision detection and resolution."""

    def __init__(self, x, y, w, h):
        """Initialize a new rectangle.

        `x` and `y` are the coordinates of the bottom-left corner. `w`
        and `h` are the dimensions of the rectangle.
        """
        self.x, self.y = x, y
        self.w, self.h = w, h

    def intersects(self, other):
        """Check whether `self` and `other` overlap.

        Rectangles are open on the top and right sides, and closed on
        the bottom and left sides; concretely, this means that the
        rectangle [0, 0, 1, 1] does not intersect either of [0, 1, 1, 1]
        or [1, 0, 1, 1].
        """

        ## Grab the displacement between the two bottom left corners of each ox
        dif_dis_x = other.x - self.x
        dif_dis_y = other.y - self.y

        ## Find the left and the bottom box as they determine whether the two rects intersect (top and right open)
        left_box = self if self.x < other.x else other
        bottom_box = self if self.y < other.y else other


        ## Check if the opposite box is far enough away to avoid intersection - if not, return True
        if abs(dif_dis_x) < left_box.w and abs(dif_dis_y) < bottom_box.h:
            return True

        ## No intersection
        return False

    @staticmethod
    def translationvector(r1, r2):
        """Compute how much `r2` needs to move to stop intersecting `r1`.

        If `r2` does not intersect `r1`, return ``None``.  Otherwise,
        return a minimal pair ``(x, y)`` such that translating `r2` by
        ``(x, y)`` would suppress the overlap. ``(x, y)`` is minimal in
        the sense of the "L1" distance; in other words, the sum of
        ``abs(x)`` and ``abs(y)`` should be as small as possible.

        When two pairs ``(x, y)`` and ``(y, x)`` are tied, return the
        one whose first element has the smallest magnitude.
        """

        def check_intersection(add):
            '''
            Helper function that creates a new rectangle with an additive
            vector and checks if it still intersects the original vector
            '''
            new_rect2 = Rectangle(r2.x + add[0], r2.y + add[1], r2.w, r2.h)
            return new_rect2.intersects(r1)


        if not r2.intersects(r1):
            return None ## No need for movement

        ## Grab the displacements between the bottom left corners of the two rectangles
        diff_origs_x = r2.x - r1.x
        diff_origs_y = r2.y - r1.y

        all_vects = set()## Instantiate an empty set for collection of possible vectors

        ## Add all options in which we adjust the x coordinate
        all_vects.add((r1.w-diff_origs_x, 0)) ## r2 is to the right of r1 and we need to move the rect to the right
        all_vects.add((-(r1.w-diff_origs_x), 0)) ## r2 is to the left of r1 and we need to move the rect to the left


        all_vects.add((-(diff_origs_x + r2.w), 0)) ## Sometimes we need to shift by a distance greater than the width
                                                   ## of the r2 box, but this will ONLY be when we need to move LEFT


        ## Add all options in which we adjust the y coordinate
        all_vects.add((0, -(r1.h-diff_origs_y))) ## r2 is above r1 and we need to move the rect downward
        all_vects.add((0, r1.h-diff_origs_y)) ## r2 below r1 and we need to move the rect upward

        all_vects.add((0, -(diff_origs_y + r2.h))) ## Sometimes we need to shift by a distance greater than the height
                                                   ## of the r2 box, but this will ONLY be when we need to move DOWN


        ## Create a blank dictionary to store tuple (vector) as keys and int (L1 distance) as values
        out_dict = dict()

        for vect in all_vects:
            if not check_intersection(vect): ## Do not add any vector that does not resolve the intersection
                out_dict[vect] = abs(vect[0]) + abs(vect[1]) ## Store the L1 distance


        vects = list(out_dict.keys())
        L1s = list(out_dict.values())

        lowest = out_dict[min(out_dict, key=out_dict.get)] ## Find the minimum L1 distance

        poss_vects = []
        while lowest in L1s:
            ## Grab all vectors that satisfy the minimul L1 distance (lowest)
            poss_vects.append(vects.pop(L1s.index(lowest)))
            L1s.pop(L1s.index(lowest))

        ## Return the vector with the smalled magnitude 0th component per the lab document
        best_vector = min(poss_vects, key=lambda tup: abs(tup[0]))

        return best_vector

class Game:
    def __init__(self, levelmap):
        """Initialize a new game, populated with objects from `levelmap`.

        `levelmap` is a 2D array of 1-character strings; all possible
        strings (and some others) are listed in the ``Textures`` class.
        Each character in `levelmap` corresponds to a blob of size
        ``TILE_SIZE * TILE_SIZE``.

        This function is free to store `levelmap`'s data however it
        wants.  For example, it may choose to just keep a copy of
        `levelmap`; or it could choose to read through `levelmap` and
        extract the position of each blob listed in `levelmap`.

        Any choice is acceptable, as long as it plays well with the
        implementation of ``timestep`` and ``render`` below.
        """

        blobs = []

        for r in range(len(levelmap)):
            for c in range(len(levelmap[0])):
                ## Loop through all elements of the levelmap array

                char = levelmap[r][c]
                if char in Blobs.blob_chars:
                    ## We've hit a blob
                    new_blob = Blob(Constants.TEXTURE_MAP[char],[c*128,(len(levelmap)-r-1)*128],char == "p", char)

                    ## Check if blob is a soft type blob
                    if char in Blobs.soft:
                        new_blob.soft = True
                    else:
                        new_blob.soft = False

                    blobs.append(new_blob)


        self.blobs = blobs ## Store all blobs
        self.state = "ongoing" ## Set game state to ongoing
        self.timeout = 0 ## Begin the counting of idle frames


    def timestep(self, keys):
        """Simulate the evolution of the game state over one time step.
        `keys` is a list of currently pressed keys."""

        if self.state != "ongoing":
            return ## Stop all updates if game is not ongoing


        ## Count the number of frames gone without input
        if not keys:
            self.timeout += 1
        else:
            self.timeout = 0

        for blob in self.blobs:
            ## Adjust the vertical velocities of all gravitationally affected blocks:
            if blob.char in Blobs.blob_gravs:
                blob.v_y += Constants.GRAVITY
                if blob.v_y <= -Constants.MAX_DOWNWARDS_SPEED:
                    ## Make sure we keep the downward velocity to a minimum
                    blob.v_y = -Constants.MAX_DOWNWARDS_SPEED

            ## Adjust the player velocities based on key inputs:
            if blob.char == "p":

                ## Adjust texture for boredom
                if self.timeout >= Constants.PLAYER_BORED_THRESHOLD + 1:
                    blob.texture = Constants.TEXTURE_MAP[Textures.PlayerBored]
                else:
                    blob.texture = Constants.TEXTURE_MAP[Textures.Player]

                ## Key Adjustments
                if "up" in keys:
                    blob.v_y = Constants.PLAYER_JUMP_SPEED

                if "left" in keys:
                    blob.v_x += -Constants.PLAYER_HORIZONTAL_ACCELERATION

                if "right" in keys:
                    blob.v_x += Constants.PLAYER_HORIZONTAL_ACCELERATION

                ## Adjust for Drag:
                drag = Constants.PLAYER_DRAG if blob.v_x < 0 else -Constants.PLAYER_DRAG

                if 0 < blob.v_x < drag:
                    drag = -blob.v_x
                if drag < blob.v_x < 0:
                    drag = blob.v_x

                ## Make sure drag does not cause us to push beyond 0 speed
                if (blob.v_x + drag)*blob.v_x < 0:
                    blob.v_x = 0
                else:
                    blob.v_x += drag if blob.v_x != 0 else 0


                ## Make sure we do not exceed max horizontal speed
                if blob.v_x > Constants.PLAYER_MAX_HORIZONTAL_SPEED:
                    blob.v_x = Constants.PLAYER_MAX_HORIZONTAL_SPEED

                if blob.v_x < -Constants.PLAYER_MAX_HORIZONTAL_SPEED:
                    blob.v_x = -Constants.PLAYER_MAX_HORIZONTAL_SPEED


            ## Adjust the positions of all blocks:
            blob.pos[0] += blob.v_x
            blob.pos[1] += blob.v_y

            ## AFTER moving the player in this frame, check if it causes him to be in defeat state
            if blob.pos[1] < -Constants.TILE_SIZE and blob.char == "p":
                self.state = "defeat"
                blob.texture = Constants.TEXTURE_MAP[Textures.PlayerLost]


        ## Vertical collision adjustments
        for blob1 in self.blobs:
            if not blob1.soft:
                continue
            for blob2 in self.blobs:
                if blob1 == blob2:
                    continue

                if blob2.soft: ## Not necessary for test suite, but necessary for soft on soft overlap
                    continue
                ## Create two rectangle objects for each blob such that we can perform out intersection algorithms
                soft_rect = Rectangle(blob1.pos[0], blob1.pos[1], Constants.TILE_SIZE, Constants.TILE_SIZE)
                hard_rect = Rectangle(blob2.pos[0], blob2.pos[1], Constants.TILE_SIZE, Constants.TILE_SIZE)

                if soft_rect.intersects(hard_rect):
                    ## Check for castle collisions:
                    if blob1.char == "p" and blob2.char == "C":
                        self.state = "victory"
                        blob1.texture = Constants.TEXTURE_MAP[Textures.PlayerWon]

                    move_vect = Rectangle.translationvector(hard_rect, soft_rect)

                    if move_vect[0] == 0:
                        ## Velocity Adjustments:
                        if (blob1.v_y * move_vect[1]) <= 0:
                            blob1.v_y = 0 ## v_y and dy differ in sign and therefore nullify each other

                        ## Adjust vertical position
                        blob1.pos[1] += move_vect[1]



        ## Remaining collision adjustments
        for blob1 in self.blobs:
            if not blob1.soft:
                continue
            for blob2 in self.blobs:
                if blob1 == blob2:
                    continue

                if blob2.soft: ## Not necessary for test suite, but necessary for soft on soft overlap
                    continue

                ## Instantiate two rectangle objects to perform out intersection algorithms
                soft_rect = Rectangle(blob1.pos[0], blob1.pos[1], Constants.TILE_SIZE, Constants.TILE_SIZE)
                hard_rect = Rectangle(blob2.pos[0], blob2.pos[1], Constants.TILE_SIZE, Constants.TILE_SIZE)

                if soft_rect.intersects(hard_rect):

                    ## Check for castle collisions:
                    if blob1.char == "p" and blob2.char == "C":
                        self.state = "victory"
                        blob1.texture = Constants.TEXTURE_MAP[Textures.PlayerWon]

                    move_vect = Rectangle.translationvector(hard_rect, soft_rect)

                    ## Velocity Adjustments:
                    if (blob1.v_x * move_vect[0]) <= 0  and move_vect[0] != 0:
                        blob1.v_x = 0 ## v_x and dx have opposite signs

                    ## Adjust horizontal position (no more vertical adjustments necessary)
                    blob1.pos[0] += move_vect[0]


    def grab_player_location(self):
        '''
        Used in the render function to grab the player's
        position such that we can center the viewing box
        '''
        for blob in self.blobs:
            if blob.player:
                return tuple(blob.pos)

    def render(self, w, h):
        """Report status and list of blob dictionaries for blobs
        with a horizontal distance of w//2 from player.  See writeup
        for details."""

        px, py = self.grab_player_location()

        output = [self.state, []] ## instatiate the format for rendering output
        viewing_rect = Rectangle(px-w//2, 0, w, h) ## instantiate the viewing rectanlge that should contain all visible blobs

        for blob in self.blobs:
            ## Create a rectangle defined by each blob
            blob_rect = Rectangle(blob.pos[0], blob.pos[1], Constants.TILE_SIZE, Constants.TILE_SIZE)

            ## If our blob rectangle intersects our viewing rectangle, that means that
            ## it should be shown on the screen
            if blob_rect.intersects(viewing_rect):
                output[1].append(blob._render())

        return output
