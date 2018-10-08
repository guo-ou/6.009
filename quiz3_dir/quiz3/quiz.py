# NO IMPORTS!

##################################################
##  Problem 1
##################################################

def all_simple_paths(graph, start_node, end_node):
    """ Set of all simple paths from start_node to end_node in the graph """
    f_node = graph[start_node]
    starting_path = (start_node, )
    out_set = set()

    def helper(node, cur_path):

        for sub_node in node:

            if sub_node == end_node:
                out_set.add(cur_path + (sub_node,))


            else:
                if sub_node in cur_path:
                    continue
                helper(graph[sub_node], cur_path + (sub_node,))

    helper(f_node, starting_path)

    return out_set


##################################################
##  Problem 2
##################################################

class Item:
    def __init__(self, owner, price):
        self.owner = owner
        self.price = price

    def __repr__(self):
        return "<" + self.__class__.__name__ + ", " + str(self.owner) + ", " + str(self.price) + ">"

    def is_a_kind_of(self, other):
        return isinstance(self, type(other))


class Vehicle(Item): pass
class Sedan(Vehicle): pass
class Truck(Vehicle): pass
class SUV(Vehicle): pass
class F150(Truck): pass
class Ram(Truck): pass


class Market:
    def __init__(self):
        self.for_sale = []
        self.requests = []

    def offer_to_sell(self, item):
        """
        Behavior: the "best" current sell match is found between the given
        item, and any want-to-buy items currently in the market. By "best sell
        match", we mean:

          (1) the for-sale item must (for sure) be a kind of item the buyer is
              willing to buy.

          (2) the want-to-buy item with the highest willing-to-pay price is
              found. If more than one matching want-to-buy item with the same
              highest willing-to-pay price is found, any such match can be
              used.  That highest willing-to-pay price is the price the seller
              will get, even if it is higher than the price the seller was
              willing to sell for.

        If there is a matching want-to-buy item, ownership of the for-sale item
        should be transferred to the buyer (i.e., the owner of the for-sale
        item should be set to the buyer, and the price of the for-sale item
        should be set to the price actually paid by the buyer for the item).
        The sold item should be returned as the result of offer_to_sell, and
        taken off the market.

        If there is no matching want-to-buy item, None should be returned, and
        the want-to-sell item should be remembered for future possible matches
        later, as new want-to-buy items are submitted to the market.
        """
        self.for_sale.append(item)
        # print("FOR SALE: ", self.for_sale)
        # if all(type(item) != type(offer) for offer in self.requests):
        #     return None


        pos_buys = []
        for offer in self.requests:
            if item.is_a_kind_of(offer) and offer.price >= item.price and offer.owner != item.owner:
                pos_buys.append(offer)

        if not pos_buys:
            return None

        else:
            best_offer = max(pos_buys, key=lambda buy: buy.price)
            # print(item.owner)
            item.owner = best_offer.owner
            item.price = best_offer.price
            self.requests.remove(best_offer)
            self.for_sale.remove(item)


            return item




    def offer_to_buy(self, item):
        """
        Behavior: the "best" current purchase match is found between the given
        item, and any items currently listed for sale in the market. By "best
        buy match", we mean:

          (1) the for-sale item must (for sure) be a kind of item the buyer is
              willing to buy.

          (2) the cheapest for-sale matching item is found. If more than one
              matching for-sale item with the same lowest sell price is found,
              any such matching for-sale item can be returned. That lowest
              for-sale price is the price the buyer will pay, even if it is
              lower than the price the buyer was willing to pay.

        If there is a matching for-sale item, ownership of that item should be
        transferred to the buyer (i.e., the owner of the for-sale item should
        be set to the buyer, and the price of the for-sale item should be set
        to the price actually paid by the buyer for the item). The sold item
        should be returned (and taken off the market), and the buyer is
        understood to no longer be seeking to buy another of the item (unless
        they again later register their desire with another offer_to_buy
        submission).

        If there is no matching for-sale item, None should be returned, and the
        offer_to_buy item should be remembered for future possible matches
        later, as new items for sale are submitted to the market.
        """


        self.requests.append(item)
        # print("REQUESTS: ", self.requests)

        pos_buys = []
        for post in self.for_sale:
            if post.is_a_kind_of(item) and item.price >= post.price and item.owner != post.owner:
                pos_buys.append(post)


        if not pos_buys:
            return None
        else:
            best_offer = min(pos_buys, key=lambda buy: buy.price)



            best_offer.owner = item.owner
            # best_offer.price = item.price
            self.requests.remove(item)
            self.for_sale.remove(best_offer)

            return best_offer
##################################################
##  Problem 3
##################################################

allwords = set(open('words2.txt').read().splitlines())

def word_squares(top):
    """ Return (top, right, bottom, left) words """
    letters = "abcdefghijklmnopqrstuvwxyz"
    # print(top)


    #BUG: Too slow for last 3 cases :(

    def word_helper(prefix, rem_chars):
        '''
        returns a generator of all VALID words of length len(prefix) + rem_chars
        '''
        if rem_chars == 0:
            if prefix in allwords: ## Yield only valid words
                yield prefix

        else:
            for let in letters:
                new_word = prefix + let ## Create a new word with each letter appended to the end,
                yield from word_helper(new_word, rem_chars -1) ## use the new word as the working prefix, and decrease length by 1

    def word_helper_backward(prefix, rem_chars):
        '''
        returns a generator of all VALID backward words of length len(prefix) + rem_chars
        '''

        if rem_chars == 0:
            if prefix[::-1] in allwords: ## Yield only valid words
                yield prefix

        else:

            for let in letters:
                new_word = prefix + let ## Create a new word with each letter appended to the end,
                yield from word_helper_backward(new_word, rem_chars -1) ## use the new word as the working prefix, and decrease length by 1


    # print(list(word_helper_backward("t",3)))



    def check_square(square):
        seen = set()
        for i in range(len(square)):
            if square[i] in seen:
                return False
            seen.add(square[i])
            if i == 0:
                if square[i][-1] != square[i+1][0]:
                    return False
            elif i == 1:
                if square[i][-1] != square[i+1][-1]:
                    return False

            elif i == 2:
                if square[i][0] != square[i+1][-1]:
                    return False

            else:
                if square[i][0] != square[0][0]:
                    return False
        return True

    # print(check_square(["is", "so", "to", "it"]))

    # num_words = 4 ## squares have 4 sides
    start_square = [top]
    def recursive_square(active_word, num_words, cur_square):

        if len(cur_square) == 4:

            cur_square[2] = cur_square[2][::-1]
            cur_square[3] = cur_square[3][::-1]

            if check_square(cur_square):

                cur_square = tuple(cur_square)
                yield cur_square


        else:

            if num_words in [4]:

                active_prefix = active_word[-1]
                ## all forward facing words - (2,1) will have to be handled backwards
                for new_word in word_helper(active_prefix, len(active_word) - 1):
                    # if new_word in cur_square:
                    #     continue
                    yield from recursive_square(new_word, num_words - 1, cur_square + [new_word])


            else:

                active_prefix = active_word[-1]
                # print(active_prefix)
                for new_word in word_helper_backward(active_prefix, len(active_word) -1):
                    # if new_word in cur_square:
                    #     continue
                    yield from recursive_square(new_word, num_words - 1, cur_square + [new_word])

    # test_square = ["at", "to", "to", "at"]
    # print(check_square(test_square))
    yield from recursive_square(top, 4, start_square)

# print(list(word_squares("is")))
