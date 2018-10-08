# Representation of a gas:
#
# gas_3 = { "width": 3,
#           "height": 4,
#           "state": [ ["w"], ["w"], ["w"],
#                      ["w"], ["r","l"], ["w"],
#                      ["w"], [ ], ["w"],
#                      ["w"], ["w","d"], ["w"] ] }

def init_state(gas):
    '''
    Initializes a properly sized gas state devoid of particles.
    It returns an array of cells only containing walls -- particles
    to be added in resolve_collisions
    '''
    new_state = [] ##initialize empty state for new gas
    for dim in range(gas["width"]*gas["height"]):
        new_state.append([])
    for i in range(len(gas["state"])):
        cell = gas["state"][i]
        if "w" in cell:
            new_state[i].append("w")
    return new_state

def resolve_collisions(state, gas):
    '''
    This function takes a gas and its state and resolves all wall-particle collisions
    and two-particle collisions. It returns the gas state EXCLUDING the
    movement of the particles, i.e. no particle changes cells, simply its
    orientation is determined here by its collision status.
    '''
    new_state = init_state(gas)
    for i in range(len(state)):
        cell = state[i]

        ## Check into which category the cell falls
        double_gas = len(cell) == 2 and "w" not in cell
        collidable = (("r" in cell and "l" in cell) or ("u" in cell and "d" in cell)) and double_gas
        wall_gas = len(cell) >=2 and "w" in cell
        others = (len(cell) !=2) or not (("r" in cell and "l" in cell) or ("u" in cell and "d" in cell))

        ## TWO-PARTICLE COLLISIONS:
        if collidable:
            if "r" in cell: #or "l" but the statement is redundant as collidable implies both
                new_state[i] = ["u","d"]
            elif "u" in cell: #or "d" as per above comment
                new_state[i] = ["l","r"]

        ## WALL COLLISIONS:
        elif wall_gas:
            if "l" in cell:
                new_state[i].append("r")
            if "r" in cell:
                new_state[i].append("l")
            if "u" in cell:
                new_state[i].append("d")
            if "d" in cell:
                new_state[i].append("u")

        ## THREE OR FOUR PARTICLE CELLS
        elif others:
            new_state[i] = cell

    return new_state

def progress_particles(state, gas):
    '''
    This function takes the same gas and a state which has
    completed its collision resolution and returns the new
    state with progressed particles. It checks which
    direction the particle should move in the current step,
    and properly fills an empty cell.
    '''
    new_state = init_state(gas)
    for i in range(len(state)):
        cell = state[i]

        try:
            ## because these are instantiated here,
            ## they may pop errors for cells near
            ## the beginning and end of the gas states
            right = new_state[i+1]
            left = new_state[i-1]
            above = new_state[i-gas["width"]]
            below = new_state[i+gas["width"]]
        except:
            pass
        ## place all moving particles in the correct location
        if "r" in cell:
            right.append("r")
        if "l" in cell:
            left.append("l")
        if "u" in cell:
            above.append("u")
        if "d" in cell:
            below.append("d")
    return new_state

def step(gas):
    '''
    Instantiates the nth gas state, and executes both resolve_collisions
    and progress_particles. It then overwrites the gas state with
    the (n+1)th gas state, and returns the whole gas object.
    '''
    state = gas["state"]
    collided_state = resolve_collisions(state, gas)
    progressed_state = progress_particles(collided_state, gas)
    gas["state"] = progressed_state

    return gas
