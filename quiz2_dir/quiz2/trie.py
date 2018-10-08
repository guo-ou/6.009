# NO ADDITIONAL IMPORTS!
class Trie:
    def __init__(self, type_=None):
        self.value = None
        self.children = {}
        self.type = type_


    def get_node(self, prefix):
        """
        Helper to return the _Trie instance_ associated with a given prefix, or
        None if the prefix isn't represented in the Trie.
        """
        if not prefix:
            return self
        if prefix[0:1] not in self.children:
            return None
        return self.children[prefix[0:1]].get_node(prefix[1:])


    def __setitem__(self, key, value):
        """
        Add a key with the given value to the trie, or reassign the associated
        value if it is already present in the trie.  Assume that key is an
        immutable ordered sequence.
        """
        if key:
            if self.type is None:
                self.type = type(key)
            else:
                assert type(key) == self.type, ("Given key %r is not the proper type "
                                                "(expected %r, got %r)") % (key, self.type.__name__, type(key).__name__)
            head = key[0:1]
            tail = key[1:]
            if head not in self.children:
                self.children[head] = Trie(self.type)
            self.children[head][tail] = value
        else:
            self.value = value

    def __getitem__(self, key):
        """
        Return the value for the specified prefix, or raise a KeyError if not
        in trie.
        """
        relevant_node = self.get_node(key)
        if relevant_node is None or relevant_node.value is None:
            raise KeyError() from None
        return relevant_node.value

    def __delitem__(self, key):
        """
        Delete the given key from the trie if it exists.
        """
        relevant_node = self.get_node(key)
        if relevant_node is not None:
            relevant_node.value = None

    def __contains__(self, key):
        """
        Is key a key in trie? return True or False.
        """
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __iter__(self):
        """
        Generator of (key, value) pairs for all keys/values in this trie and
        its children.  Must be a generator!
        """
        if self.value is not None:
            yield self.type(), self.value

        for ch, child in self.children.items():
            yield from ((ch + key, val) for key, val in child)

    def __len__(self):
        """
        Another useful function, returns the length of the Trie (the number of
        keys with values set).
        """
        for ix, _ in enumerate(self):
            pass
        return ix + 1


class RadixTrie(Trie):
    pass
