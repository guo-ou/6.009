# NO IMPORTS ALLOWED!
import json

def did_x_and_y_act_together(data, actor_id_1, actor_id_2):
    '''
    Loops over all of thge entries in the data json.
    If it reaches an entry with both actors listed,
    it returns True. Otherwise False
    '''

    for pairing in data:
        if actor_id_1 in pairing[:-1] and actor_id_2 in pairing[:-1]:
            return True
    return False

def get_actor_id(actor_name):
    '''
    Grabs the id of an actor with a supplied actor_name. Opens the names.json
    '''

    with open('resources/names.json') as f:
        namesdb = json.load(f)
        return namesdb[actor_name]

def get_actor_name(id_to_get):
    '''
    The inverse of get_actor_id. Loops over the names.json
    and returns the name of the actor corresponding to a given id.
    '''

    with open('resources/names.json') as f:
        namesdb = json.load(f)
        for name, id_ in namesdb.items():
            if id_ == id_to_get:
                return name


def get_movie_name(id_to_get):
    '''
    Similar to get_actor_name. This returns the name of a movie withi a given id.
    '''

    with open('resources/movies.json') as f:
        moviedb = json.load(f)
        for name, id_ in moviedb.items():
            if id_ == id_to_get:
                return name



def build_actor_workset(data):
    '''
    This is a major portion of optimizing the search algorithm.
    Rather than loop over the json repeatedly, it is more efficient
    to create a hashable datastructure containing the information of
    all actor pairs. In this case, this is a dictionary (actor_dict)
    in which each key is an actor id, and the entries are sets of the
    ids of actors with whom the key actor has worked. Creating these
    adjacency relations allows the program to search a tree, rather than a list.
    '''

    actor_dict = {}
    for pairing in data:
        new_0 = pairing[0] not in actor_dict
        new_1 = pairing[1] not in actor_dict

        ## Create empty sets of the actors with whom a given actor has worked.
        if new_0:
            actor_dict.update({pairing[0] : {pairing[1]} })
        if new_1:
            actor_dict.update({pairing[1] : {pairing[0]} })

        ## Dynamically add all new actors to
        if not new_0:
            actor_dict[pairing[0]].add(pairing[1])

        if not new_1:
            actor_dict[pairing[1]].add(pairing[0])

        ## we want to ignore films in which the actor appears paired with him/herself
        try:
            actor_dict[pairing[0]].remove(pairing[0])
            actor_dict[pairing[0]].remove(pairing[0])
        except:
            pass

    return actor_dict

def build_movie_casts(data):
    '''
    This is programatically identical to the above function, but formatted for movies. Returns a dict in the form movie:set(cast).
    '''

    movie_dict = {}
    for pairing in data:
        new_mov = pairing[2] not in movie_dict

        if new_mov:
            movie_dict.update({pairing[2]: {pairing[0], pairing[1]}})

        else:
            movie_dict[pairing[2]].add(pairing[0])
            movie_dict[pairing[2]].add(pairing[1])

    return movie_dict


def get_actors_with_bacon_number(data, n):
    '''
    Calls the build_actor_workset function. Iterates over
    the acotr_dict a number of times prescribed by the user.
    Returns a set of actors with a bacon number n. Begins by
    finding all the actors with bacon number 1
    (easier to separate because it is specific to Kevin Bacon as the source node).
    The same algorithm for the bacon number 1 actors is applied
    to each node found in that set.
    '''


    if n == 0:
        return {4724}

    elif type(n) != int or n<0:

        return None


    actor_dict = build_actor_workset(data)

    deg_1_bacon = set()
    for actor in actor_dict:
        if 4724 in actor_dict[actor]:
            deg_1_bacon.add(actor)

    bacons =  [deg_1_bacon]

    for iteration in range(n-1):

        ## Ignore huge n values with no actors in past 3 iterations -- personal choice of 3.
        if len(bacons[-1]) == 0 and len(bacons[-2]) == 0 and len(bacons[-3]) == 0:
            return []


        new_iter_bacon = set()
        for actor in actor_dict:
            if actor in bacons[-1]:
                new_iter_bacon.update(actor_dict[actor])

        for bacon_set in bacons:
            new_iter_bacon -= bacon_set

        if 4724 in new_iter_bacon:
            new_iter_bacon.remove(4724)

        bacons.append(new_iter_bacon)



    return bacons[-1]

def breadth_first_search(data, starting_actor, actor_id):
    '''
    The main function of this program. Implements a BFS algorithm
    to the graph created by actor_dict. Some alterations were made
    from a traditional BFS python implementation:
        1. Rather than a list of paths, a set of paths was implemented
           to alleviate some computation stress from long_list.pop(0).
           The order in which each path was checked was irrelevant to
           this particular search. The hashable set structure greatly
           improved program run time on large jsons.
        2. Because python lists are not hashable, tuples were used to
           contain the path information within the queue set. They are
           converted back to lists at the end for optimized speed
        3. Some BFS searches will create a dictionary of parent nodes,
           but this was omitted in place of each path tuple containing
           that information. This removes the necessity of a backtrack
           function to loop over the parent node dictionary after its
           creation, speeding up the algorithm.
    '''

    actor_dict = build_actor_workset(data)
    queue = set()
    visited = set()
    start_path = (starting_actor,)
    queue.add(start_path)

    ### Traditional BFS:
    while len(queue) != 0:
        for path in queue.copy():
            queue.remove(path)
            working_node = path[-1]

            if working_node not in visited:
                visited.add(working_node)
                for adjacent in actor_dict[working_node]:
                    list_to_add = path
                    list_to_add += (adjacent,)
                    queue.add(list_to_add)

                    if adjacent == actor_id:
                        return list(list_to_add)


def get_bacon_path(data, actor_id):
    '''
    Calls breadth_first_search with Kevin Bacon's id as one of the arguments.
    Returns path to the specified node, None if path is empty.
    '''

    path = breadth_first_search(data, 4724, actor_id)
    return(path)

def get_path(data, actor_id_1, actor_id_2):
    '''
    Programatically identical to the above, but takes two arguments
    for starting and ending nodes as arguments.
    '''

    path = breadth_first_search(data, actor_id_1, actor_id_2)
    return(path)


def get_movie_path(data, actor_id_1, actor_id_2):
    '''
    Finds path with BFS, and then loops over the path and finds
    corresponding movie titles with adjacent actors in the cast.
    '''

    path = get_path(data, actor_id_1, actor_id_2)
    movie_dict = build_movie_casts(data)

    movie_path = []
    for i in range(len(path)-1):
        actor1 = path[i]
        actor2 = path[i+1]
        for movie in movie_dict:
            if actor1 in movie_dict[movie] and actor2 in movie_dict[movie]:
                movie_path.append(movie)

    return movie_path





if __name__ == '__main__':
    with open('resources/tiny.json') as f:
        smalldb = json.load(f)

    with open('resources/names.json') as f:
        namesdb = json.load(f)


    # additional code here will be run only when lab.py is invoked directly
    # (not when imported from test.py), so this is a good place to put code
    # used, for example, to generate the results for the online questions.
    pass
