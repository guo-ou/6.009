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

def prod(a):
    output = 1
    for i in a:
        output = output * i
    return output

def div(a):
    output = a[0]
    for i in a[1:   ]:
        output = output / i
    return output

carlae_builtins = {
    '+': sum,
    '-': lambda args: -args[0] if len(args) == 1 else (args[0] - sum(args[1:])),
    "*": prod,
    "/": div
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


built_ins = Environment()
built_ins.variables = carlae_builtins

def evaluate(tree, env=None):
    """
    Evaluate the given syntax tree according to the rules of the carlae
    language.

    Arguments:
        tree (type varies): a fully parsed expression, as the output from the
                            parse function
    """

    if not tree: ## Empty tree error
        raise EvaluationError("empty tree")

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
            elif sub_tree != "lambda" and sub_tree != "define":
                ## Invalid
                raise EvaluationError("variable not present in current environment")
            else:
                ## Keyword
                return sub_tree

        else:
            ## LISTS
            token = sub_tree[0] ## Grab first element

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


def result_and_env(tree, env=None):
    if env is None:
        env = Environment(built_ins)

    return evaluate(tree, env), env



def REPL():


    inp = None
    env = Environment(built_ins)
    while inp != "QUIT":
        inp = input('in>')

        print("out>" + str(evaluate(parse(tokenize(inp)), env)))



if __name__ == '__main__':
    # code in this block will only be executed if lab.py is the main file being
    # run (not when this module is imported)

    REPL()
