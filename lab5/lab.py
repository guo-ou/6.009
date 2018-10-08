"""6.009 Lab 5 -- Boolean satisfiability solving"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS


def satisfying_assignment(formula):
    """Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> sa = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> ('a' in sa and sa['a']) or ('b' in sa and not sa['b']) or ('c' in sa and sa['c'])
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]]) is None
    True
    """



    def recur_helper(working_formula, assignments=None):

        if assignments is None:
            assignments = dict()


        if working_formula == []:
            return assignments

        elif working_formula is None:
            return None


        else:
            cur_var = working_formula[0][0][0]

            tru_dict = {cur_var: True}
            simp_form,_ = simplify_formula(working_formula, tru_dict)
            if simp_form is not None:
                next_step_down = recur_helper(simp_form, assignments)
                if next_step_down is not None:
                    assignments.update(tru_dict)
                    return next_step_down


            fal_dict = {cur_var: False}
            simp_form,_ = simplify_formula(working_formula, fal_dict)
            if simp_form is not None:

                next_step_down =  recur_helper(simp_form, assignments)
                if next_step_down is not None:
                    assignments.update(fal_dict)
                    return next_step_down

            else:
                return None


    return recur_helper(formula)




def simplify_formula(formula, assignments):
    '''
      Input: a boolean formula in the CNF format described above.
            a set of assignments to boolean variables represented as a dictionary
            from variables to boolean values.
      Output: a pair (Formula, Changed), where Formula is
      the new simplified formula, and Changed is a boolean
      that determines whether or not the simplification added new
      assignments. If the assignment causes the formula to
      evaluate to False, you should return (None, False).
      Effects: the operation potentially adds new assignments to
      assignments. However, the operation should NOT modify
      the input formula when creating the output (although it is ok
        for the output formula to share unchanged clauses with the input formula).

      Note that when the simplification creates new assignments,
      those assignments may themselves enable further simplification.
      You should make sure all those newly enabled simplifications
      are performed as well.

      It is advised that you write your own tests for this function.

     '''

    working_formula = formula[:]

    def helper(formula, assignments):
        changed = False
        output = []

        for clause in formula:
            output_clause = []

            #Length 1 clauses: SHOULD NOT BE OUTPUT
            if len(clause) == 1:
                if clause[0][0] in assignments:
                    if clause[0][1] != assignments[clause[0][0]]:
                        return (None, False, assignments)

                assignments[clause[0][0]] = clause[0][1]
                changed = True


            #Length >1 clauses: SHOULD BE OUTPUT
            else:
                for literal in clause:
                    if literal[0] in assignments:
                        if literal[1] != assignments[literal[0]]:
                            continue
                        else:
                            output_clause = None
                            break
                    else:
                        output_clause.append(literal)

            if output_clause is None:
                pass
            elif len(output_clause) == 0:
                return None, changed, assignments

            elif len(output_clause) == 1:
                if output_clause[0][0] in assignments:
                    if output_clause[0][1] != assignments[output_clause[0][0]]:
                        return (None, False, assignments)

                assignments[output_clause[0][0]] = output_clause[0][1]
                changed = True

            else:
                output.append(output_clause)

        if changed:
            output, changed, assignments =  helper(output, assignments)

        return (output, changed, assignments)

    final_out, final_change, final_assign = helper(formula, assignments)

    return final_out, final_change

def make_actor_dict(film_db):
    '''
    Creates a dictionary from a film db where actors are
    the keys and the values are sets of actor ids for actors
    with whom the key actor has worked.
    '''
    out_dict = dict()
    for film in film_db:
        if film[0] == film[1]:
            continue
        if film[0] not in out_dict:
            out_dict[film[0]] = {film[1]}
        if film[1] not in out_dict:
            out_dict[film[1]] = {film[0]}

        out_dict[film[0]].add(film[1])
        out_dict[film[1]].add(film[0])

    return out_dict

def make_vars_for_actors(K, film_db):
    '''
    returns all of the possible combinations of actor-manager pairs and stores
    them in a dictionary where the keys are actors and the values are lists of
    possible actor-manager combos
    '''
    actor_dict = make_actor_dict(film_db)
    indicator_dict = dict()
    for actor in actor_dict:
        #create list of tuples below
        indicator_dict[actor] = [(actor, i) for i in range(K)]

    return indicator_dict


def make_one_manager_constraints(K, indicator_dict):
    '''
    Creates a CNF formatted constraint rule ensuring that all of the actors have just one manager.
    '''

    output_constraint = []
    for actor in indicator_dict:
        all_combos = []
        for i in range(K):
            #One extra term with all true guaranteeing that at least one of the combinations is true
            all_combos.append((indicator_dict[actor][i],True))
            for j in range(K):
                if i != j:
                    #Ensure that every combination of actor-manager for all managers and all actors is false, ensuring that no double manager situations exist
                    output_constraint.append([(indicator_dict[actor][i],False), (indicator_dict[actor][j],False)])
        output_constraint.append(all_combos)
    return output_constraint


def make_different_constraint(K, film_db, indicator_dict):
    '''
    Makes the CNF constraint that all actors who work together must have different managers
    '''
    output_constraint = []
    actor_dict = make_actor_dict(film_db)
    seen_actors = set()
    for actor in actor_dict:
        actor_inds = indicator_dict[actor]
        seen_actors.add(actor)
        fellows = actor_dict[actor]
        for fellow in fellows:
            fellow_inds = indicator_dict[fellow]

            for i in range(K):
                if fellow in seen_actors:
                    continue

                #No two actors who have worked together can have the same manager index i
                output_constraint.append([(actor_inds[i], False), (fellow_inds[i], False)])

    return output_constraint



def managers_for_actors(K, film_db):
    '''
    Input:
       K , number of managers available.
       film_db, a list of [actor, actor, film] triples describing that two
       actors worked together on a film.
    Output:
        A dictionary representing an assignment of actors to managers, where
        actors are identified by their numerical id in film_db and
        managers are identified by a number from 0 to K-1.
        The assignment must satisfy the constraint that
        if two actors acted together in a film, they should not have the
        same manager.
        If no such assignment is possible, the function returns None.

    You can write this function in terms of three methods:
        make_vars_for_actors: for each actor in the db, you want an indicator
        variable for every possible manager indicating whether that manager
        is the manager for that actor.

        make_one_manager_constraints: This function should create constraints that
        ensure that each actor has one and only one manager.

        make_different_constraint: This function should create constraints
        that ensure that each actor has a different manager from other actors
        in the same movie.

    '''




    ind_dict = make_vars_for_actors(K,film_db)

    one_constraints = make_one_manager_constraints(K, ind_dict)
    pair_constrants = make_different_constraint(K, film_db, ind_dict)

    sa = satisfying_assignment(one_constraints + pair_constrants)
    if sa is None:
        return None


    output = {}
    for pairing in sa:
        if not sa[pairing]:
            continue
        output[pairing[0]] = pairing[1]
    return output



def check_solution(sol, K, film_db):
    '''
    Input:
        K, number of managers
        flim_db, a list of [actor, actor, film] triples describing that two
        actors worked together on a film.
        sol, an assignment of actors to managers.
    Output:
        The function returns True if sol satisfies the constraint that
        if two actors acted together in a film, they should not have the
        same manager and every manager has an ID less than K.
        It returns False otherwise.
    '''

    actor_dict = make_actor_dict(film_db)


    for act, man in sol.items():
        if man >= K:
            return False
        fellows = actor_dict[act]
        for fel in fellows:
            if man == sol[fel]:
                return False
    return True
