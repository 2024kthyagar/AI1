def gini_index(groups, classes):
    # count all samples at split point
    n_instances = 0
    for group in groups:
        n_instances += sum([len(row) for row in group])
    # sum weighted Gini index for each group
    gini = 0.0
    for group in groups:
        size = sum(len(row) for row in group)
        # avoid divide by zero
        if size == 0:
            continue
        score = 0.0
        # score the group based on the score for each class
        # print(group)
        for class_val in classes:
            # print(sum(row.count(class_val) for row in group))
            p = sum(row.count(class_val) for row in group) / size
            # print(p)
            score += p * p
        print(score)
        # weight the group score by its relative size
        print(size, n_instances, size/n_instances)
        gini += (1.0 - score) * (size / n_instances)
    return gini


# test Gini values
print("GINI 1: " + str(gini_index([[[1, 1], [0, 0]], [[1, 1], [0, 0]]], [0, 1])))
print(gini_index([[[1, 0], [1, 0]], [[1, 1], [1, 1]]], [0, 1]))
