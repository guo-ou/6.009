#!/usr/bin/env python3
import os
import quiz
import unittest

TEST_DIRECTORY = os.path.dirname(__file__)

##################################################
### Problem 1: runs
##################################################

def verify_run_result(L):
    # top level is a list
    if not isinstance(L,list):
        return False
    # each element should be a number or list of numbers
    for e in L:
        if isinstance(e,int):
            continue
        elif isinstance(e,list):
            for ee in e:
                if not isinstance(ee,int):
                    return False
        else:
            return False
    return True

class TestProblem1(unittest.TestCase):
    def test_runs_1(self):
        arg = []
        result = quiz.runs(arg)
        expected = []
        self.assertTrue(verify_run_result(result),msg="result has the wrong composition")
        self.assertEqual(result, expected)

    def test_runs_2(self):
        arg = [1, 3, 5]
        result = quiz.runs(arg)
        expected = [1, 3, 5]
        self.assertTrue(verify_run_result(result),msg="result has the wrong composition")
        self.assertEqual(result, expected)

    def test_runs_3(self):
        arg = [1, 2, 4]
        result = quiz.runs(arg)
        expected = [[1, 2], 4]
        self.assertTrue(verify_run_result(result),msg="result has the wrong composition")
        self.assertEqual(result, expected)

    def test_runs_4(self):
        arg = [1, 2, 4, 2, 2, 3, 4, 4, 5, 9, 10]
        result = quiz.runs(arg)
        expected = [[1, 2], 4, 2, [2, 3, 4], [4, 5], [9, 10]]
        self.assertTrue(verify_run_result(result),msg="result has the wrong composition")
        self.assertEqual(result, expected)

    def test_runs_5(self):
        # one long run
        arg = list(range(1,11))
        result = quiz.runs(arg)
        expected = [arg[:]]
        self.assertTrue(verify_run_result(result),msg="result has the wrong composition")
        self.assertEqual(result, expected)

    def test_runs_6(self):
        # no runs at all
        arg = list(range(1,11))
        arg.reverse()
        expected = arg[:]
        result = quiz.runs(arg)
        self.assertTrue(verify_run_result(result),msg="result has the wrong composition")
        self.assertEqual(result, expected)

##################################################
### Problem 2: is_cousin
##################################################


class TestProblem2(unittest.TestCase):
    parent_db = [(452, 483), (566, 483), (120, 742), (566, 742), (682, 8), (566, 8), (120, 873), (997, 873), (682, 169), (452, 840), (120, 627), (682, 723), (452, 755), (120, 697), (566, 697), (840, 519), (840, 776), (697, 776), (873, 137), (755, 137), (723, 137), (169, 652), (755, 652), (755, 398), (742, 405), (697, 281), (627, 281), (483, 281), (840, 931), (873, 931), (840, 165), (873, 165), (742, 165), (8, 40), (873, 40), (723, 939), (742, 939), (755, 563), (723, 563), (169, 54), (169, 569), (755, 569), (742, 569), (873, 65), (755, 65), (169, 839), (697, 839), (755, 839), (697, 843), (742, 843), (840, 78), (697, 78), (169, 339), (873, 342), (483, 92), (169, 738), (723, 738), (742, 738), (8, 482), (483, 103), (755, 491), (169, 878), (627, 878), (755, 878), (873, 754), (697, 754), (697, 883), (169, 883), (840, 244), (723, 244), (840, 377), (339, 135), (652, 135), (839, 135), (883, 778), (281, 778), (939, 778), (519, 524), (482, 909), (652, 909), (165, 909), (563, 142), (939, 910), (776, 656), (754, 656), (878, 269), (883, 659), (776, 532), (754, 532), (931, 532), (377, 918), (92, 918), (137, 407), (738, 407), (342, 407), (652, 791), (281, 23), (754, 23), (342, 23), (137, 26), (652, 26), (54, 26), (754, 797), (652, 797), (342, 292), (281, 420), (482, 39), (839, 686), (103, 48), (377, 564), (569, 949), (78, 949), (519, 949), (754, 950), (652, 950), (165, 950), (931, 951), (92, 315), (569, 188), (563, 188), (776, 447), (776, 833), (65, 833), (342, 833), (482, 709), (281, 969), (165, 969), (244, 77), (103, 77), (754, 463), (244, 463), (482, 212), (738, 212), (405, 212), (491, 84), (878, 475), (883, 220), (405, 220), (843, 608), (165, 608), (342, 610), (738, 743), (405, 743), (839, 232), (569, 616), (339, 616), (244, 616), (40, 365), (377, 365), (92, 365), (754, 622), (54, 622), (78, 370), (165, 370), (398, 370), (65, 626), (103, 626), (519, 626), (939, 758), (776, 502), (165, 502), (78, 502), (931, 891), (563, 380), (342, 380)]

    def test_is_cousin_1(self):
        result = quiz.is_cousin(TestProblem2.parent_db, 92, 969)
        self.assertIsNone(result)

    def test_is_cousin_2(self):
        result = quiz.is_cousin(TestProblem2.parent_db, 135, 778)
        self.assertTrue(result in {697, 169})

    def test_is_cousin_3(self):
        result = quiz.is_cousin(TestProblem2.parent_db, 84, 48)
        self.assertIsNone(result)

    def test_is_cousin_4(self):
        result = quiz.is_cousin(TestProblem2.parent_db, 656, 380)
        self.assertEqual(result, 873)

    def test_is_cousin_5(self):
        result = quiz.is_cousin(TestProblem2.parent_db, 891, 656)
        self.assertTrue(result in {840, 873})

    def test_is_cousin_6(self):
        result = quiz.is_cousin(TestProblem2.parent_db, 950, 797)
        self.assertIsNone(result)

    def test_is_cousin_7(self):
        result = quiz.is_cousin(TestProblem2.parent_db, 949, 950)
        self.assertTrue(result in {742, 840, 169, 755, 697})
        
##################################################
### Problem 3: all_phrases
##################################################

class TestProblem3(unittest.TestCase):
    grammar1 = {
        "sentence": [["noun", "verb"], ["noun", "never", "verb"]],
        "noun":     [["pigs"], ["professors"]],
        "verb":     [["fly"], ["think"]]
    }

    grammar2 = {
        "start": [["n"], ["adj", "n"], ["adj", "adj", "n"]],
        "adj":   [["quirky"], ["hungry"], ["n"]],
        "n":     [["Adam"], ["Duane"]]
    }

    grammar3 = {
        "greeting": [["hi", "there"], ["hi", "name"]],
        "name":     [["Rosenkrantz"], ["Guildenstern"]]
    }

    grammar4 = {
        "foo": [["End", "of", "quiz", "1"]]
    }
        
    def verify_all_phrases(self, L):
        # top level is a list
        self.assertIsInstance(L, list, "result should be a list")
        # each phrase is a list of strings
        for phrase in L:
            self.assertIsInstance(phrase, list, "phrase should be a list")
            for terminal in phrase:
                self.assertIsInstance(terminal, str, "terminals should be a string")

    def test_all_phrases_1(self):
        result = quiz.all_phrases(TestProblem3.grammar1, 'pigs')
        self.verify_all_phrases(result)
        expected = [['pigs']]
        # we don't care about order of phrases
        self.assertEqual(sorted(result),sorted(expected))

    def test_all_phrases_2(self):
        result = quiz.all_phrases(TestProblem3.grammar1, 'noun',)
        self.verify_all_phrases(result)
        expected = [['pigs'], ['professors']]
        # we don't care about order of phrases
        self.assertEqual(sorted(result),sorted(expected))

    def test_all_phrases_3(self):
        result = quiz.all_phrases(TestProblem3.grammar1, 'sentence')
        self.verify_all_phrases(result)
        expected = [['pigs', 'fly'], ['pigs', 'think'],
                    ['professors', 'fly'], ['professors', 'think'],
                    ['pigs', 'never', 'fly'], ['pigs', 'never', 'think'],
                    ['professors', 'never', 'fly'], ['professors', 'never', 'think']]
        # we don't care about order of phrases
        self.assertEqual(sorted(result),sorted(expected))

    def test_all_phrases_4(self):
        result = quiz.all_phrases(TestProblem3.grammar2, 'adj')
        self.verify_all_phrases(result)
        expected = [['hungry'], ['quirky'], ['Adam'], ['Duane']]
        # we don't care about order of phrases
        self.assertEqual(sorted(result),sorted(expected))
        
    def test_all_phrases_5(self):
        result = quiz.all_phrases(TestProblem3.grammar2, 'start')
        self.verify_all_phrases(result)
        expected = [['Adam'], ['Duane'],
                    ['hungry', 'Adam'], ['hungry', 'Duane'], ['quirky', 'Adam'], ['quirky', 'Duane'],
                    ['Adam', 'Adam'], ['Adam', 'Duane'], ['Duane', 'Adam'], ['Duane', 'Duane'],
                    ['hungry', 'hungry', 'Adam'], ['hungry', 'hungry', 'Duane'],
                    ['hungry', 'quirky', 'Adam'], ['hungry', 'quirky', 'Duane'],
                    ['hungry', 'Adam', 'Adam'], ['hungry', 'Adam', 'Duane'],
                    ['hungry', 'Duane', 'Adam'], ['hungry', 'Duane', 'Duane'],
                    ['quirky', 'hungry', 'Adam'], ['quirky', 'hungry', 'Duane'],
                    ['quirky', 'quirky', 'Adam'], ['quirky', 'quirky', 'Duane'],
                    ['quirky', 'Adam', 'Adam'], ['quirky', 'Adam', 'Duane'],
                    ['quirky', 'Duane', 'Adam'], ['quirky', 'Duane', 'Duane'],
                    ['Adam', 'hungry', 'Adam'], ['Adam', 'hungry', 'Duane'],
                    ['Adam', 'quirky', 'Adam'], ['Adam', 'quirky', 'Duane'],
                    ['Adam', 'Adam', 'Adam'], ['Adam', 'Adam', 'Duane'],
                    ['Adam', 'Duane', 'Adam'], ['Adam', 'Duane', 'Duane'],
                    ['Duane', 'hungry', 'Adam'], ['Duane', 'hungry', 'Duane'],
                    ['Duane', 'quirky', 'Adam'], ['Duane', 'quirky', 'Duane'],
                    ['Duane', 'Adam', 'Adam'], ['Duane', 'Adam', 'Duane'],
                    ['Duane', 'Duane', 'Adam'], ['Duane', 'Duane', 'Duane']]
        # we don't care about order of phrases
        self.assertEqual(sorted(result),sorted(expected))

    def test_all_phrases_6(self):
        result = quiz.all_phrases(TestProblem3.grammar3, 'greeting')
        self.verify_all_phrases(result)
        expected = [["hi", "there"], ["hi", "Rosenkrantz"], ["hi", "Guildenstern"]]
        # we don't care about order of phrases
        self.assertEqual(sorted(result),sorted(expected))

    def test_all_phrases_7(self):
        result = quiz.all_phrases(TestProblem3.grammar4, 'foo')
        self.verify_all_phrases(result)
        expected = [["End", "of", "quiz", "1"]]
        # we don't care about order of phrases
        self.assertEqual(sorted(result),sorted(expected))
        
if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
