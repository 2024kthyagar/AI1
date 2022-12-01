def generate_adjacents(current, word_list):
    adj_list = set()
    letters = "qwertyuiopasdfghjklzxcvbnm"
    for i in range(len(current)):
        for ladybug in letters:
            replacement = current[:i] + ladybug + current[i + 1:]
            if replacement in word_list and replacement != current:
                # print(replacement)
                adj_list.add(replacement)
    # print(adj_list)
    return adj_list


def make_graph(filename):
    # words_set = {}
    words_set = set()
    with open(filename) as infile:
        wordlist = set(infile.readlines())
        for line in wordlist:
            word = line.strip()
            words_set.add(word)
        #     words_set[word] = generate_adjacents(word, wordlist)
    return words_set


def BFS(start, end, words_set):
    # print(graph)
    explored = {start: None}
    queue = [start]
    while queue:
        node = queue.pop(0)
        if node == end:
            return display_path(end, explored)
        # for child in graph[node]:
        for child in generate_adjacents(node, words_set):
            # print(child)
            if child not in explored:
                queue.append(child)
                explored[child] = node
    return None


def DLS(start, end, words_set, limit):
    explored = {start: None}
    result = DLS_recur(start, end, words_set, explored, limit - 1)
    return display_path(end, result[0]) if result is not None else None


def DLS_recur(start, end, words_set, explored, limit):
    if start == end:
        return explored, ""
    if limit == 0:
        return explored, "cutoff"
    new_explored = {key: explored[key] for key in explored.keys()}
    cutoff_occurred = False
    # for child in graph[word]:
    for child in generate_adjacents(start, words_set):
        if child not in new_explored:
            new_explored[child] = start
            result = DLS_recur(child, end, words_set, new_explored, limit - 1)
            if result is not None and result[1] == "cutoff":
                cutoff_occurred = True
                continue
                # print(result[1])
            if result is not None:
                return result
    if cutoff_occurred:
        return explored, "cutoff"
    return None


def display_path(n, explored):
    path = []
    count = 0
    while n is not None:
        path.append(n)
        n = explored[n]
        count += 1
    path.reverse()
    return path, count


def main():
    word_set = make_graph('words_6_longer.txt')
    # print(graph)

    print("-----BFS-----\n")
    # Test BFS
    initial = input("Type the starting word: ")
    goal = input("Type the goal word: ")
    path_and_steps = (BFS(initial, goal, word_set))
    if path_and_steps is not None:
        print("Path:", path_and_steps[0])
        print("The number steps: {}".format(path_and_steps[1]))
    else:
        print("Solution not found.")

    print("\n-----DLS-----\n")

    # Test DLS
    initial = input("Type the starting word: ")
    goal = input("Type the goal word: ")
    limit = int(input("Type the limit: "))
    path_and_steps = (DLS(initial, goal, word_set, limit))
    if path_and_steps is not None:
        print("Path:", path_and_steps[0])
        print("steps within {} limit:".format(limit), path_and_steps[1])
        path_and_steps = (BFS(initial, goal, word_set))
        if path_and_steps is not None:
            print("Shortest Path:", path_and_steps[0])
            print("The number steps: {}".format(path_and_steps[1]))
    else:
        print("Solution not found in {} steps".format(limit))


if __name__ == "__main__":
    main()
