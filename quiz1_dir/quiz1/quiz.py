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

    # print(nrows)
    def get_neighbors(row,col):
        return [(row + 1, col+1), (row, col+1), (row-1, col+1)]

    def helper(row, col=0, path=[], happiness=0, happiness_dict={}):



        if col == ncols:
            if len(path) == ncols:
                happiness_dict[str(happiness)] = path
            col = 0

        else:
            for i in range(row-1, row+2):
                if 0 <= i < nrows:
                    #BUG: NOT SEARCHING THE ROW BELOW THE FIRST ONE THAT SUCCEEDS: returns before it can search the next one
                    #could've used BFS algorithm
                    path.append(i)
                    happiness += grid[i][col]
                    helper(i, col + 1, path, happiness, happiness_dict)
                    happiness = 0
                    path = []

        return happiness_dict



    happiness_dict = {}
    for r in range(nrows):
        happiness_dict.update(helper(r,0,[],0,{}))



    return happiness_dict[str(max(happiness_dict))]
