"""6.009 Lab 4 -- HyperMines"""

import sys

sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS


class HyperMinesGame:
    def __init__(self, dims, bombs):
        """Start a new game.

        This method should properly initialize the "board", "mask",
        "dimensions", and "state" attributes.

        Args:
           dims (list): Dimensions of the board
           bombs (list): Bomb locations as a list of lists, each an
                         N-dimensional coordinate

        >>> g = HyperMinesGame([2, 4, 2], [[0, 0, 1], [1, 0, 0], [1, 1, 1]])
        >>> g.dump()
        dimensions: [2, 4, 2]
        board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
               [['.', 3], [3, '.'], [1, 1], [0, 0]]
        mask:  [[False, False], [False, False], [False, False], [False, False]]
               [[False, False], [False, False], [False, False], [False, False]]
        state: ongoing
        """

        self.dimensions = []
        self.board = []
        self.mask = []
        self.state = "ongoing"

        self.set_all_values(dims, bombs)


    def grab_obj_from_coord(self, array, coord, depth, obj=None):
        '''
        Grabs the value from a given coord. Has the option
        to either +=1 to that coordinate or replace that
        cell with a specified object

        >>> g5 = HyperMinesGame([5,5,5], [[1,1,1]])
        >>> g5.grab_obj_from_coord(g5.board, [1,1,1], 0)
        '.'

        '''
        if depth == len(coord) -1:
            if obj != None:
                if obj == "add":
                    if type(array[coord[depth]]) == str: #Avoids bombs
                        pass
                    else:
                        array[coord[depth]] += 1
                else:
                    array[coord[depth]] = obj
            return array[coord[depth]]

        else:
            array = array[coord[depth]]
            return self.grab_obj_from_coord(array, coord, depth + 1, obj)



    def get_neighbors(self, dimensions, coord, depth, working_coord=[]):
        '''
        Recursively creates the coordinates of all the neighbor cells to a given cell.
        Includes the given coordinate in the final list.
        Set used to remove the possibility of doubles and increase speed.

        DOCTESTS:

        >>> g4 = HyperMinesGame([5,5,5], [])
        >>> g4.get_neighbors(g4.dimensions, [1,1,1], 0)
        {(0, 1, 1), (0, 1, 2), (1, 0, 0), (1, 0, 1), (0, 2, 1), (1, 0, 2), (0, 2, 0), (0, 2, 2), (2, 0, 1), (1, 2, 0), (2, 0, 0), (1, 2, 1), (0, 0, 2), (1, 2, 2), (2, 0, 2), (0, 0, 1), (0, 0, 0), (2, 1, 2), (1, 1, 1), (1, 1, 0), (2, 2, 2), (2, 1, 0), (2, 2, 1), (2, 1, 1), (1, 1, 2), (2, 2, 0), (0, 1, 0)}
        '''

        coord_list=set()

        def find_recursive_neighbors(dimensions, coord, working_coord, coord_list, depth):
            #Base
            if depth == len(dimensions):
                coord_list.add(tuple(working_coord))

            #Recursive
            else:
                for xi in range(-1, 2):
                    new_coord = working_coord[:]
                    if coord[depth] + xi < 0 or coord[depth] + xi > dimensions[depth] -1:
                        continue
                    new_coord.append(coord[depth] + xi)
                    find_recursive_neighbors(dimensions, coord, new_coord, coord_list, depth + 1)

        find_recursive_neighbors(dimensions, coord, working_coord, coord_list, depth)
        return coord_list






    def get_all_coords(self, dimensions, depth, working_coord=[], coord_list=set()):
        '''
        Similarly to get_neighbors, this function recursively
        finds all the possible coordinates available given a specific dimensions list.

        DOCTESTS:

        >>> g3 = HyperMinesGame([5,5,5], [])
        >>> g3.get_all_coords(g3.dimensions, 0)
        {(4, 2, 2), (3, 0, 3), (1, 4, 4), (2, 2, 4), (4, 4, 0), (1, 4, 2), (0, 2, 1), (1, 4, 0), (0, 2, 3), (3, 1, 4), (3, 2, 2), (2, 0, 1), (1, 2, 0), (3, 1, 2), (3, 2, 0), (2, 0, 3), (1, 2, 2), (3, 1, 0), (4, 1, 1), (1, 2, 4), (3, 2, 4), (0, 4, 2), (4, 1, 3), (0, 4, 0), (2, 3, 4), (0, 1, 0), (1, 3, 3), (4, 3, 4), (1, 0, 3), (0, 1, 2), (0, 4, 4), (1, 3, 1), (4, 3, 2), (1, 0, 1), (3, 3, 1), (3, 4, 1), (0, 1, 4), (2, 3, 0), (4, 0, 2), (4, 3, 0), (3, 3, 3), (2, 4, 0), (3, 4, 3), (2, 3, 2), (4, 0, 0), (2, 4, 2), (2, 4, 4), (0, 0, 3), (0, 3, 3), (4, 0, 4), (0, 0, 1), (0, 3, 1), (2, 2, 3), (2, 1, 3), (1, 1, 0), (2, 2, 1), (2, 1, 1), (4, 2, 1), (1, 1, 2), (3, 0, 0), (4, 4, 3), (4, 2, 3), (1, 1, 4), (3, 0, 2), (4, 4, 1), (3, 0, 4), (1, 4, 3), (0, 2, 0), (2, 0, 4), (1, 4, 1), (0, 2, 2), (4, 1, 4), (3, 1, 3), (3, 2, 3), (0, 2, 4), (2, 0, 0), (1, 2, 1), (3, 1, 1), (3, 2, 1), (2, 0, 2), (4, 1, 0), (1, 2, 3), (0, 4, 3), (4, 1, 2), (0, 4, 1), (3, 4, 4), (1, 3, 4), (1, 0, 2), (0, 1, 1), (1, 3, 2), (1, 0, 0), (3, 4, 0), (0, 1, 3), (4, 0, 3), (1, 3, 0), (4, 3, 3), (3, 3, 0), (2, 4, 1), (3, 4, 2), (2, 3, 1), (4, 0, 1), (4, 3, 1), (1, 0, 4), (3, 3, 2), (2, 4, 3), (2, 3, 3), (3, 3, 4), (0, 0, 4), (0, 3, 2), (0, 0, 2), (0, 3, 0), (2, 1, 4), (0, 0, 0), (2, 1, 2), (4, 2, 4), (1, 1, 1), (2, 2, 2), (0, 3, 4), (2, 1, 0), (1, 1, 3), (2, 2, 0), (4, 4, 4), (4, 2, 0), (3, 0, 1), (4, 4, 2)}

        '''
        coord_list=set()

        def find_recursive_coords(dimensions, depth, working_coord=[], coord_list=set()):
            #Base
            if depth == len(dimensions):
                coord_list.add(tuple(working_coord))
            #Recursive
            else:
                for xi in range(dimensions[depth]):
                    new_coord = working_coord[:]
                    new_coord.append(xi)
                    find_recursive_coords(dimensions, depth + 1, new_coord, coord_list)

        find_recursive_coords(dimensions, depth, working_coord, coord_list)
        return coord_list


    def recursiveArray(self, dimensions, depth, mask=""):
        '''
        Recursively creates an array of given dimensions. Has the option of filling with 0s or False bools.

        DOCTESTS:

        >>> g2 = HyperMinesGame([5,5,5], [])
        >>> g2.recursiveArray([5,5,5], 0)
        [[[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]]]
        '''

        val = 0
        if mask == "mask":
            val = False
        #Base Case:
        if depth == len(dimensions) - 1:
            curdim = dimensions[depth]
            array = []
            for i in range(curdim):
                array.append(val)
            return array

        #Recursive Case:
        else:
            array = []
            curdim = dimensions[depth]
            for i in range(curdim):
                array.append(self.recursiveArray(dimensions, depth + 1, mask))
            return array


    def build_bomb_count(self, array, bombs):
        '''
        Loops over the neighbors of a bomb coordinate and adds 1 per bomb to each neighbor.

        DOCTESTS:
        >>> g1 = HyperMinesGame([2,4,2], [])
        >>> g1.board = [[[0, 0], [0, 0], [0,0], [0, 0]],[[0, 0], [0, 0], [0, 0], [0, 0]]]
        >>> bombs = [[0,0,1] , [1,0,0], [1,1,1]]
        >>> g1.build_bomb_count(g1.board, bombs)
        >>> g1.board
        [[[3, '.'], [3, 3], [1, 1], [0, 0]], [['.', 3], [3, '.'], [1, 1], [0, 0]]]

        '''
        for bomb in bombs:
            for coord in self.get_neighbors(self.dimensions, bomb, 0):
                if tuple(coord) in self.bombs: #Hashable for speed
                    continue

                self.grab_obj_from_coord(array, coord, 0, "add")
            self.grab_obj_from_coord(array, bomb, 0,".")


    def set_all_values(self, dims, bombs):
        '''
        Sets all attributes that require a class method to be defined. Called by init.

        DOCTESTS:

        >>> game = HyperMinesGame([10], [])
        >>> game.set_all_values([10], [[1],[2]])
        >>> game.board
        [1, '.', '.', 1, 0, 0, 0, 0, 0, 0]
        >>> game.mask
        [False, False, False, False, False, False, False, False, False, False]
        >>> game.dimensions
        [10]

        '''
        self.dimensions = dims
        self.bombs = set()
        for bomb in bombs:
            self.bombs.add(tuple(bomb))
        self.board = self.recursiveArray(self.dimensions, 0)
        self.mask = self.recursiveArray(self.dimensions, 0, "mask")
        self.build_bomb_count(self.board, bombs)


    def dump(self):
        """Print a human-readable representation of this game."""
        lines = ["dimensions: %s" % (self.dimensions, ),
                 "board: %s" % ("\n       ".join(map(str, self.board)), ),
                 "mask:  %s" % ("\n       ".join(map(str, self.mask)), ),
                 "state: %s" % (self.state, )]
        print("\n".join(lines))

    def reveal_squares(self, coord):
        """Helper function: recursively reveal squares on the board, and return
        the number of squares that were revealed.

        DOCTESTS:


        >>> g6 = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
        ...                  [[False, False], [False, False], [False, False], [False, False]]],
        ...         "state": "ongoing"})
        >>> g6.reveal_squares([0, 3, 0])
        8
        """

        if self.grab_obj_from_coord(self.board, coord, 0) != 0:
            if self.grab_obj_from_coord(self.mask, coord, 0):
                return 0
            else:
                self.grab_obj_from_coord(self.mask, coord, 0, True)
                return 1
        else:
            revealed = set()
            for neighbor in self.get_neighbors(self.dimensions, coord, 0):
                if self.grab_obj_from_coord(self.board, neighbor, 0) != '.' and not self.grab_obj_from_coord(self.mask, neighbor, 0):
                    self.grab_obj_from_coord(self.mask, neighbor, 0, True)
                    revealed.add(tuple(neighbor))

            total = len(revealed)
            for coord in revealed:
                total += self.reveal_squares(coord)
            return total




    def dig(self, coords):
        """Recursively dig up square at coords and neighboring squares.

        Update the mask to reveal square at coords; then recursively reveal its
        neighbors, as long as coords does not contain and is not adjacent to a
        bomb.  Return a number indicating how many squares were revealed.  No
        action should be taken and 0 returned if the incoming state of the game
        is not "ongoing".

        The updated state is "defeat" when at least one bomb is visible on the
        board after digging, "victory" when all safe squares (squares that do
        not contain a bomb) and no bombs are visible, and "ongoing" otherwise.

        Args:
           coords (list): Where to start digging

        Returns:
           int: number of squares revealed

        >>> g7 = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
        ...                  [[False, False], [False, False], [False, False], [False, False]]],
        ...         "state": "ongoing"})
        >>> g7.dig([0, 3, 0])
        8
        >>> g7.dump()
        dimensions: [2, 4, 2]
        board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
               [['.', 3], [3, '.'], [1, 1], [0, 0]]
        mask:  [[False, False], [False, True], [True, True], [True, True]]
               [[False, False], [False, False], [True, True], [True, True]]
        state: ongoing
        >>> g7 = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...         "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                   [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...         "mask": [[[False, False], [False, True], [False, False], [False, False]],
        ...                  [[False, False], [False, False], [False, False], [False, False]]],
        ...         "state": "ongoing"})
        >>> g7.dig([0, 0, 1])
        1
        >>> g7.dump()
        dimensions: [2, 4, 2]
        board: [[3, '.'], [3, 3], [1, 1], [0, 0]]
               [['.', 3], [3, '.'], [1, 1], [0, 0]]
        mask:  [[False, True], [False, True], [False, False], [False, False]]
               [[False, False], [False, False], [False, False], [False, False]]
        state: defeat
        """

        if self.state != "ongoing":
            return 0

        if self.grab_obj_from_coord(self.board, coords, 0) == ".":
            self.grab_obj_from_coord(self.mask, coords, 0, True)
            self.state = "defeat"
            return 1

        revealed = self.reveal_squares(coords)
        bombs = 0
        covered_squares = 0

        for coord in self.get_all_coords(self.dimensions, 0):
            if self.grab_obj_from_coord(self.board, coord, 0) == '.':
                bombs += 1
            if not self.grab_obj_from_coord(self.mask, coord, 0):
                covered_squares += 1


        bad_squares = bombs  == covered_squares
        if not bad_squares:
            self.state = "ongoing"
        else:
            self.state = "victory"

        return revealed



    def render(self, xray=False):
        """Prepare the game for display.

        Returns an N-dimensional array (nested lists) of "_" (hidden squares),
        "." (bombs), " " (empty squares), or "1", "2", etc. (squares
        neighboring bombs).  The mask indicates which squares should be
        visible.  If xray is True (the default is False), the mask is ignored
        and all cells are shown.

        Args:
           xray (bool): Whether to reveal all tiles or just the ones allowed by
                        the mask

        Returns:
           An n-dimensional array (nested lists)

        >>> g8 = HyperMinesGame.from_dict({"dimensions": [2, 4, 2],
        ...            "board": [[[3, '.'], [3, 3], [1, 1], [0, 0]],
        ...                      [['.', 3], [3, '.'], [1, 1], [0, 0]]],
        ...            "mask": [[[False, False], [False, True], [True, True], [True, True]],
        ...                     [[False, False], [False, False], [True, True], [True, True]]],
        ...            "state": "ongoing"})
        >>> g8.render(False)
        [[['_', '_'], ['_', '3'], ['1', '1'], [' ', ' ']],
         [['_', '_'], ['_', '_'], ['1', '1'], [' ', ' ']]]

        >>> g8.render(True)
        [[['3', '.'], ['3', '3'], ['1', '1'], [' ', ' ']],
         [['.', '3'], ['3', '.'], ['1', '1'], [' ', ' ']]]
        """
        coords = self.get_all_coords(self.dimensions, 0)
        blank_board = self.recursiveArray(self.dimensions, 0)

        for coord in coords:

            if xray:
                val = self.grab_obj_from_coord(self.board, coord, 0)
                if val == 0:
                    self.grab_obj_from_coord(blank_board, coord, 0, " ")
                else:
                    self.grab_obj_from_coord(blank_board, coord, 0, str(val))

            else:
                val = self.grab_obj_from_coord(self.board, coord, 0)
                if val == 0:
                    self.grab_obj_from_coord(blank_board, coord, 0, " ")
                else:
                    self.grab_obj_from_coord(blank_board, coord, 0, str(val))

                if not self.grab_obj_from_coord(self.mask, coord, 0):
                    self.grab_obj_from_coord(blank_board, coord, 0, "_")

        return blank_board



    @classmethod
    def from_dict(cls, d):
        """Create a new instance of the class with attributes initialized to
        match those in the given dictionary."""
        game = cls.__new__(cls)
        for i in ('dimensions', 'board', 'state', 'mask'):
            setattr(game, i, d[i])
        return game


if __name__ == '__main__':
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
