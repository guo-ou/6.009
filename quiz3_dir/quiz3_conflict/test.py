import quiz
import types
import pickle
import unittest

class TestProblem1(unittest.TestCase):
    def test_01(self):
        result = quiz.run_length_encode_2d([[0, 0, 0],
                                            [2, 2, 1],
                                            [1, 1, 1]])
        expect = [(3, 0), (2, 2), (4, 1)]
        self.assertEqual(result, expect)

        result = quiz.run_length_encode_2d([[1, 1, 1, 1, 1, 1, 1],
                                            [1, 0, 0, 0, 0, 0, 1],
                                            [1, 0, 1, 0, 1, 0, 1],
                                            [1, 0, 0, 0, 0, 0, 1],
                                            [1, 0, 1, 1, 1, 0, 1],
                                            [1, 0, 0, 0, 0, 0, 1],
                                            [1, 1, 1, 1, 1, 1, 1]])
        expect = [(8, 1), (5, 0), (2, 1), (1, 0), (1, 1), (1, 0), (1, 1),
                  (1, 0), (2, 1), (5, 0), (2, 1), (1, 0), (3, 1), (1, 0),
                  (2, 1), (5, 0), (8, 1)]
        self.assertEqual(result, expect)

    def run_test_case(self, n):
        with open('test_data/rle%d_in.pickle' % n, 'rb') as f:
            inp = pickle.load(f)
        with open('test_data/rle%d_out.pickle' % n, 'rb') as f:
            expected = pickle.load(f)
        result = quiz.run_length_encode_2d(inp)
        self.assertEqual(result, expected)

    def test_02(self):
        self.run_test_case(2)

    def test_03(self):
        self.run_test_case(3)

    def test_04(self):
        self.run_test_case(4)

    def test_05(self):
        self.run_test_case(1)


class TestProblem2(unittest.TestCase):
    words = ('as', 'ate', 'eye', 'cast', 'eyes', 'oven', 'eeee', 'wants')

    def do_test_num(self, n):
        result = quiz.word_squares(self.words[n-1])
        self.assertTrue(isinstance(result, types.GeneratorType))
        with open('test_data/words%d.pickle' % n, 'rb') as f:
            expected = pickle.load(f)
        result = list(result)
        self.assertEqual(len(result), len(expected))
        self.assertEqual(set(result), expected)

    def test_01(self):
        self.do_test_num(1)

    def test_02(self):
        self.do_test_num(2)

    def test_03(self):
        self.do_test_num(3)

    def test_04(self):
        self.do_test_num(4)

    def test_05(self):
        self.do_test_num(5)

    def test_06(self):
        self.do_test_num(6)

    def test_07(self):
        self.do_test_num(7)

    def test_08(self):
        self.do_test_num(8)


def compare(x, y):
    if x is None:
        return y is None
    elif isinstance(x, int):
        return x == y
    else:
        return ((x.__class__.__name__, x.weight, x.arrive_at, x.duration)
                    == y)

class TestProblem3(unittest.TestCase):
    def test_01(self):
        x = quiz.Pond()
        for f in (Catfish(20, 1, 3),
                  Catfish(10, 1, 3),
                  Catfish(7, 1, 3)):
            x.add_fish((17, 19), f)

        out = []
        out.append(x.weight_caught())
        out.append(x.catch_fish((17, 19), 'stinky cheese'))
        out.append(x.catch_fish((17, 19), 'cheese'))
        out.append(x.catch_fish((17, 19), 'insect'))
        for r in range(20):
            for c in range(20):
                out.append(x.catch_fish((r, c), 'stinky cheese'))
        with open('test_data/fish1.pickle', 'rb') as f:
            expected = pickle.load(f)
        self.assertEqual(len(out), len(expected))
        for i,j in zip(out, expected):

            self.assertTrue(compare(i, j))

    def test_02(self):
        x = quiz.Pond()
        for f in (Catfish(20, 1, 2),
                  Catfish(10, 1, 2),
                  Catfish(7, 1, 2),
                  StripedBass(1, 1, 3)):
            x.add_fish((12, 23), f)

        out = []
        out.append(x.weight_caught())
        out.append(x.catch_fish((12, 23), 'stinky cheese'))
        out.append(x.weight_caught())
        out.append(x.catch_fish((12, 23), 'stinky cheese'))
        out.append(x.weight_caught())
        out.append(x.catch_fish((12, 23), 'stinky cheese'))
        out.append(x.weight_caught())
        out.append(x.catch_fish((12, 23), 'stinky cheese'))
        out.append(x.weight_caught())
        out.append(x.catch_fish((12, 23), 'stinky cheese'))
        out.append(x.weight_caught())
        out.append(x.catch_fish((12, 23), 'stinky cheese'))
        out.append(x.weight_caught())
        out.append(x.catch_fish((12, 23), 'worm'))
        out.append(x.weight_caught())

        with open('test_data/fish2.pickle', 'rb') as f:
            expected = pickle.load(f)

        self.assertEqual(len(out), len(expected))
        for i,j in zip(out, expected):

            self.assertTrue(compare(i, j))

    def test_03(self):
        x = quiz.Pond()
        for f in (StripedBass(2, 20, 3), StripedBass(3, 40, 3), BlackBass(1, 20, 3), LargemouthBass(4, 40, 3)):
            x.add_fish((1, 1), f)

        out = []
        out.append(x.catch_fish((1, 1), 'worm'))
        x.wait(20)
        out.append(x.catch_fish((1, 1), 'worm'))
        out.append(x.catch_fish((1, 1), 'worm'))
        out.append(x.catch_fish((1, 1), 'worm'))
        x.wait(20)
        out.append(x.catch_fish((1, 1), 'worm'))
        out.append(x.catch_fish((1, 1), 'worm'))
        out.append(x.catch_fish((1, 1), 'worm'))
        with open('test_data/fish3.pickle', 'rb') as f:
            expected = pickle.load(f)
        self.assertEqual(len(out), len(expected))
        for i,j in zip(out, expected):
            self.assertTrue(compare(i, j))

    def test_04(self):
        x = quiz.Pond()
        for f in (A(1, 20, 6), B(4, 20, 6), C(3, 20, 6), D(2, 20, 6), E(7, 20, 6)):
            x.add_fish((1, 1), f)

        out = []
        out.append(x.catch_fish((1, 1), 'tomatoes'))
        x.wait(20)
        out.append(x.catch_fish((1, 1), 'cucumbers'))
        out.append(x.catch_fish((1, 1), 'tomatoes'))
        out.append(x.catch_fish((1, 1), 'cucumbers'))
        out.append(x.catch_fish((1, 1), 'tomatoes'))
        out.append(x.catch_fish((1, 1), 'cucumbers'))
        out.append(x.catch_fish((1, 1), 'tomatoes'))
        out.append(x.catch_fish((1, 1), 'cucumbers'))
        out.append(x.catch_fish((1, 1), 'tomatoes'))
        out.append(x.weight_caught())
        with open('test_data/fish4.pickle', 'rb') as f:
            expected = pickle.load(f)
        self.assertEqual(len(out), len(expected))
        for i,j in zip(out, expected):
            self.assertTrue(compare(i, j))

    def test_05(self):
        with open('test_data/fish5.pickle', 'rb') as f:
            expected = pickle.load(f)
        with open('test_data/fishtest1.py', 'r') as f:
            e = {}
            exec(f.read(), globals(), e)
        self.assertEqual(len(e['out']), len(expected))
        # print(e["out"])
        for i,j in zip(e['out'], expected):
            print(i,j)
            self.assertTrue(compare(i, j))

    def test_06(self):
        with open('test_data/fish6.pickle', 'rb') as f:
            expected = pickle.load(f)
        with open('test_data/fishtest2.py', 'r') as f:
            e = {}
            exec(f.read(), globals(), e)
        self.assertEqual(len(e['out']), len(expected))
        for i,j in zip(e['out'], expected):

            self.assertTrue(compare(i, j))

    def test_07(self):
        with open('test_data/fish7.pickle', 'rb') as f:
            expected = pickle.load(f)
        with open('test_data/fishtest3.py', 'r') as f:
            e = {}
            exec(f.read(), globals(), e)
        self.assertEqual(len(e['out']), len(expected))

        for i,j in zip(e['out'], expected):
            self.assertTrue(compare(i, j))


class Fish:
    def __init__(self, weight, arrive_at, duration):
        self.weight = weight
        self.arrive_at = arrive_at
        self.duration = duration

    def __repr__(self):
        return "<" + self.__class__.__name__ + ", " + str(self.weight) + ">"


class Catfish(Fish):
    eats = ['stinky cheese']

class Bass(Fish):
    eats = ['insect', 'worm']

class BlackBass(Bass):
    pass

class TemperateBass(Bass):
    pass

class BubbleBass(Bass):
    eats = ['krabby patty']

class LargemouthBass(BlackBass):
    eats = ['crankbait', 'worm', 'spinner']

class SmallmouthBass(BlackBass):
    pass

class SpottedBass(BlackBass):
    eats = ['frog', 'insect']

class StripedBass(TemperateBass):
    eats = ['eel', 'worm', 'crawfish']

class A(Fish):
    eats = ['tomatoes']

class B(A):
    pass

class C(A):
    eats = ['cucumbers']

class D(C):
    pass

class E(B, C):
    pass


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
