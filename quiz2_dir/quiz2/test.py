#!/usr/bin/env python3
import os
import quiz
import types
import random
import unittest

TEST_DIRECTORY = os.path.dirname(__file__)

class Quiz2TestCase(unittest.TestCase):
    def _run_test(self, n):
        in_fname = os.path.join(TEST_DIRECTORY, 'test_data',
                                '%s_%d_in.pyobj' % (self.test_name, n))
        with open(in_fname, encoding='utf-8') as f:
            inp = eval(f.read())
        out_fname = os.path.join(TEST_DIRECTORY, 'test_data',
                                 '%s_%d_out.pyobj' % (self.test_name, n))
        with open(out_fname, encoding='utf-8') as f:
            expected = eval(f.read())

        result = self.get_result(inp)
        self.assertEqual(result, expected)


##################################################
### Problem 1: efficiency
##################################################

class TestProblem1(Quiz2TestCase):
    test_name = 'efficiency'

    def get_result(self, inp):
        return quiz.unique(inp)

    def test_01(self):
        self._run_test(1)

    def test_02(self):
        self._run_test(2)

    def test_03(self):
        self._run_test(3)

    def test_04(self):
        self._run_test(4)


##################################################
### Problem 2: phone words
##################################################

class TestProblem2(Quiz2TestCase):
    test_name = 'phone'

    def get_result(self, inp):
        return quiz.phone_words(inp)

    def test_01(self):
        self._run_test(1)

    def test_02(self):
        self._run_test(2)

    def test_03(self):
        self._run_test(3)

    def test_04(self):
        self._run_test(4)

    def test_05(self):
        self._run_test(5)

    def test_06(self):
        self._run_test(6)

    def test_07(self):
        self._run_test(7)

    def test_08(self):
        self._run_test(8)


##################################################
### Problem 3: radix trie
##################################################

from trie import Trie, RadixTrie
from text_tokenize import tokenize_sentences


def dictify(t):
    out = {'value': t.value, 'children': {}}
    for ch, child in t.children.items():
        out['children'][ch] = dictify(child)
    return out


def make_word_trie(words):
    t = Trie()
    for word, val in words:
        t[word] = val
    return t


def get_words(text):
    return [tuple(i.split()) for i in tokenize_sentences(text, True)]


def is_radix_trie(t):
    if not isinstance(t, RadixTrie):
        return False

    return all(is_radix_trie(i) for i in t.children.values())


class TestProblem3(Quiz2TestCase):
    test_name = 'trie'

    def get_result(self, inp):
        inp = make_word_trie(inp)
        original = dictify(inp)
        out = quiz.compress_trie(inp)
        self.assertEqual(original, dictify(inp), "Your function should not modify the given Trie.")
        self.assertTrue(is_radix_trie(out), "Your function should return an instance of RadixTrie.")
        return dictify(out)

    def test_01(self):
        self._run_test(1)

    def test_02(self):
        self._run_test(2)

    def test_03(self):
        self._run_test(3)

    def test_04(self):
        self._run_test(4)

    def test_05(self):
        self._run_test(5)

    def test_06(self):
        self._run_test(6)

    def test_07(self):
        self._run_test(7)

    def test_08(self):
        self._run_test(8)


if __name__ == '__main__':
    res = unittest.main(verbosity=3, exit=False)
