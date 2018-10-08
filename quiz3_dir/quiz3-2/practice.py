def simple_paths(graph, start, end):
    f_node = graph[start]
    starting_path = (start, )
    out_set = set()

    def helper(node, cur_path):
        print(node)
        print(cur_path)
        for sub_node in node:
            print (sub_node)


            if sub_node == end:
                out_set.add(cur_path + (sub_node,))


            else:
                if sub_node in cur_path:
                    continue
                helper(graph[sub_node], cur_path + (sub_node,))

    helper(f_node, starting_path)

    print(out_set)


graph1 = graph1 = {'a': {'b', 'c'},
            'b': {'a', 'b', 'f'},
            'c': {'c'},
            'd': {'e', 'd', 'c'},
            'e': {},
            'f': {'a'},
}


simple_paths(graph1, "b", "c")
