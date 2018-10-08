#!/usr/bin/env python3
import unittest
import quiz

##################################################
##  Problem 1 Tests
##################################################

class TestProblem1(unittest.TestCase):
    def test_01(self):
        self.assertEqual(quiz.constant_fold(('+', 'a', ('+', 'b', ('+', ('+', 3, 5), 'c')))),
                         ('+', 'a', ('+', 'b', ('+', 8, 'c'))))

    def test_02(self):
        self.assertEqual(quiz.constant_fold(('+', 'a', ('+', ('*', ('+', 3, 5), 6), 'b'))),
                         ('+', 'a', ('+', 48, 'b')))

    def test_03(self):
        self.assertEqual(quiz.constant_fold(('+', 'a', ('+', ('*', 'b', 0), 'c'))),
                         ('+', 'a', 'c'))

    def test_04(self):
        self.assertEqual(quiz.constant_fold(('*', 1, ('+', 0, ('*', ('+', 'x', 0), 1)))),
                         'x')

    def test_05(self):
        self.assertEqual(quiz.constant_fold(('+', 7, ('*', 'x', ('-', 7, ('+', 4, 3))))),
                         7)

    def test_06(self):
        self.assertEqual(quiz.constant_fold(('*', 'a', ('-', 'b', 0))),
                         ('*', 'a', 'b'))

    def test_07(self):
        self.assertEqual(quiz.constant_fold(('+', 1, ('*', 2, ('-', 3, 2)))),
                         3)

    def test_08(self):
        self.assertEqual(quiz.constant_fold(('+', 'x', ('+', 'x', 'x'))),
                         ('+', 'x', ('+', 'x', 'x')))

##################################################
##  Problem 2 Tests
##################################################

import json

class TestProblem2(unittest.TestCase):
    # one example from the readme
    def test_09(self):
        db = [['state', 'capital', 'population'],
              ['Massachusetts', 'Boston', 6547629],
              ['California', 'Sacramento', 37253956],
              ['New York', 'Albany', 19378102]]
        result = quiz.select(db, ['state','capital'],
                             filters=[('>',['population'],10000000)])

        self.assertEqual(result,
                         [['California', 'Sacramento'],
                          ['New York', 'Albany']])

    def database(self):
        with open('baseball.json', 'r') as f:
            return json.load(f)

    # first 5 players in the table
    def test_10(self):
        bbstats = self.database()
        result = quiz.select(bbstats, ['player','year','team'])

        self.assertTrue(len(result) >= 5)
        self.assertEqual(result[:5],
                         [['Laird, Gerald', 2010, 'DET'],
                          ['Rzepczynski, Marc', 2010, 'TOR'],
                          ['Brown, Corey', 2013, 'WAS'],
                          ['Canzler, Russ', 2011, 'TBA'],
                          ['Thole, Josh', 2015, 'TOR']])

    # top 10 players by salary on 2013 BOS Redsox
    def test_11(self):
        bbstats = self.database()
        result = quiz.select(bbstats, ['player','year','salary'],
                             filters=[('=',['year'],2013), ('=',['team'],'BOS'),
                                      ('!=',['year'],['salary'])
                                      # This last one is to make sure your code is general enough,
                                      # though admittedly it doesn't make too much sense w.r.t. the
                                      # English description for this query!
                                  ],
                             order_by=('salary','desc'))

        self.assertTrue(len(result) >= 10)

        self.assertEqual(result[:10], [['Peavy, Jake', 2013, 16157271],
                                       ['Lackey, John', 2013, 15950000],
                                       ['Ortiz, David', 2013, 14500000],
                                       ['Dempster, Ryan', 2013, 13250000],
                                       ['Victorino, Shane', 2013, 13000000],
                                       ['Lester, Jon', 2013, 11625000],
                                       ['Pedroia, Dustin', 2013, 10250000],
                                       ['Drew, Stephen', 2013, 9500000],
                                       ['Ellsbury, Jacoby', 2013, 9000000],
                                       ['Hanrahan, Joel', 2013, 7040000]])


    # top 14 AL players by average with more than 100 AB
    def test_12(self):
        bbstats = self.database()
        result = quiz.select(bbstats, ['player','year','team','average'],
                             filters=[('>',['AB'],100), ('=','AL',['league']),
                                      ('!=',13,16)
                                      # This last one is to make sure your code is general enough,
                                      # though admittedly it doesn't make too much sense w.r.t. the
                                      # English description for this query!
                                  ],
                             order_by=('average','desc'))

        self.assertTrue(len(result) >= 14)
        expect = [['Hamilton, Josh', 2010, 'TEX', 0.359],
                  ['Cabrera, Miguel', 2013, 'DET', 0.348],
                  ['Morneau, Justin', 2010, 'MIN', 0.345],
                  ['Cabrera, Miguel', 2011, 'DET', 0.344],
                  ['Altuve, Jose', 2014, 'HOU', 0.341],
                  ['Young, Michael', 2011, 'TEX', 0.338],
                  ['Cabrera, Miguel', 2015, 'DET', 0.338],
                  ['Gonzalez, Adrian', 2011, 'BOS', 0.338],
                  ['Altuve, Jose', 2016, 'HOU', 0.338],
                  ['Martinez, Victor', 2014, 'DET', 0.335],
                  ['Perez, Salvador', 2011, 'KCA', 0.331],
                  ['Martinez, Victor', 2011, 'DET', 0.33],
                  ['Iglesias, Jose', 2013, 'BOS', 0.33],
                  ['Cabrera, Miguel', 2012, 'DET', 0.33]]

        # Note: 15th player has lower average, so top 14 is unambiguous
        #   ['De Aza, Alejandro', 2011, 'CHA', 0.329]

        # Allow any valid sort ordering on field 3 (average). Only check top 14, since there
        # may be other players with 0.329 average swapping in for De Aza.
        result = result[:14]

        for r in expect:
            self.assertIn(r, result)
        for i in range(len(expect)):
            self.assertEqual(expect[i][3], result[i][3])

    # Big Papi's batting average, listed by year
    def test_13(self):
        bbstats = self.database()
        result = quiz.select(bbstats, ['year','average'],
                             filters=[('=',['player'],'Ortiz, David')],
                             order_by=('year','asc'))

        self.assertEqual(result, [[2010, 0.27],
                                  [2011, 0.309],
                                  [2012, 0.318],
                                  [2013, 0.309],
                                  [2014, 0.263],
                                  [2015, 0.273],
                                  [2016, 0.315]])

    # players who've stolen >= 40 bases but were thrown out <= 5 times
    def test_14(self):
        bbstats = self.database()
        result = quiz.select(bbstats, ['player','year','team','SB','CS'],
                             filters=[('>=',['SB'],40),('<=',['CS'],5)],
                             order_by=('SB','desc'))

        self.assertEqual(result, [['Ellsbury, Jacoby', 2013, 'BOS', 52, 4],
                                  ['Trout, Mike', 2012, 'LAA', 49, 5],
                                  ['Cabrera, Everth', 2012, 'SDN', 44, 4]])

##################################################
##  Problem 3 Tests
##################################################

class TestProblem3(unittest.TestCase):
    # First example from write-up
    def test_15(self):
        x = quiz.InfiniteList(lambda x: 0)
        self.assertEqual(x[20], 0)
        self.assertEqual(x[200000], 0)
        self.assertEqual(x[-5000000000000000], 0)
        x[7] = 8
        self.assertEqual(x[7], 8)

    # Second example from write-up
    def test_16(self):
        y = quiz.InfiniteList(abs)
        self.assertEqual(y[-20], 20)
        self.assertEqual(y[20], 20)
        y[20] = 8
        self.assertEqual(y[-20], 20)
        self.assertEqual(y[20], 8)

    # NOTE: this function that we use for tests only checks finitely elements of the infinite list 'obj'!
    # We only look up through the length of regular Python list 'ans'.
    # We don't think it will help you at all to try to write code that doesn't actually work properly
    # but manages to pass our tests because we only look so many positions into a list. ;-)
    def assertMatch(self, obj, ans):
        for a, b in zip(iter(obj), iter(ans)):
            self.assertEqual(a, b)

    # We also sometimes use this one, so that you can pass tests even if your __iter__ isn't working yet.
    def assertMatchWithoutIter(self, obj, ans):
        for i, v in enumerate(ans):
            self.assertEqual(obj[i], v)

    # Iteration
    def test_17(self):
        x = quiz.InfiniteList(lambda x: x)
        x[2] = 3
        x[4] = 10

        self.assertMatch(x, [0, 1, 3, 3, 10, 5, 6, 7, 8, 9])

    # Addition
    def test_18(self):
        x = quiz.InfiniteList(lambda x: x)
        x[2] = 3
        x[4] = 10

        y = quiz.InfiniteList(lambda x: 0)
        y[1] = 7
        y[2] = 30

        self.assertMatchWithoutIter(x + y, [0, 8, 33, 3, 10, 5, 6, 7, 8, 9])

    # Addition plus __iter__
    def test_19(self):
        x = quiz.InfiniteList(lambda x: x)
        x[2] = 3
        x[4] = 10

        y = quiz.InfiniteList(lambda x: 0)
        y[1] = 7
        y[2] = 30

        self.assertMatch(x + y, [0, 8, 33, 3, 10, 5, 6, 7, 8, 9])

    # Multiplication
    def test_20(self):
        x = quiz.InfiniteList(lambda x: x)
        x[2] = 3
        x[4] = 10

        self.assertMatchWithoutIter(x * 2, [0, 2, 6, 6, 20, 10, 12, 14, 16, 18])


##################################################
##  test setup
##################################################

if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
