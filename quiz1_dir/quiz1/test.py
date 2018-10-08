#!/usr/bin/env python3
import os
import quiz_resubmit
import unittest

TEST_DIRECTORY = os.path.dirname(__file__)

##################################################
### Problem 1: batch
##################################################

class TestProblem1(unittest.TestCase):
    def test_batch_1(self):
        # Simple cases
        inp = (9,)
        size = 4
        expect = [[9]]
        result = quiz_resubmit.batch(inp, size)
        self.assertEqual(expect, result)

        inp = (1, 2)
        size = 4
        expect = [[1,2]]
        result = quiz_resubmit.batch(inp, size)
        self.assertEqual(expect, result)

        inp = (4, 4)
        size = 4
        expect = [[4],[4]]
        result = quiz_resubmit.batch(inp, size)
        self.assertEqual(expect, result)


    def test_batch_2(self):
        # Batch fills/overflows
        inp = (1, 2, 3)
        size = 4
        expect = [[1,2,3]]
        result = quiz_resubmit.batch(inp, size)
        self.assertEqual(expect, result)

        inp = (4, 4)
        size = 5
        expect = [[4, 4]]
        result = quiz_resubmit.batch(inp, size)
        self.assertEqual(expect, result)

        inp = (4, 4, 4)
        size = 5
        expect = [[4, 4], [4]]
        result = quiz_resubmit.batch(inp, size)
        self.assertEqual(expect, result)

    def test_batch_3(self):
        # More complex cases
        inp = (13, 2, 3, 4, 3, 1, 1, 1, 4, 2, 3)
        size = 5
        expect = [[13], [2, 3], [4, 3], [1, 1, 1, 4], [2, 3]]
        result = quiz_resubmit.batch(inp, size)
        self.assertEqual(expect, result)

        inp = (6, 5, 6, 8, 6)
        size = 7
        expect = [[6, 5], [6, 8], [6]]
        result = quiz_resubmit.batch(inp, size)
        self.assertEqual(expect, result)

        inp = tuple(range(1,15))
        size = 7
        expect = [[1, 2, 3, 4], [5, 6], [7], [8], [9], [10], [11], [12], [13], [14]]
        result = quiz_resubmit.batch(inp, size)
        self.assertEqual(expect, result)

        inp = (1, 8, 3, 4, 3, 2, 4, 2, 3, 4, 2, 8, 8, 1, 1, 1, 18)
        size = 8
        expect = [[1, 8], [3, 4, 3], [2, 4, 2], [3, 4, 2], [8], [8], [1, 1, 1, 18]]
        result = quiz_resubmit.batch(inp, size)
        self.assertEqual(expect, result)

        size = 4
        expect = [[1, 8], [3, 4], [3, 2], [4], [2, 3], [4], [2, 8], [8], [1, 1, 1, 18]]
        result = quiz_resubmit.batch(inp, size)
        self.assertEqual(expect, result)

    def test_batch_4(self):
        big = 20000
        inp = (9,9,9,9,9)*big
        size = 10
        result = quiz_resubmit.batch(inp, size)
        self.assertEqual(big*5/2, len(result))
        for elt in result:
            self.assertEqual([9,9], elt)

    def test_batch_5(self):
        big = 20000
        inp = (1,3,5,9)*big
        size = 10
        result = quiz_resubmit.batch(inp, size)
        self.assertEqual(big, len(result))
        for elt in result:
            self.assertEqual([1,3,5,9], elt)


##################################################
### Problem 2: order
##################################################

class TestProblem2(unittest.TestCase):
    def test_order_1(self):
        inp = ['hi', 'yes', 'hello', 'yay']
        gold = inp[:]
        expect = ['hi', 'hello', 'yes', 'yay']
        result = quiz_resubmit.order(inp)
        self.assertEqual(expect, result)
        self.assertEqual(inp, gold, "the input list should not be mutated")

    def test_order_2(self):
        # non-alphabetic order
        inp = ['yes', 'hi', 'yay', 'hello']
        gold = inp[:]
        expect = ['yes', 'yay', 'hi', 'hello']
        result = quiz_resubmit.order(inp[:])
        self.assertEqual(expect, result)
        self.assertEqual(inp, gold, "the input list should not be mutated")

    def test_order_3(self):
        # repeated elements
        inp = ['b', 'ab', 'doh', 'aa', 'c', 'aa']
        gold = inp[:]
        expect = ['b', 'ab', 'aa', 'aa', 'doh', 'c']
        result = quiz_resubmit.order(inp[:])
        self.assertEqual(expect, result)
        self.assertEqual(inp, gold, "the input list should not be mutated")

        inp = ['it', 'was', 'the', 'best', 'of', 'times', 'it', 'was', 'the', 'worst', 'of', 'times']
        gold = inp[:]
        expect = ['it', 'it', 'was', 'was', 'worst', 'the', 'times', 'the', 'times', 'best', 'of', 'of']
        result = quiz_resubmit.order(inp[:])
        self.assertEqual(expect, result)
        self.assertEqual(inp, gold, "the input list should not be mutated")

    def test_order_4(self):
        inp = ['foo'*13, 'fab'*7+'ulous', 'bar'*2+'bang', 'anything', 'fab'*7] + ['anything']*2
        gold = inp[:]
        expect = ['foo'*13, 'fab'*7+'ulous', 'fab'*7,  'bar'*2+'bang', 'anything', 'anything', 'anything']
        result = quiz_resubmit.order(inp[:])
        self.assertEqual(expect, result)
        self.assertEqual(inp, gold, "the input list should not be mutated")

    def test_order_5(self):
        inp_1 = ['joe', 'barb', 'james', 'corey', 'larry', 'james', 'sarah', 'melissa']
        inp_2 = list(reversed(inp_1))

        gold = inp_1[:]
        expect = ['joe', 'james', 'james', 'barb', 'corey', 'larry', 'sarah', 'melissa']
        result = quiz_resubmit.order(inp_1[:])
        self.assertEqual(expect, result)
        self.assertEqual(inp_1, gold, "the input list should not be mutated")

        gold = inp_2[:]
        expect = ['melissa', 'sarah', 'james', 'james', 'joe', 'larry', 'corey', 'barb']
        result = quiz_resubmit.order(inp_2[:])
        self.assertEqual(expect, result)
        self.assertEqual(inp_2, gold, "the input list should not be mutated")


##################################################
### Problem 3: path_to_happiness
##################################################

class TestProblem3(unittest.TestCase):

    def make_field(self, nrows, ncols, f):
        return {"nrows": nrows, "ncols": ncols,
                "smiles": tuple(tuple(f(r,c) for c in range(ncols)) for r in range(nrows))}

    def check_result(self, field, happiness, result):
        self.assertIsInstance(result, list, "path should be a list")
        self.assertEqual(field["ncols"], len(result), "path length incorrect")
        last = result[0]
        for c in range(1, field["ncols"]):
            self.assertTrue(last-1 <= result[c] <= last+1, "invalid path")
            last = result[c]
        self.assertEqual(happiness, sum(field["smiles"][result[c]][c] for c in range(field["ncols"])),
                         "not maximum happiness path")

    # path_to_happiness tests
    def test_path_to_happiness_01(self):
        # single column field
        field = {"nrows": 3, "ncols": 1, "smiles": ((5,), (6,), (4,))}
        happiness = 6
        result = quiz_resubmit.path_to_happiness(field)
        self.assertTrue(result == [1])
        self.check_result(field, happiness, result)

    def test_path_to_happiness_02(self):
        # a two column field
        field = {"nrows": 3, "ncols": 2, "smiles": ((6, 25), (5, 2), (4, 35))}
        happiness = 40
        result = quiz_resubmit.path_to_happiness(field)
        self.assertTrue(result == [1,2])
        self.check_result(field, happiness, result)

        # a two column field with two solution paths; either is fine
        field = {"nrows": 3, "ncols": 2, "smiles": ((5, 18), (6, 0), (4, 18))}
        happiness = 24
        result = quiz_resubmit.path_to_happiness(field)
        self.assertTrue(result == [1,0] or result == [1,2])
        self.check_result(field, happiness, result)

    def test_path_to_happiness_03(self):
        # single row field
        field = {"nrows": 1, "ncols": 10, "smiles": ((5, 6, 4, 0, 5, 2, 1, 8, 9, 1),)}
        happiness = 41
        self.check_result(field, happiness, quiz_resubmit.path_to_happiness(field.copy()))

    def test_path_to_happiness_04(self):
        # small size fields
        field = {"nrows": 2, "ncols": 3, "smiles": ((100, 3, 5), (2, 4, 6))}
        happiness = 110
        self.check_result(field, happiness, quiz_resubmit.path_to_happiness(field.copy()))

        field = self.make_field(5, 3, lambda r, c: (r+c+2)%4)
        happiness = 8
        self.check_result(field, happiness, quiz_resubmit.path_to_happiness(field.copy()))

        field = self.make_field(4, 5, lambda r, c: abs(r-2))
        happiness = 10
        self.check_result(field, happiness, quiz_resubmit.path_to_happiness(field.copy()))

        field = self.make_field(5, 8, lambda r, c: 1 if r==c else 0)
        happiness = 5
        self.check_result(field, happiness, quiz_resubmit.path_to_happiness(field.copy()))

    def test_path_to_happiness_05(self):
        # tall fields
        field = self.make_field(20, 5, lambda r, c: (r+c+3)%7)
        happiness = 30
        self.check_result(field, happiness, quiz_resubmit.path_to_happiness(field.copy()))

        field = self.make_field(200, 4, lambda r, c: (r+c+3)%7)
        happiness = 24
        self.check_result(field, happiness, quiz_resubmit.path_to_happiness(field.copy()))

    def test_path_to_happiness_06(self):
        # wide field with 2 rows
        field = self.make_field(2, 20, lambda r, c: (r+c+2)%4)
        happiness = 45
        self.check_result(field, happiness, quiz_resubmit.path_to_happiness(field.copy()))

    def test_path_to_happiness_07(self):
        # wide field with 3 rows
        field = self.make_field(3, 15, lambda r, c: (r+c+2)%4)
        happiness = 37
        self.check_result(field, happiness, quiz_resubmit.path_to_happiness(field.copy()))

    def test_path_to_happiness_08(self):
        # medium size fields
        field = self.make_field(17, 12, lambda r, c: (r+c)%7)
        happiness = 72
        self.check_result(field, happiness, quiz_resubmit.path_to_happiness(field.copy()))

    def test_path_to_happiness_09(self):
        # large field
        field = self.make_field(47, 50, lambda r, c: (r*c)%7)
        happiness = 217
        self.check_result(field, happiness, quiz_resubmit.path_to_happiness(field.copy()))

    def test_path_to_happiness_10(self):
        # larger field
        field =self.make_field(500, 600, lambda r, c: (r*c+r+c)%7)
        happiness = 3600
        self.check_result(field, happiness, quiz_resubmit.path_to_happiness(field.copy()))

if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
