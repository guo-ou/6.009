# NO IMPORTS!

##############
# Problem 01 #
##############

def find_triple(ilist):
    """ If the list ilist contains three values x, y, and z such that x + y = z
        return a tuple with x and y. Otherwise return None. """

    ilist_set = set(ilist)
    for i in ilist:
        for j in ilist:
            is_valid = i != 0 and j != 0 and i != j
            if i + j in ilist_set and is_valid:
                return (i,j)

    return None



##############
# Problem 02 #
##############

def is_quasidrome(s):
    """Check whether s is a quasidrome."""


    def check_palendrome(s):
        new_str = ""
        for i in range(len(s)):
            i = len(s) - (i+1)
            new_str += s[i]
        if new_str == s:
            return True

    if check_palendrome(s):
        return True

    for char in s:
        new_s = s[:s.index(char)] + s[s.index(char) +1:]
        if check_palendrome(new_s):
            return True

    return False
##############
# Problem 03 #
##############

def max_subsequence(ilist, is_circular = False):
    """ Return the start and end indices as a tuple of the maximum subsequence
        in the list.  If is_circular = True, imagine the list is circular.
        That is, after the end index comes the start index.  """
    final_list = []

    for i in range(len(ilist)):
        # print(len(final_list) == 0)

        #WORST CASE
        if i == len(ilist)-1 and len(final_list) == 0:
            # print("EH")

            final_list.append(ilist[-2])
            final_list.append(ilist[-1])
            return final_list

        elif i >= len(ilist) - 2:
            if len(final_list) != 0:
                return final_list
            else:
                continue

        else:
            if ilist[i] + ilist[i + 1] == ilist[i + 2]:
                final_list.append(i)


    return tuple(final_list[0], final_list[-1])




    # if is_circular:
    #     ilist = 2*ilist
    # print(len(ilist))
    #
    # def grab_next_val(index, final_list=[]):
    #     print(index)
    #     if index == len(ilist) and len(final_list) == 0:
    #
    #         final_list.append(ilist[-1])
    #         final_list.append(ilist[-2])
    #         return final_list
    #
    #     elif index == len(ilist) and len(final_list) != 0:
    #
    #         final_list.append(index)
    #         return final_list
    #
    #     else:
    #
    #         try:
    #             value = ilist[index] + ilist[index + 1]
    #             if value == ilist[index + 2]:
    #
    #                 final_list.append(index)
    #                 grab_next_val(index + 1, final_list)
    #
    #             else:
    #
    #                 grab_next_val(index + 1, final_list)
    #
    #         except:
    #
    #             final_list.append(index)
    #
    #             return final_list
    #
    #
    # new_list = grab_next_val(0)
    # print(new_list)
    # try:
    #     return (final_list[0], final_list[-1])
    # except:
    #     return None





##############
# Problem 04 #
##############

def count_triangles(edges):
    """Count the number of triangles in edges."""
    def make_edges_dict(edges):
        connections_dict = {}
        for edge in edges:
            if edge[0] not in connections_dict:
                connections_dict[edge[0]] = set(edge[1])

            if edge[1] not in connections_dict:
                connections_dict[edge[1]] = set(edge[0])


            connections_dict[edge[0]].add(edge[1])
            connections_dict[edge[1]].add(edge[0])

        return connections_dict

    connections_dict = make_edges_dict(edges)
    running_set = set()

    for node in connections_dict:
        for sec_node in connections_dict[node]:
            for third_node in connections_dict[sec_node]:
                if node in connections_dict[third_node]:
                    running_set.add((node, sec_node, third_node))


    # print(running_set)
    return len(running_set) / 6



##############
# Problem 05 #
##############

def is_unique( A ):
    """ return True if no repeated element in list A. """
    set_A = set(A[:])
    if len(set_A) == len(A):
        return True
    else:
        return False


##############
# Problem 06 #
##############

def matrix_product( A, B, m, n, k ):
    """ compute m-by-k product of m-by-n matrix A with n-by-k matrix B. """

    output_mat = []
    #(mxk)
    value = 0
    for i in range(len(A)):
        print(i+1)

        try:
            value += A[i] * B[i + k]
        except:
            pass

        if (i + k) == len(B):
            break
        if (i+1) % n == 0:
            print("ADD")
            output_mat.append(value)
            value = 0


    return output_mat







##############
# Problem 07 #
##############

def mode( A ):
    """ return the most common value in list A. """

    eleset = set(A[:])
    value_dict = {}
    for ele in eleset:
        value_dict[str(ele)] = 0

    for ele in A:
        if ele in eleset:
            value_dict[str(ele)] += 1


    keys = []
    items = []
    for key, item in value_dict.items():
        keys.append(key)
        items.append(item)


    return int(keys[items.index(max(items))])



##############
# Problem 08 #
##############

def transpose( A, m, n ):
    """ return n-by-m transpose of m-by-n matrix A. """
    row = []
    array = []
    for i in range(len(A)):
        row.append(A[i])

        if (i+1) % n == 0 :
            array.append(row)
            row = []

    row = []
    final_array = []
    for i in range(len(array[0])):
        for ele in array:
            row.append(ele[i])
        final_array.append(row)
        row = []

    running_list = []
    for row in final_array:
        for ele in row:
            running_list.append(ele)


    return running_list
##############
# Problem 09 #
##############

def check_valid_paren(s):
    """return True if each left parenthesis is closed by exactly one
    right parenthesis later in the string and each right parenthesis
    closes exactly one left parenthesis earlier in the string."""

    lcount = 0
    rcount = 0
    if s[0] == ")" or s[-1] == "(":
        return False

    for char in s:
        if char == "(":
            lcount += 1
        elif char == ")":
            rcount += 1

    return(lcount == rcount)


##############
# Problem 10 #
##############

def get_all_elements(root):
    """ Return a list of all numbers stored in root, in any order. """

    def grab_LR(node, value_set=set()):
        if node["left"] == None and node["right"] == None:
            return value_set

        else:
            if node["left"] != None:
                grab_LR(node["left"], value_set)








##############
# Problem 11 #
##############

def find_path(grid):
    """ Given a two dimensional n by m grid, with a 0 or a 1 in each cell,
        find a path from the top row (0) to the bottom row (n-1) consisting of
        only ones.  Return the path as a list of coordinate tuples (row, column).
        If there is no path return None. """
    raise NotImplementedError


##############
# Problem 12 #
##############

def longest_sequence(s):
    """ find sequences of a single repeated character in string s.
        Return the length of the longest such sequence. """
    if len(s) == 0:
        return 0
    count_list = set()
    past_char = s[0]
    count = 0
    for i  in range(len(s)):
        # print(cha r)
        if s[i] == past_char:
            count += 1
            if i == len(s) -1:
                count_list.add(count)


        else:

            past_char = s[i]
            count_list.add(count)
            count = 1

    return(max(count_list))




##############
# Problem 13 #
##############

# straightforward enumeration
def integer_right_triangles(p):
    """Let p be the perimeter of a right triangle with integral, non-zero
       length sides of length a, b, and c.  Return a sorted list of
       solutions with perimeter p.
    """
    triangles = []
    used_lenghts = set()
    for a in range(p):
        used_lenghts.add(a)
        for b in range(p):
            c = (a**2 + b**2)**.5
            if c + a + b == p and a != 0 and b != 0 and b not in used_lenghts:
                triangles.append([a,b,int(c)])

    return triangles




##############
# Problem 14 #
##############

def encode_nested_list(seq):
    """Encode a sequence of nested lists as a flat list."""

    def lowest_depth(depth, final_depth, obj=seq):
        print(obj)
        has_list = False
        for x in obj:
            if isinstance(x, list):
                has_list = True

        if depth == final_depth or not has_list:
            return obj

        else:
            for element in obj:
                lowest_depth(depth + 1, final_depth, element)


    print(lowest_depth(0, 10))



# A = [1,2,3,4,5,6]
# B = [1,2]
# m,n,k = 3,2,1
#
# print(matrix_product(A,B,m,n,k))
#


# s = "ASDF"
# print(s[:s.index("D")] + s[s.index("D") +1:])

# ilist = [1,55,3,-100,30,80]
# print(max_subsequence(ilist))
# big1 = [175, 96, 280, 389, 346, 22, 182, 350, 203, 275, 313, 305, 287, 320, 1, 44, 277, 56, 412, 374, 175, 116, 64, 127,437, 439]
#
# #
# print(find_triple(big1))
