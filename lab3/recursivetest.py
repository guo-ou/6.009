


def n_dimensional_array(dimensions):
    depth = 0
    return recursiveArray(dimensions, depth)

def recursiveArray(dimensions, depth):
    if depth == len(dimensions) - 1:
        curdim = dimensions[depth]
        array = []
        for index in range(curdim):
            array.append(0)

    else:
        curdim = dimensions[depth]
        array = []
        for index in range(curdim):
            array.append(recursiveArray(dimensions, depth + 1))
    return array

print(n_dimensional_array([2,4,2])[0])
