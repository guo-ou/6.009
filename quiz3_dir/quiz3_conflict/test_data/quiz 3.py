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
    # create one master list
    master = []
    for row in array:
        for col in row:
            master.append(col)
    # print(master)

    ans = []

    current = master[0]
    counter = 0

    for num in master:
        if num == current:
            counter += 1
            # print('count', counter)
        else:
            # print('tuple', (counter, current))
            ans.append((counter, current))
            current = num
            # print('current', current)
            counter = 1
    ans.append((counter, current))
    return ans

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
    temp =''
    for i in range(len(top),0,-1):
        temp += i
    ans = set(top, temp)
    return ans


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

        # create array of 30 x 30
        a_row = [[]]*30
        for i in range(30):
            self.array.append(a_row)

    def smallest_weight(self, location, timestep):
        r,c = location
        smallest_weight = 100000000000
        smallest_fish = None
        fish_in_interval = []
        print(self.array[r][c])
        print(timestep)
        for fish in self.array[r][c]:
            if fish.arrive_at <= timestep <= fish.arrive_at+fish.duration:
                print('interval', fish)
                fish_in_interval.append(fish)
                # print(fish_in_interval)
        for fish in fish_in_interval:
            if fish.weight < smallest_weight:
                smallest_weight = fish.weight
                smallest_fish = fish
        print('min weight', smallest_weight)
        return smallest_weight

    def fish_with_smallest_weight(self, location, timestep):
        fish_with_smallest_weight = []
        r,c = location
        smallest_weight = self.smallest_weight(location, self.timestep)

        for fish in self.array[r][c]:
            if fish.arrive_at <= timestep <= fish.arrive_at+fish.duration:
                if fish.weight == smallest_weight:
                    fish_with_smallest_weight.append(fish)
        # a list with fish instances that have the min weight
        return fish_with_smallest_weight


    def add_fish(self, location, fish):
        r,c = location
        self.array[r][c].append(fish)

    def catch_fish(self, location, bait):
        r,c = location
        at_location = self.array[r][c]
        if at_location == []:
            return None
        else:
            if len(at_location) == 1:
                # print(at_location)
                # print('YO', at_location[0])
                # if one fish at that location
                if bait in at_location[0].eats:

                    if at_location[0].arrive_at < self.timestep <= at_location[0].arrive_at + at_location[0].duration:
                        ans = at_location[0]
                        self.caught.append(at_location[0])
                        self.array[r][c].remove(at_location[0])

                        self.timestep += 1
                        return ans

            # if multiple fish
            else:
                print()
                print('mult')
                # print(at_location)

                # if multiple fish have same smallest weight
                smallest_weight = self.smallest_weight(location, self.timestep)
                fish_with_smallest = self.fish_with_smallest_weight(location, self.timestep)
                # print('time', self.timestep)
                # print('small weight', smallest_weight)

                print(fish_with_smallest)
                if fish_with_smallest == []:
                    self.timestep+=1
                    return None

                if bait in fish_with_smallest[0].eats:
                    print('bait')
                    # print(fish_with_smallest[0].arrive_at, fish_with_smallest[0].duration)
                    if fish_with_smallest[0].arrive_at < self.timestep <= fish_with_smallest[0].arrive_at + fish_with_smallest[0].duration:
                        ans = fish_with_smallest[0]
                        self.caught.append(fish_with_smallest[0])
                        self.array[r][c].remove(fish_with_smallest[0])
                        self.timestep += 1
                        return ans

        self.timestep += 1
        return None


    def wait(self, n):
        self.timestep += n

    def weight_caught(self):
        weight = 0
        for fish in self.caught:
            weight += fish.weight

        return weight


x = Pond()
a = Catfish(20, 1, 2)
b = Catfish(10, 1, 2)
c = Catfish(7, 1, 2)
d = StripedBass(1, 1, 3)
x.add_fish((12, 23), a)
x.add_fish((12, 23), b)
x.add_fish((12, 23), c)
x.add_fish((12, 23), d)
print((x.weight_caught()))
print('END', (x.catch_fish((12, 23), 'stinky cheese')))
print((x.weight_caught()))
print('END', (x.catch_fish((12, 23), 'stinky cheese')))
print((x.weight_caught()))

print('END', (x.catch_fish((12, 23), 'stinky cheese')))
print((x.weight_caught()))

print('END', (x.catch_fish((12, 23), 'stinky cheese')))
print((x.weight_caught()))

print('END', (x.catch_fish((12, 23), 'stinky cheese')))
print((x.weight_caught()))

print('END', (x.catch_fish((12, 23), 'stinky cheese')))
print((x.weight_caught()))

print('END',(x.catch_fish((12, 23), 'worm')))
print((x.weight_caught()))


print(x.timestep)


