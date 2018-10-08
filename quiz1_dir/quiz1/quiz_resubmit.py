# NO IMPORTS!

##################################################
### Problem 1: batch
##################################################

def batch(inp, size):
    """ Return a list of batches, per quiz specification """
    working_list = []
    final_list = []
    for ele in list(inp):
        working_list.append(ele)
        if sum(working_list) >= size:
            final_list.append(working_list)
            working_list = []
    if len(working_list) != 0:
        final_list.append(working_list)
    return final_list




##################################################
### Problem 2: order
##################################################

def order(inp):
    """ Return an ordered list of string, per quiz specification """
    output = []
    working_char = ""
    used = set()
    for ele in inp:
        if ele[0] in used:
            continue
        working_char = ele[0]
        used.add(working_char)
        for ele2 in inp:
            if ele2[0] == working_char:
                output.append(ele2)

    return output
##################################################
### Problem 3: path_to_happiness
##################################################

def path_to_happiness(field):
    """ Return a path through field of smiles that maximizes happiness """

    ncols = field["ncols"]
    nrows = field["nrows"]
    grid = field["smiles"]

    def blank_board(nrows, ncols):
        """
        Returns a board of all 0s --> used to fill in partial happiness sums
        """
        return [[0 for c in range(ncols)] for r in range(nrows)]

    partial_board = blank_board(nrows, ncols) #instantiate a partial sum board each element will correspond to the max happiness over a path to that point

    path_to_dict = {} #Will contain tuple coordinate keys, and list values corresponding to the best path to that point.


    for c in range(ncols): #loop each column, then each row in each column
        for r in range(nrows):
            if c == 0:
                #fill the first column with the minimum values from the smile board
                partial_board[r][c] = grid[r][c]
                path_to_dict[(r,c)] = [r]
            else:
                #search the neighbors from the column before and find the max happiness val --> add to the current column, and append the row value to the current path
                best_val = 0 #best happiness from previous column
                for i in range(-1, 2):
                    if 0<=r + i<nrows and 0<= c-1< ncols: #correct list indexing issues
                        if partial_board[r+i][c-1] >= best_val:

                            best_val = partial_board[r+i][c-1]
                            partial_board[r][c] = best_val + grid[r][c] #assign partial sum to the cell
                            path_to_dict[(r,c)] = path_to_dict[(r+i, c-1)] + [r] #put the new path of max happiness in the dictionary
                        else:
                            continue

    final_list = [partial_board[r][ncols-1] for r in range(nrows)] #make a list of the max happiness values for all cells in the last column
    final_row_index = final_list.index(max(final_list)) #grab the index of the best

    return path_to_dict[(final_row_index, ncols-1)] #return the path of the best option.

    #OLD QUIZ: --> Bug listed under BUG. Main issue is that my algorithm did not check more than one neighbor for the best move.
    #The recursive solution below finished before it checked the next option. Theoretically, this solution would work with this
    #bug fixed, but it is still not efficient enough.

    # def get_neighbors(row,col):
    #     return [(row + 1, col+1), (row, col+1), (row-1, col+1)]
    #
    # def helper(row, col=0, path=[], happiness=0, happiness_dict={}):
    #
    #
    #
    #     if col == ncols:
    #         if len(path) == ncols:
    #             happiness_dict[str(happiness)] = path
    #         col = 0
    #
    #     else:
    #         for i in range(row-1, row+2):
    #             if 0 <= i < nrows:
    #                 #BUG: NOT SEARCHING THE ROW BELOW THE FIRST ONE THAT SUCCEEDS: returns before it can search the next one
    #                 #could've used BFS algorithm
    #                 path.append(i)
    #                 happiness += grid[i][col]
    #                 helper(i, col + 1, path, happiness, happiness_dict)
    #                 happiness = 0
    #                 path = []
    #
    #     return happiness_dict
    #
    #
    #
    # happiness_dict = {}
    # for r in range(nrows):
    #     happiness_dict.update(helper(r,0,[],0,{}))
    #
    #
    #
    # return happiness_dict[str(max(happiness_dict))]
