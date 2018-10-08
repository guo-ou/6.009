# NO IMPORTS ALLOWED!

##################################################
### Problem 1: efficiency
##################################################

def find_vals(input_list):
	# doubled = [item*2 for item in input_list]
	# output = []
	# for item in input_list:
	#     if item in set(doubled):
	#         output = output + [item]
	# return outputn out_dict.keys():
	storage = set(input_list)
	out_set = [x for x in input_list if x/2 in storage]
	return out_set
	#
	# out_set = set(x/2 for x in set(input_list))
	# return list(out_set.union(set(input_list)))


##################################################
### Problem 2: operation combinations
##################################################

# REMINDER: YOU ARE NOT ALLOWED TO USE PYTHON'S BUILT-IN eval FUNCTION!

def combinations(numbers):
	if numbers == []:
		return set()

	if len(numbers) == 1:
		return set(numbers)


	out_set = set()
	def helper(remaining_numbers, total):
		if len(remaining_numbers) == 0:
			out_set.add(total)
		else:
			new_total = total + remaining_numbers[0]
			helper(remaining_numbers[1:], new_total)
			new_total = total - remaining_numbers[0]
			helper(remaining_numbers[1:], new_total)
			new_total = total * remaining_numbers[0]
			helper(remaining_numbers[1:], new_total)
			new_total = total // remaining_numbers[0]
			helper(remaining_numbers[1:], new_total)

	helper(numbers[1:],  numbers[0])
	return out_set

##################################################
### Problem 3: radix trie insertion
##################################################

from trie import Trie  # our solution for lab 6 has been included in trie.py


def dictify(t):
	"""
	For debugging purposes.  Given a trie (or radix trie), return a dictionary
	representation of that structure, including the value and children
	associated with each node.
	"""
	out = {'value': t.value, 'children': {}}
	for ch, child in t.children.items():
		out['children'][ch] = dictify(child)
	return out

def find_prefix_index(word1, word2):
	for i in range(min(len(word1), len(word2))):
		if word1[i] != word2[i]:
			return i
	return min(len(word1), len(word2))



class RadixTrie(Trie):



	def __setitem__(self, key, val):
		if len(key) == 0:
			self.value = val
			return


		prefix, prefix_index = self.prefix_finder(key)
		if prefix is not None:
			if prefix_index == len(prefix):
				return self.children[prefix].__setitem__(key[len(prefix):], val)
			else:
				new_radix = RadixTrie()
				new_radix.children[prefix[prefix_index:]] = self.children.pop(prefix)
				return self.children[prefix[0:prefix_index]].__setitem__(new_radix, val)

		else:
			self.children[key] = RadixTrie()
			self.children[key].__setitem__("",val)
			return

	def prefix_finder(self, word):
		for subkey in self.children:
			prefix_i = find_prefix_index(subkey, word)
			if prefix_i > 0:
				return (subkey, prefix_i)

		return (None, None)
	# else:
		# 	self.children[key] = RadixTrie()
		# 	self.children[key].value = val
