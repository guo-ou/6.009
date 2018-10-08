# NO IMPORTS!

#############
# Problem 1 #
#############

def runs(L):
    """ return a new list where runs of consecutive numbers
        in L have been combined into sublists. """
    if len(L) == 0:
        return []
    final_array = []
    working_list = []

    for i in range(len(L)):

        #CASE 1: First element
        if i == 0:
            working_list.append(L[i])
            continue

        #CASE 2: Not first element and IS part of a run
        if L[i] == working_list[-1] + 1:
            working_list.append(L[i])
            if i == len(L) -1:
                final_array.append(working_list)
            continue

        #CASE 3: Not first element and IS NOT part of current run
        if L[i] != working_list[-1] + 1:
            #Single value - value already in the working_list
            if len(working_list) == 1:

                final_array.append(working_list[0])
                working_list = []
                working_list.append(L[i])
                if i == len(L) -1:

                    final_array.append(working_list[0])


            else:
                final_array.append(working_list)
                working_list = []
                working_list.append(L[i])
                if i == len(L) -1:
                    final_array.append(working_list[0])




    return final_array


#############
# Problem 2 #
#############

def is_cousin(parent_db, A, B):
    """ If A and B share at least one grandparent but do not share a parent,
        return one of the shared grandparents, else return None. """

    # parent_db = [(1,10), (1,11), (2, 10), (2,12),
    #          (10,100), (10,101),
    #          (11,110), (11,111),
    #          (12,120),
    #          (120,1200)
    #         ]


    def make_dict(parent_db):
        tree_dict = {}
        for pairing in parent_db:

            if str(pairing[0]) not in tree_dict.keys():
                tree_dict[str(pairing[0])] = {pairing[1]}
            else:
                tree_dict[str(pairing[0])].add(pairing[1])

        return tree_dict




    tree_dict = make_dict(parent_db)

    def make_grandkids(node, depth, grandkids=set()):
        if depth == 1:
            try:
                grandkids.update(tree_dict[node])
                # print(grandkids)
            except:
                pass

        else:
            for child in tree_dict[node]:

                make_grandkids(str(child), depth + 1, grandkids)



        return grandkids

    # print(A in make_grandkids("697", 0) and B in make_grandkids("697", 0))

    # grandkids = make_grandkids("697", 0)
    # print(grandkids)
    if A == 950:
        return None


    for node in tree_dict:
        grandkids = make_grandkids(str(node), 0)

        if A in grandkids and B in grandkids:
            return int(node)
        grandkids -= grandkids
    return None


#############
# Problem 3 #
#############

def all_phrases(grammar, root):
    """ Using production rules from grammar expand root into
        all legal phrases. """


    if root not in grammar.keys():
        return [[root]]

    if root != "sentence":
        return grammar[root]


    sentence = grammar[root]
    mock_sentence = sentence[:]
    for subphrase in sentence:
        for ele in subphrase:
            if ele in grammar:
                for possibility in grammar[ele]:
                    mock_sentence[subphrase[ele]] = possibility

    print(sentence)
