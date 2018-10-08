# NO IMPORTS!
import sys
sys.setrecursionlimit(100)
####################
## Problem 01
####################

def solve_latin_square(grid):
    n = len(grid)
    def has_contradictions(test_grid):

        col_dict = dict()
        for r in range(n):
            row_vals = set()
            for c in range(n):
                if test_grid[r][c] == -1:
                    continue



                ## Column Check
                if str(c) not in col_dict:
                    col_dict[str(c)] = set()
                if test_grid[r][c] in col_dict[str(c)]:
                    return False
                col_dict[str(c)].add(test_grid[r][c])

                if test_grid[r][c] in row_vals:
                    return False


                ## Add to Row Check only after it passes columns, don't want to add bad things
                row_vals.add(test_grid[r][c])

        return True



    def helper(working_grid=None):

        if working_grid is None:
            working_grid = grid[:]

        elif not has_contradictions(working_grid):
            return False

        for r in range(n):
            for c in range(n):
                if working_grid[r][c] == -1:

                    for i in range(1,n+1):

                        working_grid[r][c] = i

                        recur_solved = helper(working_grid)
                        if not recur_solved:
                            continue

                        else:
                            return helper(recur_solved)

                    working_grid[r][c] = -1
                    return False

        # if working_grid is None:
        #     return False


        return working_grid

    output = helper()

    return output

####################
## Problem 02
####################

def is_proper(root):
    output_dict = dict()

    # return number of black nodes on all paths if proper, else False
    def helper(working_node=None, working_path=None, count=0):
        if working_node is None:
            working_node = root
            if root["left"] == -1 and root["right"] == -1:
                return True

        if working_path is None:
            working_path = tuple()

        left = working_node["left"]
        right = working_node["right"]
        color = working_node["color"]
        # print(left, right)


        if color == "black":
            count += 1


        if left == -1:
            if working_path is not tuple():
                output_dict[working_path] = count

        if right == -1:
            if working_path is not tuple():
                output_dict[working_path] = count


        if type(left) == dict:
            helper(left, working_path + ("left",), count)

        if type(right) == dict:
            helper(right, working_path + ("right",), count)

    output = helper()
    if output:
        return True

    # print(output_dict)

    if len(set(output_dict.values())) != 1:

        return False

    return True

####################################################
## Problem 03. Prairie Dog Housing Lottery
####################################################

# Please implement the function lottery(prairie_dogs, capacities), which assigns
# prairie dogs to available burrows.  Not all prairie dogs are willing to live
# in all burrows; they have idiosyncratic individual preferences.  Furthermore,
# each borrow can only fit so many prairie dogs.  The first input value is a
# list with one element per prairie dog, where each element is itself a list of
# numbers, each number standing for an available burrow.  The second input value
# is a list giving burrow capacities.  Indices in this list correspond to
# numbers from the prairie-dog-preference lists.
#
# If an assignment exists from prairie dogs to burrows, satisfying everyone's
# preferences, then return that assignment, as a list of numbers, following
# the same order as the original list.  If no satisfactory assignment exists,
# return None.
def lottery(prairie_dogs, capacities):

    def helper(remaining_dogs):
        if remaining_dogs == []:
            return []
        else:
            for pref in remaining_dogs[0]:
                if capacities[pref] > 0:
                    capacities[pref] -= 1

                    remaining = helper(remaining_dogs[1:])
                    if remaining is None:
                        capacities[pref] += 1

                    else:
                        return [pref] + remaining
            return None
    return helper(prairie_dogs)

    # def is_violating(orientation):
    #     check_dict = dict()
    #     for burrow in orientation:
    #         if str(burrow) not in check_dict:
    #             check_dict[str(burrow)] = 1
    #         else:
    #
    #             check_dict[str(burrow)] += 1
    #
    #     for x in range(len(capacities)):
    #
    #         if str(x) in check_dict and check_dict[str(x)] > capacities[x]:
    #             return True
    #
    #     return False
    #
    # def helper(working_orientation=None):
    #     if working_orientation is None:
    #         working_orientation = [-1 for x in range(len(prairie_dogs))]
    #
    #     elif is_violating(working_orientation):
    #         return False
    #
    #     for i in range(len(prairie_dogs)):
    #         if working_orientation[i] == -1:
    #             for pref in prairie_dogs[i]:
    #
    #                 working_orientation[i] = pref
    #
    #                 recur_solved = helper(working_orientation)
    #
    #                 if not recur_solved:
    #                     continue
    #
    #                 else:
    #                     return helper(recur_solved)
    #
    #             working_orientation[i] = -1
    #             return False
    #     # if working_orientation is None:
    #     #     return False
    #     return working_orientation
    #
    # output = helper()
    # print(output)
    # if not output:
    #
    #     return None
    # return output

    # print(is_violating([0,1,0]))

    # def helper(working_orientation=None, remaining_dogs=prairie_dogs[:]):
    #     print(remaining_dogs)
    #     if working_orientation is None:
    #         working_orientation = []
    #
    #     elif is_violating(working_orientation):
    #         print("FAILING: ", working_orientation)
    #         return None
    #
    #     if len(remaining_dogs) == 0:
    #         # print(working_orientation)
    #         return working_orientation
    #
    #     for i in range(len(remaining_dogs)):
    #         # print(prairie_dogs[i])
    #         for pref in remaining_dogs[i]:
    #             working_orientation.append(pref)
    #             next_step = helper(working_orientation, remaining_dogs[1:])
    #             if next_step is None:
    #                 working_orientation = working_orientation[:-1]
    #                 continue
    #
    #             else:
    #                 return helper(next_step)
    #
    #     return working_orientation
    #
    # output = helper()
    # if is_violating(output):
    #     return None
    #
    # return output

####################################################
## Problem 04. Advanced Forestry
####################################################

def one_node_tree(data):
    return {"data": data, "left": None, "right": None, "prev": None, "next": None}

def print_tree(tree):
    def tweak_indent(indent):
        if indent == "":
            return "|_"
        else:
            return "  " + indent

    def print_tree_indented(prefix, tree, indent):
        if tree == None:
            return

        print(indent + prefix + " " + str(tree["data"]))
        if tree["prev"]:
            print(indent + "Prev: " + str(tree["prev"]["data"]))
        if tree["next"]:
            print(indent + "Next: " + str(tree["next"]["data"]))

        print_tree_indented("Left:", tree["left"], tweak_indent(indent))
        print_tree_indented("Right:", tree["right"], tweak_indent(indent))

    print_tree_indented("Root:", tree, "")

# Given a tree of the kind explained in the readme, modify it to add the new
# data value.
def insert(tree, data):
    raise NotImplementedError


####################
## Problem 05
####################

def solve_magicsquare_recursive(grid, magic_sum, choices):
    # return True if square is still solvable
    n = len(grid)

    def is_valid(sample):
        # print(sample)
        first_diag_count = 0
        sec_diag_count = 0

        col_dict = dict()
        for r in range(n):
            row_count = 0
            for c in range(n):

                if sample[r][c] == -1:
                    if r == n-1:
                        if str(c) in col_dict and  magic_sum - col_dict[str(c)] not in choices:
                            # print("HELLO")
                            return False

                        # if magic_sum - first_diag_count not in choices:
                        #     return False

                    if c == n-1 and all(sample[r][x] != -1 for x in range(n-1)):
                        if magic_sum - row_count not in choices:
                            # print("HERE")
                            return False

                    return True



                if r == c:
                    first_diag_count += sample[r][c]
                if r == n-c-1:
                    sec_diag_count += sample[r][c]


                if sample[r][c] != -1:

                    row_count += sample[r][c]
                    # print(row_count)
                    if str(c) not in col_dict:
                        col_dict[str(c)] = sample[r][c]
                    else:
                        col_dict[str(c)] += sample[r][c]
            if row_count != magic_sum:
                # print("ROW")
                return False
        # print(col_dict)
        for val in col_dict.values():
            if val != magic_sum:
                # print("COL")
                return False

        if first_diag_count != magic_sum or sec_diag_count != magic_sum:

            return False

        return True

    def helper(working_grid=None):
        # print(working_grid)
        if working_grid is None:
            working_grid = grid[:]

        elif not is_valid(working_grid):
            return False

        for r in range(n):
            for c in range(n):
                if working_grid[r][c] == -1:
                    for choice in choices:
                        working_grid[r][c] = choice
                        next_step = helper(working_grid)
                        if not next_step:
                            continue
                        return helper(next_step)

                    working_grid[r][c] = -1
                    # print("HELLO")
                    return False

        return working_grid

    output = helper()
    return output

####################
## Problem 06
####################

# The code determines if a graph can be colored using two colors or not.
# Return {} if the graph cannot be colored.
# Return coloring_dict if the graph can be colored,
# where the coloring_dict maps vertices in the graph to 'Red' or 'Blue'.
def alternating_colors(graph, start):
    out_colors = dict()

    def color_this_shit(node, color):
        if node in out_colors:
            return color == out_colors[node]

        else:
            out_colors[node] = color
            neighbors = graph[node]
            new_color = "Red" if color == "Blue" else "Blue"
            for neighbor in neighbors:
                if not color_this_shit(neighbor, new_color):
                    return False

            return True

    if color_this_shit(start, "Red"):
        return out_colors
    return {}





    # starting_node = start
    # painted = set()
    #
    #
    # def is_valid(sample_dict):
    #     # print(sample_dict)
    #     for node, color in sample_dict.items():
    #         for sub_node in graph[node]:
    #             if sub_node not in sample_dict:
    #                 return True
    #
    #             if sub_node in sample_dict and color == sample_dict[sub_node]:
    #                 return False
    #
    #             #
    #             # # if sub_node not in sample_dict:
    #             # #     return True
    #             # if sample_dict[node] == sample_dict[sub_node]:
    #             #     return False
    #
    #     return True
    #
    #
    # def helper(working_node=None, coloring_dict=None):
    #     print("NODE: ", working_node)
    #     if working_node is None:
    #         working_node = start
    #     if coloring_dict is None:
    #         coloring_dict = {start: "Red"}
    #         painted.add(start)
    #
    #
    #     elif not is_valid(coloring_dict):
    #         # print("FAILED")
    #         return False
    #
    #     print(working_node, coloring_dict)
    #     print("SUBNODES: ", graph[working_node])
    #     for sub_node in graph[working_node]:
    #
    #         print("SUB: ", sub_node)
    #         if sub_node in painted:
    #             continue
    #
    #         elif sub_node not in painted:
    #             painted.add(sub_node)
    #
    #             if coloring_dict[working_node] == "Red":
    #                 if sub_node not in coloring_dict:
    #                     coloring_dict[sub_node] = "Blue"
    #                 # print("NEW_DICT: ", coloring_dict)
    #
    #                 if is_valid(coloring_dict):
    #
    #                     return helper(sub_node, coloring_dict)
    #
    #                 # return dict()
    #
    #             elif coloring_dict[working_node] == "Blue":
    #                 if sub_node not in coloring_dict:
    #                     coloring_dict[sub_node] = "Red"
    #                 # print("NEW_DICT: ", coloring_dict)
    #                 if is_valid(coloring_dict):
    #                     return helper(sub_node, coloring_dict)
    #
    #                 # return dict()
    #
    #
    #     return coloring_dict
    #
    # output = helper()
    #
    # if not is_valid(output):
    #     return dict()
    # print(output, painted)
    # return output

####################
## Problem 07
####################

# Given a binary tree, check if it is a Binary Search Tree (BST).
# In a BST, for every vertex, the value of the vertex is greater than the
# value of any vertex in its left subtree, and less than the value of any
# vertex in its right subtree.
# return True or False depending on whether tree is a BST or not.
def check_BST(btree, start):

    def helper(node, lbound, rbound):
        value, left, right = btree[node]

        if lbound and value <= lbound:
            return False
        if rbound and value >= rbound:
            return False

        if left != "" and not helper(left, lbound, value):
            return False

        if right != "" and not helper(right, value, rbound):
            return False

        return True

    return helper(start, None, None)


    # def helper(working_node=start):
    #
    #     # if working_node not in btree:
    #     #     return False
    #     if working_node in btree:
    #         node_obj = btree[working_node]
    #         value = node_obj[0]
    #         left = node_obj[1]
    #         right = node_obj[2]
    #
    #
    #         print("NODE: ", node_obj)
    #         if left == "" and right == "":
    #             return True
    #
    #         if left in btree and value < btree[left][0]:
    #             print(btree[left][0])
    #             return False
    #         if right in btree and value < btree[right][0]:
    #             print("RIGHT")
    #             return False
    #
    #         elif btree[left][0] > btree[right][0]:
    #             print("HELLo")
    #             return False
    #
    #         else:
    #             next_right = helper(right)
    #             next_left = helper(left)
    #             print(right, next_right)
    #             print(left, next_left)
    #
    #
    #             if not next_right or not next_left:
    #                 return False
    #             return True
    #     else:
    #         return False
    #
    # return helper()

####################
## Problem 08
####################

# return minimum number of pipes of length stock_length
# that can be cut to satisfy the list of requested pipe_lengths
def pipe_cutting(requests,stock_length):
    print(requests, stock_length)
    # count = 0
    def helper(remaining_requests, length, count=0):
        print(remaining_requests, length, count)
        if remaining_requests == []:
            print(count)
            return count
        working_length = min(remaining_requests)
        min_index = remaining_requests.index(min(remaining_requests))
        remaining_length = length - working_length
        print(remaining_length)
        if all(remaining_length <= x for x in remaining_requests) or remaining_length < 0:
            print("HEY")
            count += 1
            return helper(remaining_requests[1:], stock_length, count)

        else:
            return helper(remaining_requests[:min_index] + remaining_requests[min_index + 1:], remaining_length, count)


    count = helper(requests, stock_length)

    return count


print(solve_latin_square([[2,4,5,3,1],[4,1,3,2,5],[3,2,1,5,4],[-1,-1,-1,-1,-1],[-1,-1,-1,-1,-1]]))
