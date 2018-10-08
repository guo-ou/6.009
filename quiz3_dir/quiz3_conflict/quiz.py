#############
# Problem 1 #
#############


def run_length_encode_2d(array):
    """
    input:
        array: a 2-d array (list of lists) containing the elements to be
        run-length encoded.

    returns:
        a list of (count, element) tuples
    """

    big_out = []
    past_ele = array[0][0]
    count = 1
    for r in range(len(array)):
        for c in range(len(array[0])):

            if r == 0 and c == 0:
                continue

            working_ele = array[r][c]
            # print(working_ele)
            if working_ele == past_ele:

                count += 1
            else:
                big_out.append((count, past_ele))
                count = 1

            past_ele = working_ele
    big_out.append((count, past_ele))

    return big_out

array = [[0, 0, 0],
 [2, 2, 1],
 [1, 1, 1]]

# print(run_length_encode_2d(array))


#############
# Problem 2 #
#############

allwords = set(open('words2.txt').read().splitlines())


def word_squares(top):
    """
    input:
       top: a string representing the top word in the word square

    produces a generator that generates all word squares that have the given
    word as the top word.  each word square should be represented as a tuple of
    strings.
    """

    if top in allwords:
        letters  = "abcdefghijklmnopqrstuvwxyz"
        square = (top, )
        def helper(length, prefix):

            if length == 0:
                if prefix in allwords:
                    yield prefix

            else:
                for letter in letters:
                    new_start = prefix + letter
                    yield from helper(length-1, new_start)

        def recur_helper(index, word_len, square):
            if len(square) == word_len:
                yield square
            else:
                new_start = ''
                for word in square:
                    new_start += word[index]
                for new_word in helper(word_len - len(square), new_start):
                    yield from recur_helper(index + 1, word_len, square + (new_word,))

        yield from recur_helper(1, len(top), square)

#############
# Problem 3 #
#############


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


class Pond:
    def __init__(self):
        self.timestep = 0
        self.array = []
        self.caught = []

        self.fishes = dict()

    # def smallest_weight(self, location, timestep):
    #
    # def fish_with_smallest_weight(self, location, timestep):
    #     pass


    def add_fish(self, location, fish):
        self.fishes[fish] = location


    def catch_fish(self, location, bait):



        pos_fishes = []
        # print("TIME: ",self.timestep)

        for fish in self.fishes:
            if self.fishes[fish] == location:
                if bait in fish.eats and fish.arrive_at <= self.timestep < fish.arrive_at + fish.duration and fish not in self.caught:
                    pos_fishes.append(fish)

        # if len(pos_fishes) == 1:
        #     print(fishes)
        #     print(pos_fishes, bait, location)


        self.wait(1)
        weight_fish = []
        pos_fishes = sorted(pos_fishes, key=lambda f: f.weight)

        for f in pos_fishes:
            if weight_fish == [] or f.weight == weight_fish[-1].weight:
                weight_fish.append(f)

        #

        if pos_fishes == []:
            return None
        else:
            self.caught.append(min(weight_fish, key=lambda f: f.arrive_at))

            return min(weight_fish, key=lambda f: f.arrive_at)



    def wait(self, n):
        self.timestep += n

    def weight_caught(self):
        total = 0
        for fish in self.caught:
            total += fish.weight


        return total

# x = Pond()
# x.add_fish((0,0), SmallmouthBass(7, 3, 10)) # 7 pounds, location (0,0), can be caught on timesteps 3 through 12 (inclusive)
# print(x.catch_fish((0,0), 'insect'))  # timestep 0.  Returns None (fish has not yet arrived).
# x.add_fish((0,1), BubbleBass(10, 0, 5)) # 10 pounds, location (0,0), can be caught on timesteps 0 through 4 (inclusive)
# print(x.catch_fish((0,1), 'insect'))  # timestep 1.  Returns None (wrong bait).
# x.wait(3)
# print(x.catch_fish((0,1), 'krabby patty')  )# timestep 4.  Returns the fish (correct bait, fish is still around).
# print(x.weight_caught()) # 10, for the one fish we've caught.
# print(x.catch_fish((0,0), 'insect'))
# print(x.weight_caught())

#
# x = Pond()
# # print(x.array)
# #
# a = Catfish(20, 1, 2)
# b = Catfish(10, 1, 2)
# c = Catfish(7, 1, 2)
# d = StripedBass(1, 1, 3)
# x.add_fish((12, 23), a)
# x.add_fish((12, 23), b)
# x.add_fish((12, 23), c)
# x.add_fish((12, 23), d)
# # print((x.weight_caught()))
# print('END', (x.catch_fish((12, 23), 'stinky cheese')))
# # print((x.weight_caught()))
# # print('END', (x.catch_fish((12, 23), 'stinky cheese')))
# # print((x.weight_caught()))
# #
# # print('END', (x.catch_fish((12, 23), 'stinky cheese')))
# # print((x.weight_caught()))
# #
# # print('END', (x.catch_fish((12, 23), 'stinky cheese')))
# # print((x.weight_caught()))
# #
# # print('END', (x.catch_fish((12, 23), 'stinky cheese')))
# # print((x.weight_caught()))
# #
# # print('END', (x.catch_fish((12, 23), 'stinky cheese')))
# # print((x.weight_caught()))
# #
# # print('END',(x.catch_fish((12, 23), 'worm')))
# # print((x.weight_caught()))
# #
# #
# # print(x.timestep)
