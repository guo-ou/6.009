#!/usr/bin/env python3
import os, unittest, collections, types
import quiz
from quiz import CLLN

TEST_DIRECTORY = os.path.dirname(__file__)

##################################################
##  Problem 1 Tests
##################################################

class TestProblem1(unittest.TestCase):
    def test_true_for_all_01(self):
        simple_cases = [(('<', 1, 2), True),
                        (('<', 1, 1), False),
                        (('<', 2, 1), False),
                        (('>', 1, 2), False),
                        (('>', 2, 2), False),
                        (('>', 3, 2), True)]
        for i in range(len(simple_cases)):
            with self.subTest(test=i):
                tree, expect = simple_cases[i]
                self.assertIs(quiz.true_for_all(tree), expect)

    def test_true_for_all_02(self):
        tree = ('>', ('>', 10, 5), 6)
        expect = False
        self.assertIs(quiz.true_for_all(tree), expect)
        tree = ('<', 6, ('>', 10, 7))
        expect = True
        self.assertIs(quiz.true_for_all(tree), expect)

    def test_true_for_all_03(self):
        tree = ('<', ('>', 4, 3), ('>', ('>', 7, 5), 2))
        expect = False
        self.assertIs(quiz.true_for_all(tree), expect)
        tree = ('<', ('>', 4, 3), ('>', ('>', 7, 6), 5))
        expect = True
        self.assertIs(quiz.true_for_all(tree), expect)

    def test_true_for_all_04(self):
        tree = ('<', ('>', 4, 1), ('<', ('<', 2, 4), 5))
        expect = False
        self.assertIs(quiz.true_for_all(tree), expect)

    def test_true_for_all_05(self):
        tree = ('<', ('>', 4, 1), ('<', 5, ('<', 7, 6)))
        expect = False
        self.assertIs(quiz.true_for_all(tree), expect)

    def test_true_for_all_06(self):
        tree = make_tree('<', list(range(100)))
        expect = True
        self.assertIs(quiz.true_for_all(tree), expect)
        self.assertIs(quiz.true_for_all(('<', tree, 0)), False)

        tree = make_tree('>', list(range(500,-1,-1)))
        expect = True
        self.assertIs(quiz.true_for_all(tree), expect)
        self.assertIs(quiz.true_for_all(('>', tree, 0)), False)


def make_tree(ineq, nums):
    n = len(nums)
    if n == 2:
        return (ineq, nums[0], nums[1])
    elif n%3 == 0:
        return (ineq, nums[0], make_tree(ineq, nums[1:]))
    elif n%5 == 0:
        return (ineq, make_tree(ineq, nums[:-1]), nums[-1])
    else:
        return (ineq, make_tree(ineq, nums[:n//2]), make_tree(ineq, nums[n//2:]))

        

##################################################
##  Problem 2 Tests
##################################################

class TestProblem2(unittest.TestCase):
    def test_cities_01(self):
        simple_cases = [([{3}, {1}, {2}], 3, [3, 1, 2]),
                        ([{1,2,3}, {1,2,3}, {1,2,3}], 3, [1, 2, 3]),
                        ([{1,2,3}, {1,2}, {1}], 3, [3, 2 ,1]),
                        ([{1,2}, {1,2}, {1,2}], 3, None),
                        ([set(), {1,2,3}, {2,3}], 3, None)]
        for i in range(len(simple_cases)):
            with self.subTest(test=i):
                L, N, expect = simple_cases[i]
                self.check_assign_cities(L, N, expect)

    def test_cities_02(self):
        L = [{10, 6, 7}, {8, 9, 4}, {8, 9, 5}, {1, 9}, {1, 2, 7},
             {8, 10, 6}, {2, 4, 6}, {10, 4}, {3}, {8, 2}]
        N = 10
        expect = not None
        self.check_assign_cities(L, N, expect)

    def test_cities_03(self):
        L = [{3, 4, 5}, {8, 10, 6}, {10, 5, 6}, {10, 3, 5}, {2, 7},
             {1, 10, 4}, {3, 4, 6}, {8, 4, 7}, {1, 10, 7}, {10, 7}]
        N = 10
        expect = None # no pigeon is able to fly to city 9
        self.check_assign_cities(L, N, expect)
            
    def test_cities_04(self):
        L = [{9, 18, 11}, {2, 19, 12}, {16, 20, 15}, {18, 12, 14}, {13, 6, 7},
             {1, 10, 19}, {9, 5}, {11, 12}, {11, 3, 20}, {9, 2}, {19, 5, 6},
             {10, 12, 13}, {18, 10, 5}, {16, 8, 4}, {2, 10, 6}, {17, 10, 3},
             {10, 11, 13}, {4, 14}, {16, 18}, {11, 4}]
        N = 20
        expect = None
        self.check_assign_cities(L, N, expect)

    def test_cities_05(self):
        L = [{16, 20, 14}, {19, 20, 13}, {8, 1}, {17, 10, 6}, {11, 9, 19},
             {16, 9, 3}, {10, 13, 14}, {2, 13, 6}, {8, 10, 5}, {2, 11},
             {16, 5, 14}, {16, 3, 20}, {12, 5, 14}, {2, 20, 15}, {2, 13, 15},
             {16, 4, 5}, {1, 2, 20}, {11, 20, 5}, {18, 4, 12}, {16, 13, 7}]
        N = 20
        expect = not None
        self.check_assign_cities(L, N, expect)

    def skip_test_cities_06(self):
        # Slow if optimization not present.
        # Even then, may take a very long time depending on how recursion is ordered.
        L = [{33, 3, 17, 49, 25, 27}, {32, 38, 20, 23, 26, 31}, {33, 9, 14, 49, 19},
             {35, 7, 40, 39, 46, 17}, {5, 7, 10, 44, 47, 20}, {36, 7, 22, 23, 28, 31},
             {36, 40, 41, 14, 21, 31}, {1, 34, 4, 36, 17, 29}, {6, 41, 43, 46, 47, 26},
             {32, 1, 40, 47, 16, 22}, {37, 5, 13, 46, 15, 21}, {35, 6, 10, 16, 29},
             {32, 33, 36, 7, 20, 21}, {35, 36, 8, 46, 19, 22}, {36, 38, 39, 14, 19, 29},
             {37, 6, 39, 16, 21, 25}, {3, 40, 12, 13, 19}, {5, 6, 43, 44, 17, 31},
             {3, 6, 9, 10, 45, 49}, {34, 35, 44, 46, 18, 26}, {34, 38, 44, 14, 16, 27},
             {32, 38, 42, 43, 18, 29}, {6, 40, 8, 45, 21, 23}, {32, 38, 41, 13, 16, 22},
             {2, 8, 46, 47, 15, 18}, {4, 7, 11, 22, 24, 28}, {3, 37, 41, 10, 45, 15},
             {2, 35, 5, 39, 8, 44}, {37, 39, 8, 41, 13, 26}, {2, 3, 6, 39, 8, 24},
             {8, 12, 13, 46, 14, 31}, {2, 35, 4, 44, 47, 28}, {5, 7, 40, 15, 17},
             {4, 42, 12, 20, 23, 28}, {33, 3, 7, 39, 45, 30}, {13, 47, 17, 23, 26, 31},
             {37, 11, 44, 45, 14, 50}, {34, 4, 11, 44, 22}, {39, 8, 43, 12, 17, 29},
             {1, 33, 37, 44, 27, 31}, {42, 43, 17, 20, 23, 25}, {1, 36, 10, 45, 48, 30},
             {35, 3, 6, 48, 18, 22}, {40, 9, 16, 49, 23, 31}, {38, 40, 41, 44, 19, 23},
             {9, 46, 48, 20, 25, 27}, {1, 6, 39, 42, 13, 45}, {41, 11, 15, 16, 22, 29},
             {3, 37, 44, 46, 25, 27}, {37, 43, 45, 50, 26, 27}]
        N = 50
        expect = not None
        self.check_assign_cities(L, N, expect)
        
    def skip_test_cities_07(self):
        # worst-case search test: requires optimization to finish in reasonable time.
        # Even then, may take a very long time depending on how recursion is ordered.
        L = [{1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20},
             {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19},
             {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18},
             {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17},
             {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16},
             {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15},
             {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14},
             {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13},
             {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12}, {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11},
             {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}, {1, 2, 3, 4, 5, 6, 7, 8, 9},
             {1, 2, 3, 4, 5, 6, 7, 8}, {1, 2, 3, 4, 5, 6, 7}, {1, 2, 3, 4, 5, 6},
             {1, 2, 3, 4, 5}, {1, 2, 3, 4}, {1, 2, 3}, {1, 2}, {1}]
        N = 20
        expect = not None
        self.check_assign_cities(L, N, expect)

    def skip_test_cities_08(self):
        # worst-case search test: requires optimization to finish in reasonable time.
        # Even then, may take a very long time depending on how recursion is ordered.
        L = [{3, 17, 49, 25, 27}, {32, 33, 20, 26, 31}, {33, 38, 9, 14, 23}, {7, 40, 9, 49, 19},
             {35, 39, 10, 46, 17}, {5, 7, 44, 47, 20}, {36, 7, 22, 23, 31}, {40, 41, 14, 21, 28},
             {34, 36, 17, 29, 31}, {1, 4, 36, 6, 47}, {1, 41, 43, 46, 26}, {32, 40, 47, 16, 22},
             {37, 5, 13, 46, 21}, {35, 10, 15, 16, 29}, {32, 33, 21, 6}, {36, 7, 46, 19, 20},
             {35, 36, 8, 14, 22}, {36, 38, 39, 19, 29}, {37, 6, 39, 21, 25}, {16, 19, 12, 13},
             {3, 40, 43, 17, 31}, {5, 6, 9, 44, 49}, {35, 3, 6, 10, 45}, {34, 44, 46, 18, 26},
             {34, 38, 44, 14, 16}, {32, 38, 18, 27, 29}, {6, 42, 43, 45, 23}, {32, 38, 40, 8, 21},
             {2, 41, 13, 16, 22}, {8, 46, 15, 47, 18}, {4, 11, 22, 24, 28}, {3, 7, 10, 45, 15},
             {35, 37, 39, 41, 44}, {2, 5, 8, 41, 13}, {37, 6, 39, 8, 26}, {2, 3, 39, 8, 24},
             {8, 12, 13, 46, 31}, {2, 4, 44, 14, 47}, {35, 7, 40, 17, 28}, {42, 20, 5, 15},
             {33, 4, 12, 23, 28}, {3, 7, 39, 45, 30}, {13, 47, 17, 23, 26}, {37, 11, 44, 45, 31},
             {4, 11, 44, 14, 50}, {34, 8, 11, 17, 22}, {1, 39, 43, 12, 29}, {33, 37, 44, 27, 31},
             {42, 43, 20, 23, 25}, {1, 36, 10, 45, 17}]
        N = 50
        expect = None
        self.check_assign_cities(L, N, expect)
        
    def legal_assignment(self, L, result):
        # defend against ill-formed results
        self.assertIsInstance(result, list)
        assigned = set()
        for i, city in enumerate(result):
            # defend against ill-formed results
            self.assertIsInstance(city, int)
            # person must be willing to do city
            self.assertIn(city, L[i])
            # city has already been assigned to another
            self.assertNotIn(city, assigned)
            assigned.add(city)
        # check if all citys were assigned
        self.assertEqual(len(set(assigned)), len(L))

    def check_assign_cities(self, L, N, expect):
        LL =[{e for e in p} for p in L]
        result = quiz.assign_cities(LL, N)
        if expect:
            self.legal_assignment(L, result)
        else:
            self.assertIsNone(result)

##################################################
##  Problem 3 Tests
##################################################

class TestProblem3(unittest.TestCase):
    def test_CLLN_01(self):
        # after (two nodes)
        x = CLLN(1)
        y = x.after(2)
        self.assertEqual(1, x.val)
        self.assertEqual(2, y.val)
        self.assertEqual("<CLLN 1 2>", repr(x))
        self.assertEqual("<CLLN 2 1>", repr(y))
        self.assertEqual(2, len(x))
        self.assertEqual(2, len(y))
        self.check(x); self.check(y)

    def test_CLLN_02(self):
        # after (three nodes)
        x = CLLN(1)
        y = x.after(2).after(3)
        self.assertEqual("<CLLN 1 2 3>", repr(x))
        self.assertEqual("<CLLN 2 3 1>", repr(x.next))
        self.assertEqual("<CLLN 3 1 2>", repr(y))
        self.check(x); self.check(y)

        # before should also work
        z = x.before(4)
        self.check(x); self.check(z)
        self.assertEqual("<CLLN 1 2 3 4>", repr(x))
        self.assertEqual("<CLLN 4 1 2 3>", repr(z))
        
    def test_CLLN_03(self):
        # len
        x = CLLN(1)
        self.assertEqual(1, len(x))
        x = x.after(2).before(3).after(4).before(5)
        self.check(x)
        self.assertEqual(5, len(x))

    def test_CLLN_04(self):
        # remove
        x = CLLN(1).after(2).after(3).after(4).next
        y = x.next
        self.check(x); self.check(y)

        z = y.remove()
        self.assertEqual(str(z), str(y), msg="removed object incorrect")
        self.assertEqual(str(z.next), str(z), msg="removed object incorrect")
        self.assertEqual(str(z.prev), str(z), msg="removed object incorrect")
        self.assertEqual("<CLLN 2>", repr(y))
        self.check(x)
        self.assertEqual("<CLLN 1 3 4>", repr(x))

        y.remove()
        self.check(x); self.check(y)
        self.assertEqual("<CLLN 2>", repr(y))
        self.assertEqual("<CLLN 1 3 4>", repr(x))
        x.next.remove()
        self.check(x); self.check(y)
        self.assertEqual("<CLLN 1 4>", repr(x))
        
    def test_CLLN_05(self):
        # map
        a = CLLN(10)
        b = a.map(lambda v: v-4)
        self.assertEqual("<CLLN 6>", repr(b))
        self.assertEqual("<CLLN 10>", repr(a))

        x = CLLN(1).after(2).after(3).after(4).next
        self.assertEqual("<CLLN 1 2 3 4>", repr(x))
        xm = x.map(lambda v: v*v)
        self.assertEqual("<CLLN 1 4 9 16>", repr(xm))
        self.assertEqual("<CLLN 1 2 3 4>", repr(x))
        self.check(x); self.check(xm)
        
    def test_CLLN_06(self):
        # reversed
        x = CLLN(1).after(2).after(3).after(4).next
        self.assertEqual("<CLLN 1 2 3 4>", repr(x))
        y = x.reversed()
        self.check(x); self.check(y)
        self.assertEqual("<CLLN 4 3 2 1>", repr(y))
        self.assertEqual([4, 3, 2, 1], list(y)) # y reversed
        self.assertEqual([1, 2, 3, 4], list(x)) # should not change x

    def test_CLLN_07(self):
        # map big; should be efficient enough not to be recursion depth limited
        x = CLLN(0)
        for i in range(1,2000): x.after(i)
        self.check(x)
        y = x.map(lambda v: v*v)
        self.assertEqual(2000, len(y))
        self.assertEqual(2664667000, sum([nd.val for nd in y.nodes()]))

    def test_CLLN_08(self):
        # reversed big; dhould be efficient enough not to be recursion depth limited
        size = 2000
        x = CLLN(0)
        for i in range(2, size*2, 2): x = x.after(i)
        x = x.next
        self.check(x)

        y = x.reversed()
        self.check(y); self.check(x)
        self.assertEqual(list(range((size-1)*2,-2,-2)), list(y))
        self.assertEqual(list(range(0, size*2, 2)), list(x)) # x should not change
        
    def check(self, x):
        for a, b in zip(x.nodes(), x.next.nodes()):
            self.assertIsInstance(a, CLLN)
            self.assertIsInstance(b, CLLN)
            self.assertEqual(str(a.next), str(b), msg="node "+str(a)+" next pointer inconsistency")
            self.assertEqual(str(b.prev), str(a), msg="node "+str(b)+" prev pointer inconsistency")


##################################################
##  test setup
##################################################

if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
