# NO IMPORTS ALLOWED!

##################################################
### Problem 1: efficiency
##################################################

def unique(input_list):
    output = []
    seen_items_set = set()
    for item in input_list:
        if item not in seen_items_set:
            seen_items_set.add(item)
            output.append(item)

    return output

    # stored_in_list = set(input_list)
    # return list(set(stored_in_list))


     # output = []
     # seen = []
     # for item in input_list:
     #     if item not in set(seen):
     #         seen = seen + [item]
     #         output = output + [item]
     # return output


##################################################
### Problem 2: phone words
##################################################

allwords = set(open('words2.txt').read().splitlines())

def is_word(i):
    return i.lower() in allwords

key_letters = {
    '2': 'ABC',
    '3': 'DEF',
    '4': 'GHI',
    '5': 'JKL',
    '6': 'MNO',
    '7': 'PQRS',
    '8': 'TUV',
    '9': 'WXYZ',
}


def phone_words(digits):


    def helper(possible_digits=None, out_set=set(), big_out_set=set()):
        if possible_digits is None:
            possible_digits = digits
            # print(possible_digits)
        # print(possible_digits)

        if possible_digits == "":
            return big_out_set
        for digit in possible_digits:
            if digit == "1" or digit == "0":
                out_set = set()
                continue
                # return helper(possible_digits[possible_digits.index(digit):], set(), big_out_set)


            # print(digit)
            possible_values = key_letters[str(digit)]

            if len(out_set) == 0:
                for letter in possible_values:
                    if is_word(letter):
                        big_out_set.append(letter)
                    out_set.add(letter)
            else:
                for existing in set(out_set):
                    out_set.remove(existing)


                    for letter in possible_values:


                        # print(existing, letter)
                        out_set.add(existing + letter)
                        if is_word(existing + letter):
                            # print(existing + letter)
                            big_out_set.add(existing + letter)


        big_out_set.union(out_set)
        return helper(possible_digits[1:],set(), big_out_set)
    output = helper()

    return output



##################################################
### Problem 3: radix trie
##################################################

from trie import Trie, RadixTrie


def dictify(t):
    """
    For debugging purposes.  Given a trie (or radix trie), return a dictionary
    representation of that structure, including the value and children
    associated with each node.
    """
    out = {'value': t.value, 'children': {}}
    for ch, child in t.children.items():
        out['children'][ch] = dictify(child)
    return out


def compress_trie(trie):
    out_trie = RadixTrie()

    #LARGE CHANGES

    # Add the value for the beginning node.
    if trie.value is not None:
        out_trie.value = trie.value

    def recurse_down(node, working_trie, working_str=""):

        #BUG from quiz: working_str for working prefixes is not resetting properly - also this cannot accommodate for
        # multiple words with a common prefix yet.

        # Quiz Solution: This was actually quite close to the correct solution. The structure
        # is almost congruent to the final solution, however, it does not properly track where
        # to store the trie objects in the out_trie. So, for cases like "cat", "bat", it works fine,
        # aside from the bug where working_str is not reset in memory each time we start a new branch.
        # All that needed to be done is to implement the working_trie (found in the final solution) such
        # that it actually stores the RadixTrie objects in the larger tree as we recurse down the trie, and
        # not just in the highest level children dictionary.

        # for letter, sub_trie in node.children.items():
        #     # print("WORKING: ",working_str)
        #     # print("LETTER: ", letter)
        #
        #     if sub_trie.value is None:
        #
        #         working_str += letter
        #         # print(working_str)
        #         recurse_down(sub_trie, working_str)
        #     else:
        #         working_str += letter
        #         new_trie = RadixTrie()
        #         new_trie.value = sub_trie.value
        #         # print("AT PLACEMENT: ", working_str)
        #         if len(working_str) == 4:
        #             working_str = working_str[1:]
        #         out_trie.children[working_str] = new_trie
        #         working_str = ""
        #





        # Second attempt after quiz: This had 3 main issues in my debugging. For one,
        # working_str was not being reset every time we began a new branch of the original trie.
        # Hence, when we encountered a trie with a branch at the first node (e.g. "cat" and "bag"),
        # This code would not reset the working_str to "", it reset to "b" as it used += instead
        # of creating a new immutable object in memory. Secondly, it was unable to account for
        # single letter differences in the first layer. So, if "bat" and "bot" both appeared, they
        # would be treated as such in out_trie.children. However, this is incorrect as we need a node
        # for "b". This was soled by moving the for loops from within the statements about "node"
        # to the beginning of the function, allowing for these first node adjustments. Finally,
        # This code could be condensed such that it resembles my final solution and the original
        # quiz solution I wrote.

        # if node.value is None and len(node.children) == 1:
        #     working_str += list(node.children.keys())[0]
        #     recurse_down(list(node.children.values())[0], working_str, working_trie)
        #
        #
        #
        # # if node.value is not None and working_str != "":
        # else:
        #     # print(node.value)
        #     new_trie = RadixTrie()
        #     new_trie.value = node.value
        #     working_trie.children[working_str] = new_trie
        #     # working_trie.children[working_str] = new_trie
        #     if node.children is not {}:
        #         for letter, sub_trie in node.children.items():
        #             recurse_down(sub_trie, "" + letter, new_trie)
        #     working_str = ""


        # else:
        #     print("WORKING: ", working_str)
        #     for letter, sub_trie in node.children.items():
        #
        #         recurse_down(sub_trie, working_str + letter, working_trie)
        # return out_trie


        # Final Attempt: realized code could be condensed from the versions above
        # Had an issue with overwriting the working_str in memory, hence the use of
        # extended. This caused "bcat" to appear in my children when it shouldn't have.
        # Also, beginning the function with a loop solved the issue that attempt 2 had
        # in which branches at the first node (i.e. "bat" and "bot") were not implemented.
        for letter, sub_trie in node.children.items():
            extended = working_str + letter
            if sub_trie.value is None and len(sub_trie.children) == 1:

                recurse_down(sub_trie, working_trie, extended)

            else:

                new_trie = RadixTrie()
                new_trie.value = sub_trie.value
                working_trie.children[extended] = new_trie
                recurse_down(sub_trie,  new_trie, "")

    recurse_down(trie, out_trie,"")

    return out_trie
