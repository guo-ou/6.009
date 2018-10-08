import sys
sys.setrecursionlimit(1000)

# NO OTHER IMPORTS!

############################################################
## Problem 1
############################################################

# Inequal-a-Tree
#
# An "inequal-a-tree" data structure is a binary tree where the leaves
# of the tree are integers, but the nodes are an 'inequality' indicator,
# either the string '>' (greater than) or '<' (less than), which makes
# the claim that **all** integers in the left branch of the
# inequal-a-tree satisfy the indicator with respect to **all** values in
# the right branch of the inequal-a-tree.
#
# We will represent inequal-a-trees as a tuple, where the first element
# is the string '<' or '>'; the second element is the left branch of the
# inequal-a-tree and can be either an integer or another inequal-a-tree;
# and the third element is the right branch of the inequal-a-tree and
# again can be either an integer or another inequal-a-tree. Six example
# inequal-a-trees are shown below:
#
#     x1 = ('<', 1, 2)
#     x2 = ('<', 1, 1)
#     x3 = ('>', 1, 2)
#     x4 = ('<', ('>', 4, 3),
#                ('>', ('>', 7, 5), 2))
#     x5 = ('<', ('>', 4, 3),
#                ('>', ('>', 7, 6), 5))
#     x6 = ('>', ('>', 10, 5), 6)
#
# Write a function `true_for_all` that takes an inequal-a-tree as an
# input and returns True or False, based on whether or not the
# inequal-a-tree relationships and values throughout the inequal-a-tree
# hold true, as claimed by the inequality indicators and values in that
# tree.
#
# For the examples above:
#
#     true_for_all(x1) ==> True
#     true_for_all(x2) ==> False   # 1 is not < 1
#     true_for_all(x3) ==> False   # 1 is not > 2
#     true_for_all(x4) ==> False   # 3 is not < 2
#     true_for_all(x5) ==> True
#     true_for_all(x6) ==> False   # 5 is not > 6

def true_for_all(tree):
    def helper(node):
        if type(node) == int:
            return (node, node)
        else:
            op = node[0]
            left = node[1]
            right = node[2]

            lres = helper(left)
            if lres is False:
                return False
            else:
                left_min, left_max = lres
            rres = helper(right)
            if rres is False:
                return False
            else:
                right_min, right_max = rres


            if (op == "<" and not left_max < right_min):
            #print("left_max", left_max, "is not < right_min", right_min)
                return False
            if (op == ">" and not left_min > right_max):
            #print("left_min", left_min, "is not > right_max", right_max)
                return False

            return(min(left_min, right_min), max(left_max, right_max))

    output = helper(tree)
    return True if output else False



############################################################
## Problem 2
############################################################

# We wish to send a message to N different cities, numbered 1 through
# N. There are N carrier pigeons, each of whom has a set of cities
# that they are able to fly to. A legal assignment is one where
#  1) there's exactly one pigeon assigned to every city, and
#  2) no pigeon is assigned a city they aren't able to fly to.
#
# assign_cities(L,N) takes an N-element list L of sets where L[j] is
# the set of cities that pigeon j is able to fly to.  N is the
# number of cities.
#
# assign_cities should return None if there is no legal assignment,
# otherwise it should return an N-element list whose jth element is
# the number of the city assigned to pigeon j.
#
# Note: you'll need to think of an optimization in order to complete
# the last two tests in the time allowed.
#
# Examples:
#
# assign_cities([{3}, {1}, {2}], 3) ==> [3, 1, 2]
# assign_cities([{1,2,3}, {1,2,3}, {1,2,3}], 3) ==> [1, 2, 3]
# assign_cities([{1,2,3}, {1,2}, {1}], 3) ==> [3, 2 ,1]
# assign_cities([{1,2}, {1,2}, {1,2}], 3) ==> None
# assign_cities([set(), {1,2,3}, {2,3}], 3) ==> None

def assign_cities(L, N):
    capacities = [1 for i in range(N)]
    def helper(remaining_pidgeons):
        if remaining_pidgeons == []:
            return []

        for pref in remaining_pidgeons[0]:
            if capacities[pref - 1] > 0:
                capacities[pref - 1] -= 1
                others = helper(remaining_pidgeons[1:])
                if others is not None:
                    return [pref] + others
                else:
                    capacities[pref - 1] += 1


        return None


    return helper(L)


############################################################
## Problem 3
############################################################

# Circularly linked lists
#
# Infinite Data Structures, Inc. is developing their newest data
# structure, and needs your help. Their novel idea is a "circularly
# linked list" where each node has a value (called `val`) and a `next`
# node pointer, but *also* has a `prev` pointer to the previous
# node. Importantly, there is no first or last node in the
# circularly-linked list: what would ordinarily be thought of as the first
# and last nodes also link to each other, completing the circularly
# linked list.
#
# The company has only partially completed their implementation: you
# are asked to complete the methods below for the circularly-linked
# list node (`CLLN`) class that implements this idea, consistent with
# the docstring/doctest specifications.
#
# Note: Your score for this problem will be based on passing tests
# in test.py. However, you can also run "python3 quiz.py" to run quiz.py
# as a script to run the doctests below to aid in your debugging.

class CLLN():
    def __init__(self, val):
        """ Initialize a CLLN  that consists of only one node, holding val
        >>> x = CLLN(77)
        >>> isinstance(x, CLLN)
        True
        >>> x
        <CLLN 77>
        >>> x.next
        <CLLN 77>
        >>> x.prev
        <CLLN 77>
        >>> x.val
        77
        """
        self.val = val
        self.prev = self
        self.next = self

    def after(self, val):
        """ Create a new node holding val, and splice it into the circularly
            linked lisk at the 'next' position after the self node, returning
            the new node.
        >>> x = CLLN(77)
        >>> y = x.after(99)
        >>> x
        <CLLN 77 99>
        >>> y
        <CLLN 99 77>
        >>> x.next is y and x.prev is y and y.next is x and y.prev is x
        True
        >>> y.after(100).after(101)
        <CLLN 101 77 99 100>
        >>> x
        <CLLN 77 99 100 101>
        >>> x.prev
        <CLLN 101 77 99 100>
        """
        new_node = CLLN(val)
        new_node.prev = self
        new_node.next = self.next
        self.next.prev = new_node
        self.next = new_node
        return new_node



    def before(self, val):
        """ Create a new node holding val, and splice it into the circularly
            linked lisk at the 'prev' position before the self node, returning
            the new node.
        >>> x = CLLN(2).before(1)
        >>> x
        <CLLN 1 2>
        """
        return self.prev.after(val)

    def remove(self):
        """ if self is a singleton node (i.e., it has length 1), do nothing
            and return self.

            Otherwise, remove self from the circularly linked list
            that self is part of.  After removal, return this removed
            node; it should should be a valid CLLN of length 1, and
            the prior circularly linked list should have length one
            less than before.

        >>> x = CLLN(1).after(2).after(3).after(4).next
        >>> x
        <CLLN 1 2 3 4>
        >>> gone = x.next.remove()
        >>> x
        <CLLN 1 3 4>
        >>> gone
        <CLLN 2>
        """
        if self.next == self:
            return self

        else:
            self.prev.next = self.next
            self.next.prev = self.prev

            self.next = self
            self.prev = self
            return self


    def nodes(self):
        """ yield all CLLN *nodes* (NOT values) in the circularly-linked
            list starting from this (self) node in the "forward" direction,
            yielding each node only once
        >>> x = CLLN(77)
        >>> y = x.after(88)
        >>> [nd.val for nd in x.nodes()]
        [77, 88]
        >>> [nd.val for nd in x.next.nodes()]
        [88, 77]
        """
        origin = self
        yield self
        while self.next is not origin:
            yield self.next
            self = self.next

    def __iter__(self):
        """ yield all values in the circularly-linked starting from this (self)
            node in the "forward" direction, yielding each val once
        >>> x = CLLN(77).before(66)
        >>> list(x)
        [66, 77]
        """
        yield from (nd.val for nd in self.nodes())

    def __len__(self):
        """ return the number of nodes in the circularly-linked list """
        return len(list(self.__iter__()))


    def __repr__(self):
        """ compact representation of a full circularly-linked list, e.g.
        >>> x = CLLN(77).after(88)
        >>> x
        <CLLN 88 77>
        """
        result = "<CLLN"
        for val in self:
            result += " " + repr(val)
        result += ">"
        return result

    def __str__(self):
        """ a string representation of the internals of a single CLLN, e.g.
        >> x = CLLN(77)
        >> print(x)
        <CLLN-id-52932960>
        >> print(x.prev, x.val, x.next)
        <CLLN-id-52932960> 77 <CLLN-id-52932960>
        """
        return "<CLLN-id-"+str(id(self))+">"

    def map(self, f):
        """ create a new circularly linked list with function f applied to the
            corresponding node's val in sequence in the original CLLN given
            by self. Return the new node corresponding to the original self.

        >>> x = CLLN(1).after(2).after(3).next
        >>> x
        <CLLN 1 2 3>
        >>> x.map(lambda v: v*v)
        <CLLN 1 4 9>
        >>> x
        <CLLN 1 2 3>
        """
        start = self
        new_CLLN = CLLN(f(self.val))
        while self.next is not start:
            new_CLLN = new_CLLN.after(f(self.next.val))
            self = self.next
        return new_CLLN.next

    def reversed(self):
        """ return a new circularly linked list with elements from self in
            reversed order
        >>> x = CLLN(1).after(2).after(3).after(4).next
        >>> y = x.reversed()
        >>> y
        <CLLN 4 3 2 1>
        >>> x
        <CLLN 1 2 3 4>
        """

        new_CLLN = None
        for node in self.nodes():
            if new_CLLN is None:
                new_CLLN = CLLN(node.val)
            else:
                new_CLLN.after(node.val)

        return new_CLLN.next

if __name__ == "__main__":
    # Test with doctests. Helpful to debug individual quiz.py functions.
    import doctest
    doctest.testmod()
