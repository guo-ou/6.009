import sys
sys.setrecursionlimit(1000)

# NO OTHER IMPORTS!

############################################################
## Problem 1
############################################################

# Constant folding

def constant_fold(expr):
    """Simplify parts of the expression whose constant values we can predict in advance,
    according to the rules set out in the quiz document.

    >>> constant_fold(1)
    1
    >>> constant_fold('x')
    'x'
    >>> constant_fold(('+', 2, 3))
    5
    >>> constant_fold(('+', 'x', ('*', 8, 3)))
    ('+', 'x', 24)
    >>> constant_fold(('*', 'x', ('-', 8, 7)))
    'x'
    """
    if isinstance(expr, tuple):
        working_token = expr[0]
    else:
        working_token = expr
    if working_token in ["*","/","+","-"]:
        ## Begin expression
        left = constant_fold(expr[1])
        right = constant_fold(expr[2])

        if isinstance(left, int) and isinstance(right, int):
            if working_token == "*":
                return left * right
            elif working_token == "/":
                return left / right
            elif working_token == "+":
                return left + right
            elif working_token == "-":
                return left - right

        if isinstance(left, str) and right == 0:
            if working_token == "*":
                return 0
            elif working_token == "+" or working_token == "-":
                return left

        if isinstance(right, str) and left == 0:
            if working_token == "*" or working_token == "/":
                return 0
            elif working_token == "+" or working_token == "-":
                return right

        if isinstance(left, str) and right == 1:
            if working_token == "*" or working_token == "/":
                return left

        if isinstance(right, str) and left == 1:
            if working_token == "*":
                return right

        return (working_token, left, right)


    elif isinstance(working_token, int):
        return working_token

    elif isinstance(working_token, str):
        return working_token


############################################################
## Problem 2
############################################################

# Databases

def select(table,which,filters=None,order_by=None):
    """select matching rows from the table
    result is a list containing the field values specifed by select in the order
    specified by order_by (or in table order if no order_by is specified).
    No row of table headers should be included.

    table is a list of rows, each row is a list of field values
      table[0] is a row of field names (strings)
      table[1:] are rows of data (can be any type)
      table has at least one row (ie, the field names)

    which is a sequence of field names specifing which data should
      be included in each returned row.  Must contain at least one field.

    filters, if specified, is a sequence of clauses of the form (pred, field_or_const, field_or_const)
      field has the form ['field_name'], const is a number or string
      pred is one of "=","!=","<","<=",">",">="
      if specified, row matches if all predicates evaluate to True
      if not specified, all rows match

    order_by, if specified is (field_name, asc_or_desc).
      asc_or_desc is either "asc" or "desc" for ascending or decending sort order
      if not specifed, return rows in table order"""

    categories = table[0]

    output = []
    for row in table[1:]:
        safe_row = True
        ## splice off preds:
        if filters:
            for filter_ in filters:
                # print(filter_)
                pred = filter_[0] if filter_[0] != "=" else "=="
                field_or_const1 = filter_[1]
                field_or_const2 = filter_[2]

                if isinstance(field_or_const1, list) and isinstance(field_or_const2, list):
                    if not eval(str(row[categories.index(field_or_const1[0])]) + pred + str(row[categories.index(field_or_const2[0])])):
                        safe_row = False

                if isinstance(field_or_const1, list) and isinstance(field_or_const2, (float, int, str)):
                    if isinstance(row[categories.index(field_or_const1[0])], str):
                        if not row[categories.index(field_or_const1[0])] == field_or_const2:
                            safe_row = False

                    elif not eval(str(row[categories.index(field_or_const1[0])]) + pred + str(field_or_const2)):
                        safe_row = False

                if isinstance(field_or_const2, list) and isinstance(field_or_const1, (float, int, str)):
                    if isinstance(field_or_const1, str):
                        if not row[categories.index(field_or_const2[0])] == field_or_const1:
                            safe_row = False

                    elif not eval(str(field_or_const1) + pred + str(row[categories.index(field_or_const2[0])])):
                        safe_row = False

        if not safe_row:
            continue
        output.append(row)



    ##Order by
    if order_by:

        field_name = order_by[0]
        asc_or_desc = 1 if order_by[1] == "asc" else -1
        output_new = sorted(output[:], key=lambda row: row[categories.index(field_name)] * asc_or_desc)

    else:
        output_new = output[:]
    ## Which:
    new_out =[]
    for row in output_new:
        new_row = []
        for ele in row:
            if categories[row.index(ele)]  in which:
                new_row.append(ele)

        new_out.append(new_row)

    return new_out




############################################################
## Problem 3
############################################################

# Infinite lists

class InfiniteList:
    def __init__(self, f):
        """Create an infinite list where position i contains value f(i)."""
        self.f = f
        self.set_vals = dict()

    def __getitem__(self, i):
        """Standard Python method for defining notation ls[i], which expands to ls.__getitem__(i)"""
        if i in self.set_vals:
            return self.set_vals[i]
        return self.f(i)


    def __setitem__(self, i, val):
        """Standard Python method for defining notation ls[i] = val, which expands to ls.__setitem__(i, val)"""
        self.set_vals[i] = val
        return val


    def __iter__(self):
        """Standard Python method for producing a generator where called for, e.g. to loop over.
        Note that this iterator has infinitely many values to return, so a usual loop over it will never finish!
        It should yield values from index 0 to infinity, one by one."""


        i = 0
        while i > -1:
            yield self.__getitem__(i)
            i += 1

    def __add__(self, other):
        """Standard Python method for defining notation a + b, which expands to a.__add__(b).
        For this quiz question, other will be another InfiniteList, and the generated InfiniteList should
        add the elements of self and other, at each position."""

        # i = 0
        # for ele in other.__iter__():
        #     print(ele)
        #     self[i] += ele
        #     i += 1
        def add(i):
            return self[i] + other[i]
        return InfiniteList(add)


        # def f_new(i):
        #
        #     return self.f(i) + other.f(i)


        # new_list = InfiniteList(f_new)
        # for i in self.set_vals:
        #     if i in other.set_vals:
        #         new_list.set_vals[i] = other.set_vals[i] + self.set_vals[i]
        #
        #     else:
        #         new_list.set_vals[i] = other.f(i) + self.set_vals[i]
        #
        # for i in other.set_vals:
        #     if i in new_list.set_vals:
        #         continue
        #     new_list.set_vals[i] = self.f(i) + other.set_vals[i]
        #
        #
        # return new_list


    def __mul__(self, other):
        """Standard Python method for defining notation a * b, which expands to a.__mul__(b).
        For this quiz question, other will be a number, and the generated InfiniteList should
        multiply each position of self by other."""

        def f_new(i):

            return self.f(i) * other


        new_list = InfiniteList(f_new)
        for i in self.set_vals:
            new_list.set_vals[i] = other * self.set_vals[i]






        return new_list
