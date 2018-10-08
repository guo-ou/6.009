# NO ADDITIONAL IMPORTS!
from text_tokenize import tokenize_sentences

#Letter sets: comprehensive of most commonly used characters
letters = "abcdefghijklmnopqrstuvwxyz"
alpha_numeric_letters = letters + "0123456789!@#$%^&*()_-/{}[]:;<>,."

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
        if len(key) == 1:
            return self.children[key].value

        #TypeError issues
        if (type(key) == str and self.type != "") or (type(key) == tuple and self.type != ()):
            raise TypeError

        #KeyError for bad keys
        try:
            working_trie = self.children[key[:1]]
        except:
            raise KeyError


        #Functional
        if working_trie.value is None or len(key) != 1:
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
        #False for bad keys
        try:
            working_trie = self.children[key[:1]]
        except:
            return False

        #Functional
        if working_trie.value is not None and len(key) == 1:
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
    text_list = tokenize_sentences(text)
    out_trie = Trie()
    for sentence in text_list:
        for word in sentence.split():
            if word in out_trie:
                out_trie[word] = out_trie[word] + 1
            else:
                out_trie[word] = 1

    return out_trie

def make_phrase_trie(text):
    """
    Given a piece of text as a single string, create a Trie whose keys are the
    sentences in the text (as tuples of individual words) and whose values are
    the number of times the associated sentence appears in the text.
    """
    text_list = tokenize_sentences(text)
    out_trie = Trie()
    for sentence in text_list:
        sentence = tuple(sentence.split())
        if sentence not in out_trie:
            out_trie[sentence] = 1
        else:
            out_trie[sentence] += 1

    return out_trie

def autocomplete(trie, prefix, max_count=None):
    """
    Return the list of the most-frequently occurring words that start with
    prefix.  Include only the top max_count elements if max_count is specified,
    otherwise return all.
    """


    cur_node = recurse_down(trie, prefix)
    if cur_node is None:
        return []

    assoc_words = list(cur_node) #__iter__() call into a list

    if cur_node.value is not None:
        assoc_words.append((prefix, cur_node.value))

    assoc_words = sorted(assoc_words, key=lambda x: x[1])[::-1] #sort
    out_list = []

    for ele in assoc_words[:max_count]:
        if ele[0] != prefix:
            out_list.append(prefix + ele[0])
        else:
            out_list.append(ele[0])

    return out_list

def autocorrect(trie, prefix, max_count=None):
    """
    Return the list of the most-frequent words that start with prefix or that
    are valid words that differ from prefix by a small edit.
    """

    def deletions(prefix):
        '''
        returns all the deletions of a given prefix
        '''
        out_list = []
        for i in range(len(prefix)):
            prefix_copy = prefix[:]
            out_word = prefix_copy[:i] + prefix_copy[(i + 1):]
            if out_word in trie and out_word != prefix:
                out_list.append(out_word)

        return out_list

    def additions(prefix):
        '''
        returns all the additions of a given prefix
        '''
        out_list = []
        for i in range(len(prefix)):
            for letter in letters:
                prefix_copy = prefix[:]
                out_word = prefix_copy[:i] + letter + prefix_copy[(i):]
                if out_word in trie and out_word != prefix:
                    out_list.append(out_word)

        return out_list

    def replacements(prefix):
        '''
        returns all the replacements of a given prefix
        '''
        out_list = []
        for i in range(len(prefix)):


            for letter in letters:
                prefix_copy = prefix[:]
                out_word = prefix_copy[:i] + letter + prefix_copy[(i+1):]

                if out_word in trie and out_word != prefix:
                    out_list.append(out_word)

        return out_list

    def transposes(prefix):
        '''
        returns all the possible transposes of a given prefix
        '''
        out_list = []
        for i in range(len(prefix)):
            if 0 < i < len(prefix):
                prefix_copy = prefix[:]
                out_word = prefix_copy[:i-1]  + prefix_copy[i]+ prefix_copy[i-1]+ prefix_copy[(i + 1):]
                if out_word in trie and out_word != prefix:
                    out_list.append(out_word)

        return out_list

    #Set of all autocorrections
    corrections_set = set(deletions(prefix)) | set(additions(prefix)) | set(replacements(prefix)) | set(transposes(prefix))
    #Autocompleted endings
    uncorrected_endings = autocomplete(trie, prefix, max_count)

    value_dict = [] #tuple pairs
    for ending in corrections_set:
        value_dict.append((ending, trie[ending]))

    value_dict = sorted(value_dict, key=lambda x: x[1])[::-1] #sort
    new_endings = []
    for i in range(len(value_dict)):
        new_endings += [value_dict[i][0]]

    if max_count is not None: #clip endings
        return (uncorrected_endings + new_endings)[:max_count]
    else:
        return (uncorrected_endings + new_endings)

def word_filter(trie, pattern):
    """
    Return list of (word, freq) for all words in trie that match pattern.
    pattern is a string, interpreted as explained below:
         * matches any sequence of zero or more characters,
         ? matches any single character,
         otherwise char in pattern char must equal char in word.
    """

    def helper(pattern, possibilities=None):
        if possibilities is None:
            possibilities = set()


        if len(pattern) == 0:
            #BASE CASE
            output = []
            for word in possibilities:
                if word not in trie:
                    #Drop words that made it past other checks but arent in Trie
                    continue
                cur_node = recurse_down(trie, word)
                output.append((word, cur_node.value))
            return output

        else:
            #Recursive Case
            if pattern[0] == "*":
                #* possibilities
                if len(possibilities) == 0:
                    for word in all_nodes(trie):
                        possibilities.add(word[0])
                    possibilities.add("") #Make sure to include empty string

                else:
                    out_pos = set()
                    for node in possibilities:
                        cur_node = recurse_down(trie, node)
                        for word in all_nodes(cur_node):
                            out_pos.add(node + word[0])
                        out_pos.add(node)

                    possibilities = out_pos

            elif pattern[0] == "?":
                #? possibilities
                if len(possibilities) == 0:
                    for letter in alpha_numeric_letters:
                        if letter not in trie.children:
                            continue
                        possibilities.add(letter)

                else:
                    out_pos = set()
                    for word in possibilities:
                        cur_node = recurse_down(trie, word)
                        for letter in alpha_numeric_letters:
                            if letter not in cur_node.children:
                                continue
                            out_pos.add(word + letter)
                    possibilities = out_pos

            else:
                # AlphaNumeric possibilities
                if len(possibilities) == 0:
                    possibilities.add(pattern[0])

                else:
                    out_pos = set()
                    for word in possibilities:
                        cur_node = recurse_down(trie, word)
                        if pattern[0] not in cur_node.children:
                            continue
                        out_pos.add(word + pattern[0])

                    possibilities = out_pos

        return helper(pattern[1:], possibilities)

    return helper(pattern)

### HELPER FUNCTIONS ###
def all_nodes(trie):
    '''
    Takes a given trie and returns a generator object (similarly to __iter__())
    that contains ALL nodes and all associated values, even if the value is None.
    This is very helpful for evaluating patterns with *.
    '''
    def gen(working_path=None, working_trie=None):
        if working_path is None:
            working_path = trie.type

        for node, sub_trie in working_trie.children.items():
            child = working_path + node
            yield child, sub_trie.value

            yield from gen(child, sub_trie)

    yield from gen(working_trie=trie)

def recurse_down(trie, prefix):
    '''
    Takes a given string (prefix) and recursively searches down the trie until
    reaching the node whose parents construct that string. Helpful for evaluating
    which letters can possibly follow a given node -- optimizes the generation
    of words from the trie.
    '''
    def helper(prefix, working_trie=None):
        if len(prefix) == 0:
            return trie
        if working_trie is None:
            working_trie = trie.children[prefix[:1]]
            if len(prefix) == 1:
                return working_trie
            prefix = prefix[1:]

        if len(prefix) == 1:
            try:
                return working_trie.children[prefix]
            except:
                return None
        else:
            return helper(prefix[1:], working_trie.children[prefix[:1]])

    return helper(prefix)


# you can include test cases of your own in the block below.
if __name__ == '__main__':
    pass
