# NO IMPORTS ALLOWED!
# You are welcome to modify the classes below, as well as to implement new
# classes and helper functions as necessary.

## GLOBALS FOR STORING LETTERS AND NUMBERS
numerals = "0123456789"
alphas = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

class Symbol:

    ## RECREATION OF THE DUNDER METHODS
    def __add__(self, other):
        return Add(self, other)

    def __radd__(self, other):
        if type(other) == str:
            return Add(Var(other), self)
        else:
            return Add(Num(other), self)

    def __mul__(self, other):
        return Mul(self, other)

    def __rmul__(self, other):
        if type(other) == str:
            return Mul(Var(other), self)
        else:
            return Mul(Num(other), self)

    def __truediv__(self, other):
        return Div(self, other)

    def __rtruediv__(self, other):
        if type(other) == str:
            return Div(Var(other), self)
        else:
            return Div(Num(other), self)

    def __sub__(self, other):
        return Sub(self, other)

    def __rsub__(self, other):
        if type(other) == str:
            return Sub(Var(other), self)
        else:
            return Sub(Num(other), self)

class Var(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `name`, containing the
        value passed in to the initializer.
        """
        self.name = n
        self.op = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return 'Var(' + repr(self.name) + ')'

    def deriv(self, wrt):
        ## Base Cases for derivatives
        if self.name == wrt:
            ## Differentiation wrt the same variable
            return Num(1)
        else:
            ## Not dependent on this variable
            return Num(0)

    def simplify(self):
        ## Base Case for simplification
        return self

    def eval(self, mapping):
        ## Base Case for eval
        return mapping[self.name]

class Num(Symbol):
    def __init__(self, n):
        """
        Initializer.  Store an instance variable called `n`, containing the
        value passed in to the initializer.
        """
        self.n = n
        self.op = None

    def __str__(self):
        return str(self.n)

    def __repr__(self):
        return 'Num(' + repr(self.n) + ')'

    def deriv(self, wrt):
        ## Base Case for derivatives
        return Num(0)

    def simplify(self):
        ## Base Case for simplify
        return self

    def eval(self, mapping):
        ## Base Case for eval
        return self.n

class BinOp(Symbol):
    def __init__(self, left, right):
        ## Check if left is a symbol
        if isinstance(left, Symbol):
            self.left = left
        ## Create new symbol if left is not a symbol
        else:
            if type(left) == str:
                self.left = Var(left)
            else:
                self.left = Num(left)

        ## Check if right is a symbol
        if isinstance(right, Symbol):
            self.right = right
        ## Create new symbol if right is not a symbol
        else:
            if type(right) == str:
                self.right = Var(right)
            else:
                self.right = Num(right)

class Add(BinOp):
    def __init__(self, left, right):
        BinOp.__init__(self,left,right)
        self.op = "+"

    def __str__(self):
        ## Add has nothing of lower precendence, AND no special case as in subtraction. Therefore, just Base Case
        return str(self.left) + " " +  self.op + " " + str(self.right)

    def __repr__(self):
        return "Add("+repr(self.left) + "," + repr(self.right) + ")"

    def deriv(self, wrt):
        #Derivatives are linear
        return (self.left.deriv(wrt) + self.right.deriv(wrt))

    def simplify(self):
        ## Recurse to the bottom of the tree at the beginning
        self.left = self.left.simplify()
        self.right = self.right.simplify()


        ## Case with 2 Num objects (Covers 0 + 0)
        if type(self.left) == Num and type(self.right) == Num:
            return Num(self.left.n + self.right.n)

        ## Cases with 1 Num Object == 0
        if (type(self.left) == Num and self.left.n == 0):
            return self.right
        if (type(self.right) == Num and self.right.n == 0):
            return self.left

        ## Ultimate Base Case
        return self.left + self.right

    def eval(self, mapping):
        return self.left.eval(mapping) + self.right.eval(mapping)

class Sub(BinOp):
    def __init__(self, left, right):
        BinOp.__init__(self,left,right)
        self.op = "-"

    def __str__(self):
        ## Case where the Right term is either subtraction or addition --> Special Case!!
        if self.right.op is not None and self.right.op in "-+":
            return str(self.left) + " " +  self.op + " (" + str(self.right) +")"

        ## Base case: a - b
        return str(self.left) + " " +  self.op + " " + str(self.right)

    def __repr__(self):
        return "Sub("+repr(self.left) + "," + repr(self.right) + ")"

    def deriv(self, wrt):
        ## Derivatives are linear
        return (self.left.deriv(wrt) - self.right.deriv(wrt))

    def simplify(self):
        ## Recurse to the bottom of the tree first
        self.left = self.left.simplify()
        self.right = self.right.simplify()

        ## Case with 2 Num objects being subtracted (Covers 0-0)
        if type(self.left) == Num and type(self.right) == Num:
            return Num(self.left.n - self.right.n)


        # This case is ignored for the purposes of this lab
        # but could be reimplemented for personal use
        # if (type(self.left) == Num and self.left.n == 0):
        #     return (-1 * self.right).simplify()

        ## Case wih Right Num == 0
        if (type(self.right) == Num and self.right.n == 0):
            return self.left

        #Ultimate Base Case
        return self.left - self.right

    def eval(self, mapping):
        ## Recursively call eval
        return self.left.eval(mapping) - self.right.eval(mapping)

class Mul(BinOp):
    def __init__(self, left, right):
        BinOp.__init__(self,left,right)
        self.op = "*"

    def __str__(self):

        ## Case with two sums/diffs multiplied together: (a + b) * (c + d)
        if self.left.op is not None and self.left.op in "-+" and self.right.op is not None and self.right.op in "-+":
            return "(" + str(self.left) + ") " +  self.op + " (" + str(self.right) + ")"

        ## Case where one sum/diff multiplied by a single symbol LEFT: (a + b) * c
        if self.left.op is not None and self.left.op in "-+":
            return "(" + str(self.left) + ") " +  self.op + " " + str(self.right)

        ## Case where one sum/diff multiplied by a single symbol RIGHT: a * (b + c)
        if self.right.op is not None and self.right.op in "-+":
            return str(self.left) + " " +  self.op + " (" + str(self.right) +")"

        ## Base case: a * b
        return str(self.left) + " " +  self.op + " " + str(self.right)

    def __repr__(self):
        return "Mul("+repr(self.left) + "," + repr(self.right) + ")"

    def deriv(self, wrt):
        ## Product rule
        return (self.left * self.right.deriv(wrt) + self.right * self.left.deriv(wrt))

    def simplify(self):
        ## Recurse down the tree to the bottom before continuing
        self.left = self.left.simplify()
        self.right = self.right.simplify()

        ## 2 Num objects multiplied case
        if type(self.left) == Num and type(self.right) == Num:
            return Num(self.left.n * self.right.n)

        ## Multiply by 0 cases
        if (type(self.left) == Num and self.left.n == 0) or (type(self.right) == Num and self.right.n == 0):
            return Num(0)

        ## Multiply by 1 cases
        if (type(self.left) == Num and self.left.n == 1):
            return self.right
        if (type(self.right) == Num and self.right.n == 1):
            return self.left

        ## Ultimate Base Case
        return self.left * self.right

    def eval(self, mapping):
        return self.left.eval(mapping) * self.right.eval(mapping)

class Div(BinOp):
    def __init__(self, left, right):
        BinOp.__init__(self,left,right)
        self.op = "/"

    def __str__(self):

        ## Two sums/diffs being divided: (a + b) / (a - b)
        if self.left.op is not None and self.left.op in "-+" and self.right.op is not None and self.right.op in "-+":
            return "(" + str(self.left) + ") " +  self.op + " (" + str(self.right) + ")"

        ## Coupled Cases: First if statement covers our Special Case as in the lab doc
        if self.right.op is not None and self.right.op in "-+*/":

            ## Covers situations in which the Right op is * or /  and the Left is ALSO of lower precendence: (a + b) / (c / d)
            if self.left.op is not None and self.left.op in "-+":
                return  "(" + str(self.left) + ") " +  self.op + " (" + str(self.right) + ")"

            ## Covers the definition of the Special Case as in the lab doc, and when Right is of lower precendence
            return str(self.left) + " " +  self.op + " (" + str(self.right) +")"

        ## Covers case where Left is of lower precedence: (a + b) / c
        if self.left.op is not None and self.left.op in "-+":
            return "(" + str(self.left) + ") " +  self.op + " " + str(self.right)


        ## Base Case: a / b
        return str(self.left) + " " +  self.op + " " + str(self.right)

    def __repr__(self):
        return "Div("+repr(self.left) + "," + repr(self.right) + ")"

    def deriv(self, wrt):
        ## Quotient rule
        return((self.right * self.left.deriv(wrt) - self.left * self.right.deriv(wrt)) / (self.right * self.right))

    def simplify(self):
        ## Recurse all the way down the tree before continuing
        self.left = self.left.simplify()
        self.right = self.right.simplify()

        ## Case with 0 / E
        if type(self.left) == Num and self.left.n == 0:
            return Num(0)

        ## Case with E / 1
        if type(self.right) == Num and self.right.n == 1:
            return self.left

        ## Double Num division: can be evaluated
        if type(self.left) == Num and type(self.right) == Num:
            return Num(self.left.n / self.right.n)

        ## Ultimate Base Case
        return self.left / self.right

    def eval(self, mapping):
        return self.left.eval(mapping) / self.right.eval(mapping)

## NON-CLASS METHODS:
def tokenize(text):
    '''
    Takes a string - text - and returns a tuple of all
    important tokens (complete integers, operators, and variable names)
    '''
    output = []

    for i in range(len(text)):
        try:
            ## Adding numbers into the output -- accounts for multidigit positive and negative numbers
            if text[i] in numerals and (text[i-1][-1] in numerals or (output[-1] == "-" and text[i-1] != " ")):
                output[-1] += text[i]
                continue
        except:
            pass

        ## Get rid of all spaces
        if text[i] == " ":
            continue

        output.append(text[i])

    return tuple(output)

def parse(tokens):
    '''
    Takes a tuple of all important tokens from a string and recursively calls the parse_expression method
    '''

    def parse_expression(index):
        '''
        Takes int index and recursively returns the parsed expression described by the tuple tokens
        '''

        ## Instantiate working token
        token = tokens[index]

        ## Base Case for finding alphabetical Variables
        if token in alphas:
            return Var(token), index + 1

        ## Beginning of operator expression
        elif token == "(":
            ## Recurse down the tree of the left side of this operation
            left_side, from_left = parse_expression(index + 1)
            ## Find the operator for this initial open parenthesis
            operator = tokens[from_left]
            ## Recurse down the tree of the right side of this operation
            right_side, from_right = parse_expression(from_left + 1)


            ## Cases for all of the operator types
            if operator == "+":
                return Add(left_side, right_side), from_right + 1
            elif operator == "-":
                return Sub(left_side, right_side), from_right + 1
            elif operator == "*":
                return Mul(left_side, right_side), from_right + 1
            elif operator == "/":
                return Div(left_side, right_side), from_right + 1

        ## Base Case for integers:
        else:
            temp_int = int(token)
            return Num(temp_int), index + 1

    parsed_expression, next_index = parse_expression(0)

    return parsed_expression

def sym(input):
    '''
    Calls the above functions to return a parsed symbol object
    '''
    return parse(tokenize(input))




if __name__ == "__main__":
    pass
