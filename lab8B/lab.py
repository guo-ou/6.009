"""6.009 Lab 8A: carlae Interpreter"""

import sys


class EvaluationError(Exception):
    """Exception to be raised if there is an error during evaluation."""
    pass


def tokenize(source):
    """
    Splits an input string into meaningful tokens (left parens, right parens,
    other whitespace-separated values).  Returns a list of strings.

    Arguments:
        source (str): a string containing the source code of a carlae
                      expression
    """
    ## Replace special characters such that they are all separated by spaces so that
    ## we can use _list_.split() to separate pertinent characters in the final output
    spaced = source.replace(")", " ) ").replace("(", " ( ").replace("\n", " \n ")

    ## Create individual 'clauses' for each line in a multiline statement
    ## If there is no newline in the text, we should place the string in an empty list so that
    ## we can iterate through it in the next step (it is still just one clause)
    if "\n" in spaced:
        spaced = spaced.split("\n")
    else:
        spaced = [spaced]

    ## Loop through the clauses and splice off the comments from each one
    for x in range(len(spaced)):
        if ";" in spaced[x]:
            spaced[x] = spaced[x][:spaced[x].index(";")]

    ## Rejoin all of the clauses into one string
    spaced = "".join(spaced)

    ## Split by spaces into pertinent items from the original string
    return spaced.split()


def check_parens(tokens):
    parens = 0
    for i in range(len(tokens)):
        if parens == 0 and i != 0:
            raise SyntaxError("misplaced clauses")
        if tokens[i] == "(":
            parens += 1
        if tokens[i] == ")":
            parens -= 1

def parse(tokens):
    """
    Parses a list of tokens, constructing a representation where:
        * symbols are represented as Python strings
        * numbers are represented as Python ints or floats
        * S-expressions are represented as Python lists

    Arguments:
        tokens (list): a list of strings representing tokens
    """
    ## Quick count of left and right parentheses: optimized such that
    ## the parser function does not have to run in order to find this
    if tokens.count(")") != tokens.count("("):
        raise SyntaxError("Mismatched Parentheses")

    ## Quick search for tokens that have no parentheses and do not contain just one entry
    if ("(" not in tokens or ")" not in tokens) and len(tokens) > 1:
        raise SyntaxError("Missing Parentheses")

    ## Quick check to see if user put something outside of an S-exression not enclosed in a larger expression "(+ x y) y"
    if (tokens[0] != "(" and len(tokens) > 1) or (tokens[-1] != ")" and len(tokens) > 1):
        raise SyntaxError("Item outside parentheses in expression with parentheses")

    check_parens(tokens)

    ## Copy tokens to avoid aliasing issues
    new_tokens = tokens[:]




    def parser(tokens):
        '''
        Recursive helper function that takes a tokenized input list and returns a properly formatted
        output, as described above
        '''
        output = [] ## instantiate new list for output

        while len(tokens) != 0:

            token = tokens[0] ## grab first index to analyze

            if token == "(":
                ## Beginning of S-Expression
                next, rem_tokens = parser(tokens[1:])
                ## next is the output of our parser, and rem_tokens are the remaining
                ## tokens left to be parsed after we finished evaluating the S expression
                ## at the deepest recursive level
                output.append(next)

                if not rem_tokens: ## We have hit the end of the input tokens
                    return output[0]
                else:
                    tokens = rem_tokens ## if not, we dont care about the tokens we have passed
                                        ## over at a deeper recursive level, so we must move on
                                        ## to the remaining

            elif token == ")":
                ## End of S-Expression
                remaining_tokens = tokens ## Assign what is left of tokens to remaining_tokens

                if not output and remaining_tokens:
                    ## Kills all instances of )( parentheses in locations in which that is improper
                    raise SyntaxError("Misordered Parentheses")

                return output, remaining_tokens


            else:
                ## Properly add individual atomic objects to the output
                try:
                    if "." in token:
                        output.append(float(token))
                    else:
                        output.append(int(token))
                except:
                    output.append(token)

            del tokens[0] ## Splice off the first index of tokens such that the while loop can complete


        return output[0] ## output is a list containing the correct output as its only entry so we must grab the 0th index

    fin_out = parser(new_tokens)

    return fin_out


## Builtin Functions:
def prod(a):
    output = 1
    for i in a:
        output = output * i
    return output

def div(a):
    output = a[0]
    for i in a[1:]:
        output = output / i
    return output

def all_eq(a):
    return len(set(a)) == 1

def g_than(a):
    return all(i>j for i,j in zip(a, a[1:]))

def l_than(a):
    return all(i<j for i,j in zip(a, a[1:]))

def g_than_eq(a):
    return all(i>=j for i,j in zip(a, a[1:]))

def l_than_eq(a):
    return all(i<=j for i,j in zip(a, a[1:]))

def cons(a):
    car = a[0]
    cdr = a[1]
    new_pair = Pair(car, cdr)

    return new_pair

def list_(a):
    remaining = a
    if remaining == []:
        return None

    new_list = create_list(remaining) ## Call our helper function that takes a
                                      ## python list and creates a linked list
    return new_list

def car(pair):
    try:
        out_val = pair[0].car
        return out_val
    except:
        raise EvaluationError("object is not of type Pair")

def cdr(pair):
    try:
        new_cdr = pair[0].cdr
        return new_cdr
    except:
        EvaluationError("object is not of type Pair")

def length(a):
    a = a[0]

    if not a:
        return 0

    if not isinstance(a, Pair):
        raise EvaluationError("length called on non Pair object")
    else:
        if not isinstance(a.cdr, Pair) and a.cdr:
            raise EvaluationError("not a list object")

    count = 1
    while a.cdr: ## While until we hit a nil object
        count +=1
        a = a.cdr
    return count

def index(a):
    list_obj = a[0]
    work_index = a[1]

    if not isinstance(list_obj, Pair):
        raise EvaluationError("length called on non Pair object")

    if work_index == 0: ## Grab first index -- simple case
        return list_obj.car

    count = 1
    working_ele = list_obj.cdr
    if not isinstance(working_ele, Pair) and working_ele is not None:
        ## This accounts for instances of indexing done on Cons objects -- requires a 0 index
        if work_index == 0:
            return list_obj.car
        else:
            raise EvaluationError("cons obj given with non-zero index")



    while count != work_index: ## loop until we hit the count we want,
                               ## if we hit the end of the list, pop a
                               ## list index out of range error
        count += 1
        if working_ele is None:
            raise EvaluationError("list index out of range")
        working_ele = working_ele.cdr
    return working_ele.car

def concat(a):

    ## Basic checks for simple concat calls
    if len(a) == 0:
        return None

    if len(a) == 1:
        return a[0]

    ## This allows us to accommodate for occurrences of None (empty lists) in concat calls
    ## which have no impact on the output, so we can simply remove them
    while None in a:
        a.pop(a.index(None))

    if not all(isinstance(x, Pair) for x in a):
        raise EvaluationError("objects given are not lists")

    try:
        ## We are going to loop over all of the values in each list and "append" each to an empty list
        ## extend is a helper function that acts analogously to python list objects method .append()
        out_list = Pair(a[0].car, None)
        count = 0
        for list_obj in a:

            if count != 0 or out_list.car is None:
                extend(out_list, list_obj.car) ## put the first car in for each list

            obj = list_obj.cdr ## "recursively" loop down each list and extend each element
            while obj is not None:
                if obj.car is not None:
                    extend(out_list, obj.car)
                obj = obj.cdr
            count += 1
    except:
        ## error popped when .car attribute called, so this must be a Cons object
        raise EvaluationError("cannot concatenate Cons objects")

    if out_list.car is None:
        return out_list.cdr

    return out_list

def map_(a):

    if len(a) != 2:
        raise EvaluationError("not the right number of arguments")

    f = a[0]
    old_list = a[1]

    if old_list is None:
        return None

    if not isinstance(old_list, Pair):
        raise EvaluationError("not a Pair object to map onto")

    return Pair(f([old_list.car]), map_([f, old_list.cdr])) ## Recursively call map on the remaining elements of a linked list

def filter_(a):

    if len(a) > 2:
        raise EvaluationError("too many arguments")

    if len(a) == 1:
        raise EvaluationError("not enough args")

    f = a[0]
    old_list = a[1]

    if old_list is None:
        return None

    ## If our element passes the filter, we should put it in the Pair object, if not, we should skip it and call filter on the remaining cdr
    return Pair(old_list.car, filter_([f, old_list.cdr])) if f([old_list.car]) else filter_([f, old_list.cdr])

def reduce_(a):
    f = a[0]
    old_list = a[1]
    start = a[2]

    if old_list is None:
        return start

    ## recursively call reduce with a running tally of the output value
    return reduce_([f, old_list.cdr, f([start, old_list.car])])

def extend(old_list, value):

    obj = old_list
    while obj.cdr is not None:
    ## Loop through the list until we reach the end of the linked list
        obj = obj.cdr

    obj.cdr = Pair(value, None) ## add the newest Pair object to the end of the list

    return old_list

def begin(a):
    return a[-1]

carlae_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "*": prod,
    "/": div,
    "=?": all_eq,
    ">": g_than,
    "<": l_than,
    ">=": g_than_eq,
    "<=": l_than_eq,
    "#f": False,
    "#t": True,
    "nil": None,
    "not": lambda x: not x[0],
    "cons": cons,
    "list": list_,
    "car": car,
    "cdr": cdr,
    "length": length,
    "elt-at-index": index,
    "concat": concat,
    "map": map_,
    "filter": filter_,
    "reduce": reduce_,
    "begin": begin
    # "abs": lambda x: x[0] if x[0]>0 else -x[0] ## support for abs function
}

class Environment(object):
    def __init__(self, parent=None):
        self.parent = parent
        self.variables = dict()

    def __contains__(self, variable):
        if variable in self.variables:
            return True
        else:
            if self.parent is not None:
                return self.parent.__contains__(variable)
            else:
                return False



    def __setitem__(self, variable, value):
        self.variables[variable] = value

    def __getitem__(self, variable):
        if variable in self.variables:

            return self.variables[variable]
        else:
            return self.parent.__getitem__(variable)

class Function(object):
    def __init__(self, params, func, environ):
        self.params = params
        self.func = func
        self.environ = environ

    def __call__(self, params):
        '''
        Used such that we can call builtins and Function objects in an identical way --
        set all variables to a new environment (a child of self.environ) and call evaluate on the
        Function body
        '''
        new_env = Environment(self.environ)

        for i in range(len(params)):
            new_env[self.params[i]] = params[i]

        return evaluate(self.func, new_env)

class Pair(object):
    def __init__(self, car, cdr):
        self.car = car
        self.cdr = cdr

built_ins = Environment()
built_ins.variables = carlae_builtins

special_forms = ["define", "lambda", "if", "and", "or", "cons", "list", "map",
                "filter", "reduce", "concat", "let", "set!"]

def create_list(args):
    '''
    Recursively creates the linked list structure use for list definitions in LISP dialects.
    Instantiates Pair objects from the class defined in this document.
    '''
    car = args[0]
    if len(args) == 1:
        cdr = None
    else:
        cdr = create_list(args[1:])
    return Pair(car, cdr)


def evaluate(tree, env=None):
    """
    Evaluate the given syntax tree according to the rules of the carlae
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """

    ## Instantiate the environment
    if env is None:
        env = Environment(built_ins)


    def helper(sub_tree, env):
        '''
        Takes a sub_tree element (of same set of types as tree in evaluate) and evaluates the element
        recursively. Many cases are enumerated by inline comments below.
        '''


        if isinstance(sub_tree, (int, float)):
            ## NUMBERS -- auto return
            return sub_tree

        elif isinstance(sub_tree, str):
            ## VARIABLES/KEYWORDS -- check if valid then return
            if sub_tree in env:
                ## Valid
                return env[sub_tree]
            elif sub_tree not in special_forms:
                ## Invalid
                raise EvaluationError("variable not present in current environment")
            else:
                ## Keyword
                return sub_tree

        else:
            ## LISTS
            try:
                token = sub_tree[0] ## Grab first element
            except:
                raise EvaluationError("hit an improperly empty list")
            ## RECURSE DOWN THE TREE -- this will give us the function we need to operate, or will pop an error
            ## All S-Expressions should begin with a function call or keyword
            next_obj = helper(token, env)


            if next_obj == "define":
                ## SPECIAL FORM: Variable definition
                name = sub_tree[1] ## Variable name
                eval = sub_tree[2] ## Variable value, must be evaluated recursively as well

                if isinstance(eval, str) and eval not in env: ## Trying to assign a variable to another that has
                                                              ## no assignment in the environment

                    raise EvaluationError("value to assign to variable not in current environment")

                if isinstance(name, list):
                    ## Case with simplified functional definitions
                    params = name[1:]
                    name = name[0]
                    eval = ["lambda", params, eval] ## Restructure the eval such that it can be passed into the lambda case


                evaluated = helper(eval, env) ## evaluate the r.h.s of the variable definition

                env[name] = evaluated ## set variable in environment
                return env[name] ## return the variable value

            elif next_obj == "lambda":
                ## SPECIAL FORM: Function definition

                params = sub_tree[1] ## input parameters
                func = sub_tree[2] ## actual operations to be performed
                out_func = Function(params, func, env) ## instantiate new Function object

                return out_func

            elif next_obj == "if":
                ## SPECIAL FORM: Conditional
                cond = sub_tree[1]
                truexp = sub_tree[2]
                falexp = sub_tree[3]

                eval_cond = helper(cond, env) ## evaluate the condition
                if eval_cond:
                    return helper(truexp, env) ## truthy option
                return helper(falexp, env) ## falsely option

            elif next_obj == "and":
                ## SPECIAL FORM: and
                conds = sub_tree[1:]
                # if all(helper(x,env) for x in conds): ## all expressions must be truthy
                                                      ## Python documentation says that this
                                                      ## is equivalent to looping through until
                                                      ## finding a falsely argument -- therefore
                                                      ## it follows the protocol for short circuiting
                for x in conds: ## Separate solution to the short_circuit problem
                    if not helper(x, env):
                        return False
                return True

            elif next_obj == "or":
                ## SPECIAL FORM: or
                conds = sub_tree[1:]
                # if any(helper(x,env) for x in conds): ## any expression must be truthy
                                                      ## Python documentation says that this
                                                      ## is equivalent to looping through until
                                                      ## finding a truthy argument -- therefore
                                                      ## it follows the protocol for short circuiting

                for x in conds: ## Separate solution to the short_circuit problem
                    if helper(x, env):
                        return True
                return False

            elif next_obj == "let":
                ## SPECIAL FORM: let
                vals = sub_tree[1]
                body = sub_tree[2]

                new_env = Environment(env)
                for val in vals:
                    new_env[val[0]] = helper(val[1], env) ## set all variables in a temporary environment

                return helper(body, new_env) ## call helper on the body with the temporary environment


            elif next_obj == "set!":
                ## SPECIAL FORM: set!
                var = sub_tree[1]
                new_val = sub_tree[2]

                env_obj = env
                ## Loop down such that we can directly alter the variables
                ## dictionary from the env in which the variable is found
                while var not in env_obj.variables:
                    env_obj = env_obj.parent
                    if env_obj is None:
                        raise EvaluationError("Variable not present")

                env_obj.variables[var] = helper(new_val, env) ## reset the variable value at the source
                return env[var] ## grab the variable from the environment


            elif isinstance(next_obj, Function):
                ## Encountered a user defined Function object
                new_env = Environment(next_obj.environ) ## Create a new environment for this function with
                                                        ## with the environment in which the function was created
                                                        ## as the parent
                usr_params = sub_tree[1:] ## Grab the user's input parameters (guaranteed to be here)
                if len(usr_params) != len(next_obj.params):
                    ## User improperly listed his/her variable assignments for the function call
                    raise EvaluationError("mismatched parameters for function call")

                ## Create new assignments of variables in the new environment
                for i in range(len(next_obj.params)):
                    new_env[next_obj.params[i]] = helper(usr_params[i], env) ## make sure to evaluate the r.h.s of all new variable defs
                                                                             ## allows for functional compositions "f(g(x))"
                return helper(next_obj.func, new_env) ## evaluate the functional part of the object with these new assignments

            elif next_obj in built_ins.variables.values():
                ## Encountered a built in -- they all require this format of fully evaluated sub_objects or else they will pop TypeErrors
                return next_obj([helper(x, env) for x in sub_tree[1:]])

            else:
                ## There was no function listed in an S-Expression somewhere in the user's input
                raise EvaluationError("no function listed in an S-expression")


    return helper(tree, env)


def evaluate_file(filename, REPL_tog=False, env=None):
    '''
    Similar to result_and_env, we simply
    load the file, and evaluate the lines
    of code from the document
    '''
    if env is None:
        env = Environment(built_ins)

    with open(filename, "r") as f:
        lines = f.read()
        if REPL_tog:
            return evaluate(parse(tokenize(lines)), env), env ## Pass environment into REPL
        return evaluate(parse(tokenize(lines)), env)



def result_and_env(tree, env=None):
    if env is None:
        env = Environment(built_ins)

    return evaluate(tree, env), env

def REPL(env=None):
    inp = None
    if env is None:
        env = Environment(built_ins)
    while True:
        inp = input('in>')
        if inp == "QUIT":
            break

        try:
            print("out>" + str(evaluate(parse(tokenize(inp)), env)))
        except:
            ## Make sure we don't exit the REPL when we hit an error
            print("Error popped during evaluation of input:", sys.exc_info()[0])
            continue



if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    ## Run this if lab.py is called with file arguments after
    if len(sys.argv) != 1:
        for file in sys.argv:
            if file == "lab.py":
                continue

            output, environ = evaluate_file(file, True)
            print(output)

    try:
        REPL(environ)
    except:
        REPL()
