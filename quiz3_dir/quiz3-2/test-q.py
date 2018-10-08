#!/usr/bin/env python3
import quiz
import os, unittest, collections, types
import pickle
from copy import deepcopy

TEST_DIRECTORY = os.path.dirname(__file__)

##################################################
##  Problem 1
##################################################


class TestProblem1(unittest.TestCase):
    graph1 = {'a': {'b', 'c'},
              'b': {'a', 'b', 'f'},
              'c': {'c'},
              'd': {'e', 'd', 'c'},
              'e': {},
              'f': {'a'},
    }

    def test_01(self):
        G = {'a': {'b'},
             'b': {'c'},
             'c': {}}

        expect = {('a', 'b')}
        result = set(quiz.all_simple_paths(deepcopy(G),'a','b'))
        self.verify(G, 'a', 'b', len(expect), result)
        self.assertEqual(expect, result)

        expect = {('b', 'c')}
        result = set(quiz.all_simple_paths(deepcopy(G),'b','c'))
        self.assertEqual(expect, result)

        expect = {('a', 'b', 'c')}
        result = set(quiz.all_simple_paths(deepcopy(G),'a','c'))
        self.assertEqual(expect, result)

        expect = set()
        result = set(quiz.all_simple_paths(deepcopy(G),'c','a'))
        self.assertEqual(expect, result)

    def test_02(self):
        G = {'a': {'b', 'c'},
             'b': {'c'},
             'c': {}}

        expect = {('a', 'b')}
        result = set(quiz.all_simple_paths(deepcopy(G),'a','b'))
        self.assertEqual(expect, result)

        expect = {('b', 'c')}
        result = set(quiz.all_simple_paths(deepcopy(G),'b','c'))
        self.assertEqual(expect, result)

        expect = {('a', 'b', 'c'), ('a', 'c')}
        result = set(quiz.all_simple_paths(deepcopy(G),'a','c'))
        self.verify(G, 'a', 'c', len(expect), result)
        self.assertEqual(expect, result)

    def test_03(self):
        G = {'a': {'b', 'c'},
             'b': {'c', 'a'},
             'c': {}}

        expect = {('a', 'b')}
        result = set(quiz.all_simple_paths(deepcopy(G),'a','b'))
        self.verify(G, 'a', 'b', len(expect), result)
        self.assertEqual(expect, result)

        expect = {('b', 'a', 'c'), ('b', 'c')}
        result = set(quiz.all_simple_paths(deepcopy(G),'b','c'))
        self.verify(G, 'b', 'c', len(expect), result)
        self.assertEqual(expect, result)

        expect = {('a', 'b', 'c'), ('a', 'c')}
        result = set(quiz.all_simple_paths(deepcopy(G),'a','c'))
        self.verify(G, 'a', 'c', len(expect), result)
        self.assertEqual(expect, result)

    def test_04(self):
        G = self.graph1
        expect = {('b', 'a'), ('b', 'f', 'a')}
        result = quiz.all_simple_paths(deepcopy(G),'b', 'a')
        self.verify(G, 'b', 'a', len(expect), result)
        self.assertEqual(expect, result)

    def test_05(self):
        # small fully connected graph
        size = 4
        graph = {n: {v for v in range(size)} for n in range(size)}
        expect = {(0, 1, 3), (0, 3), (0, 2, 3), (0, 2, 1, 3), (0, 1, 2, 3)}
        result = quiz.all_simple_paths(deepcopy(graph),0, size-1)
        self.verify(graph, 0, size-1, len(expect), result)
        self.assertEqual(expect, result)

    def test_06(self):
        # medium NOT fully connected graph
        size = 6
        graph = {n: {v for v in range(size)} for n in range(size)}
        graph[1] = {}
        expect = {(0, 4, 5), (0, 4, 2, 3, 5), (0, 4, 3, 2, 5), (0, 2, 3, 4, 5), (0, 2, 4, 3, 5),
                  (0, 3, 5), (0, 2, 4, 5), (0, 4, 2, 5), (0, 5), (0, 3, 4, 5), (0, 2, 5),
                  (0, 3, 2, 5), (0, 3, 4, 2, 5), (0, 4, 3, 5), (0, 2, 3, 5), (0, 3, 2, 4, 5)}
        result = quiz.all_simple_paths(deepcopy(graph),0, size-1)
        self.verify(graph, 0, size-1, len(expect), result)
        self.assertEqual(expect, result)

    def test_07(self):
        # large complex connected graph
        size = 10
        graph = {n: {v for v in range(size)} for n in range(size)}
        for i in range(2, size//2):
            graph[i] = {i-1}
        expect_len = 1109
        result = quiz.all_simple_paths(deepcopy(graph),0, size-1)
        #print("len result:", len(result))
        self.verify(graph, 0, size-1, expect_len, result)

    def verify(self, graph, start, end, num_expect, result):
        self.assertIsInstance(result, set, msg="result should be a set")
        self.assertEqual(num_expect, len(result), msg="wrong number of paths")
        for p in result:
            self.assertIsInstance(p, tuple, "path should be a tuple")
            self.assertEqual(start, p[0], msg="path should start with "+str(start))
            self.assertEqual(end, p[-1], msg="path should end with "+str(end))
            for s, t in zip(p, p[1:]):
                self.assertIn(t, graph[s], msg="no edge from "+str(s)+" to "+str(t))

##################################################
##  Problem 2
##################################################


def item_convert(i):
    if isinstance(i, (type(None), int, float)):
        return i
    elif isinstance(i, Item):
        return (i.__class__.__name__, i.price, i.owner)


class TestProblem2(unittest.TestCase):
    def test_01(self):
        m = quiz.Market()
        self.assertIsInstance(m, quiz.Market)

        a = Vehicle('Anne', 100)
        sold = m.offer_to_sell(a)
        self.assertIsNone(sold)

        sold = m.offer_to_buy(Vehicle('Bob', 90))
        self.assertIsNone(sold)

        sold = m.offer_to_buy(Vehicle('Carl', 110))
        self.assertIsInstance(sold, Vehicle)
        self.assertEqual(sold.owner, 'Carl')
        self.assertEqual(sold.price, 100)
        self.assertIs(sold, a)

        sold = m.offer_to_sell(Vehicle('Dan', 85))
        self.assertIsInstance(sold, Vehicle)
        self.assertEqual(sold.owner, 'Bob')
        self.assertEqual(sold.price, 90)


    def test_02(self):
        m = quiz.Market()
        a = Vehicle('Anne', 100)
        sold = m.offer_to_sell(a)
        self.assertIsNone(sold)

        sold = m.offer_to_buy(Truck('Carl', 110))
        # Anne's Vehicle may not be a Truck, so Carl won't buy
        self.assertIsNone(sold)

        e = F150('Erik', 125)
        sold = m.offer_to_sell(e)
        # Erik's F150 Truck costs more than Carl is willing to pay
        self.assertIsNone(sold)

        sold = m.offer_to_buy(Truck('Fiona', 150))
        # Fiona is willing to buy any truck, so buys Erik's
        self.assertIsInstance(sold, F150)
        self.assertIs(sold, e)
        self.assertEqual(sold.owner, 'Fiona')
        self.assertEqual(sold.price, 125)

        sold = m.offer_to_buy(Truck('Fiona', 150))
        # Fiona wants another truck. But there are no more for sale for 150 or less
        self.assertIsNone(sold)

        g = Ram('Greg', 35)
        sold = m.offer_to_sell(g)
        # Greg is willing to sell a beat-up Ram Truck. Fiona still wants one, so buys Greg's
        self.assertIsInstance(sold, Ram)
        self.assertIsInstance(sold, Truck)
        self.assertIsInstance(sold, Vehicle)
        self.assertIs(sold, g)
        self.assertEqual(sold.owner, 'Fiona')
        self.assertEqual(sold.price, 150)


    def test_03(self):
        m = quiz.Market()
        self.assertIsInstance(m, quiz.Market)

        d1 = D('doug', 10)
        d2 = D('dave', 20)
        sold = m.offer_to_sell(d1)
        self.assertIsNone(sold)

        sold = m.offer_to_sell(d2)
        self.assertIsNone(sold)

        sold = m.offer_to_buy(A('abby', 25))
        self.assertIsInstance(sold, D)
        self.assertIs(sold, d1)
        self.assertEqual(sold.owner, 'abby')
        self.assertEqual(sold.price, 10)

        sold = m.offer_to_buy(B('abby', 25))
        self.assertIsInstance(sold, D)
        self.assertIs(sold, d2)
        self.assertEqual(sold.owner, 'abby')
        self.assertEqual(sold.price, 20)

    def run_big_test(self, n):
        with open('test_data/marketout%d.pickle' % n, 'rb') as f:
            expected = pickle.load(f)
        with open('test_data/markettest%d.py' % n, 'r') as f:
            e = {}
            exec(f.read().replace('Market', 'quiz.Market', 1), globals(), e)
        self.assertEqual(len(e['out']), len(expected))
        for i,j in zip(e['out'], expected):
            self.assertEqual(item_convert(i), j)

    def test_04(self):
        self.run_big_test(1)

    def test_05(self):
        self.run_big_test(2)

    def test_06(self):
        self.run_big_test(3)

    def test_07(self):
        self.run_big_test(4)

class Item:
    def __init__(self, owner, price):
        self.owner = owner
        self.price = price

    def __repr__(self):
        return "<" + self.__class__.__name__ + ", " + str(self.owner) + ", " + str(self.price) + ">"

    def is_a_kind_of(self, other):
        return isinstance(self, type(other))

class Vehicle(Item): pass
class Sedan(Vehicle): pass
class Truck(Vehicle): pass
class SUV(Vehicle): pass
class F150(Truck): pass
class Ram(Truck): pass
class Car(Vehicle): pass
class Spaceship(Item): pass
class Toaster(Item): pass
class DeluxeToaster(Toaster): pass
class Corolla(Car): pass

class A(Item): pass
class B(A): pass
class C(A): pass
class D(B, C): pass


##################################################
##  Problem 3
##################################################

class TestProblem3(unittest.TestCase):
    allwords = frozenset(open('words2.txt').read().splitlines())

    def test_01(self):
        top = 'at'; total_squares = 3
        g = quiz.word_squares(top)
        self.check_square(top, g, check_n=3, check_total=-1)

    def test_02(self):
        top = 'is'; total_squares = 2
        g = quiz.word_squares(top)
        self.check_square(top, g, check_n=2, check_total=total_squares)
        # Generator should work more than once within same process...
        top = 'ad'; total_squares = 3
        g = quiz.word_squares(top)
        self.check_square(top, g, check_n=2, check_total=total_squares)

    def test_03(self):
        top = 'bar'; total_squares = 1743
        g = quiz.word_squares(top)
        self.check_square(top, g, check_n=1743, check_total=total_squares)

    def test_04(self):
        top = 'fast'; total_squares = 202505
        g = quiz.word_squares(top)
        self.check_square(top, g, check_n=20, check_total=total_squares)

    def test_05(self):
        top = 'drink'; total_squares = 673052
        g = quiz.word_squares(top)
        self.check_square(top, g, check_n=20, check_total=total_squares)

    def test_06(self):
        top = 'wristbands'; total_squares = 9551927
        g = quiz.word_squares(top)
        self.assertIsInstance(g, types.GeneratorType)
        l = list(g)
        self.assertEqual(len(l), total_squares)
        s = set(l)
        self.assertEqual(len(l), len(s))
        for i in range(1000):
            self.validate(top, [s.pop()], 1)

    def check_square(self, top, result_gen, check_n=0, check_total=-1):
        self.assertIsInstance(result_gen, types.GeneratorType, "word_squares should be a generator")
        if check_n >= 0: # verify first check_n yields from result_gen
            results = self.get_some(result_gen, check_n)
            self.validate(top, results, check_n)
        if check_total >= 0: # verify total count of items from generator is correct
            results += list(result_gen)
            self.validate(top, results, check_total)

    def validate(self, top, results, count):
        # Validate that list of results are all (non-duplicative)
        # square_word tuples, and the right number of results are
        # provided.
        for res in results:
            self.assertIsInstance(res, tuple, msg="word_squares should yield tuples")
            words = set(res)
            self.assertEqual(len(res), 4, msg="tuples from word_squares should have 4 different strings")
            for w in res:
                self.assertIn(w, TestProblem3.allwords, msg="word in result is not in words2.txt")

            top, right, bot, left = res
            self.assertEqual(top[0], left[0])
            self.assertEqual(top[-1], right[0])
            self.assertEqual(bot[0], left[-1])
            self.assertEqual(bot[-1], right[-1])

        rset = set(results)
        self.assertEqual(len(rset), len(results), msg="word_squares should not yield duplicates")
        self.assertEqual(len(results), count, "wrong number of square_word tuples produced")

    def get_some(self, g, n):
        res = []
        for i in range(n):
            try: res.append(next(g))
            except StopIteration: pass
        return res


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
