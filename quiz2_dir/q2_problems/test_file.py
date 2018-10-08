def create_all(numbers):


    def helper(remaining_numbers, out_set=None):
        if out_set is None:
            out_set = set(numbers)

        if remaining_numbers == []:
            return out_set

        working_num = remaining_numbers[0]

        for value in set(out_set):
             out_set.add(value + working_num)
             out_set.add(value - working_num)
             out_set.add(value * working_num)
             out_set.add(value // working_num)

        return helper(remaining_numbers[1:], out_set)

    return helper(numbers)


print(len(create_all([1,2,3,5])))
