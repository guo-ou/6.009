# NO ADDITIONAL IMPORTS!
from text_tokenize import tokenize_sentences
import pickle
import os
TEST_DIRECTORY = os.path.dirname(__file__)

class Trie:
    def __init__(self):
        self.value = None
        self.children = dict()
        self.type = None


    def __setitem__(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.
        """

        if self.type is None:
            if type(key) == str:
                self.type = ""
            if type(key) == tuple:

                self.type = tuple()

        if (type(key) == str and self.type != "") or (type(key) == tuple and self.type != ()):
            raise TypeError

        if len(key) == 0:
            self.value = value
            return

        elif key[:1] not in self.children:
            self.children[key[:1]] = Trie()

        self.children[key[:1]].__setitem__(key[1:], value)

    def __getitem__(self, key):
        """
        Return the value for the specified prefix.  If the given key is not in
        the trie, raise a KeyError.
        """

        #TypeError issues
        if (type(key) == str and self.type != "") or (type(key) == tuple and self.type != ()):
            raise TypeError

        #KeyError for bad keys
        try:
            working_trie = self.children[key[:1]]
        except:
            raise KeyError


        #Functional
        if working_trie.value is None:
            return working_trie.__getitem__(key[1:])
        else:
            return working_trie.value

    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists.
        """
        self[key] = None

    def __contains__(self, key):
        """
        Is key a key in the trie? return True or False.
        """

        #KeyError for bad keys
        try:
            working_trie = self.children[key[:1]]
        except:
            return False

        #Functional
        if working_trie.value is not None:
            return True

        elif key[1:2] in working_trie.children:
            return key[1:] in working_trie

        else:
            return False



    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator!
        """
        def gen(working_path=None, working_trie=None):
            if working_path is None:
                working_path = self.type


            for node, trie in working_trie.children.items():
                child = working_path + node

                if trie.value is not None:
                    yield child, trie.value


                yield from gen(child, trie)

        yield from gen(working_trie=self)


def make_word_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    words in the text, and whose values are the number of times the associated
    word appears in the text
    """
    word_list = tokenize_sentences(text)
    # print(word_list)
    out_trie = Trie()
    for sentence in word_list:
        for word in sentence.split():
            #print(word, len(word))
            if word in out_trie:
                # print("hello")
                out_trie[word] += 1
            else:
                out_trie[word] = 1

    return out_trie


def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    """
    raise NotImplementedError


def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring words that start with
    prefix.  Include only the top max_count elements if max_count is specified,
    otherwise return all.
    """
    raise NotImplementedError


def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.
    """
    raise NotImplementedError


def word_filter(trie, pattern):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """
    raise NotImplementedError


# you can include test cases of your own in the block below.
if __name__ == '__main__':

    def read_expected(fname):
        with open(os.path.join(TEST_DIRECTORY, 'testing_data', fname), 'rb') as f:
            return pickle.load(f)

    test = read_expected("1.pickle")

    # print(test)


    test_trie = Trie()
    test_trie["cat"]=True
    # print(test_trie.children)
