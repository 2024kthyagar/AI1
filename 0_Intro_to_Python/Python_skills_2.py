import random


class Node:
    def __init__(self, value=0):
        self.value = value

    def a_method(self):
        print("this is a method")

    def b_method(self):
        print("all parent's methods inherited")


class TreeNode(Node):
    def __init__(self, value=0, left=None, right=None):
        super().__init__(value)
        self.left, self.right = left, right

    def a_method(self):
        print("method overriding happened")


n = Node()
print(n.value)
n.a_method()

root = TreeNode()
print(root.value, root.left, root.right)
root.a_method()  # was overridden
root.b_method()  # not overridden

root.left = TreeNode(value=random.randint(0, 9))
root.right = TreeNode(left=TreeNode(right=TreeNode(value=7)))


def display_preorder(t):
    if t is None:
        return
    print(t.value, end=' ')
    display_preorder(t.left)
    display_preorder(t.right)


print("Preorder:")
display_preorder(root)


def display_level(t, level):
    s = ""
    if t is None:
        return s
    s += display_level(t.right, level + 1)
    for k in range(level):
        s += '\t'
    s += str(t.value) + '\n'
    s += display_level(t.left, level + 1)
    return s


print("\n" * 2 + "Read left to right:\n")
print(display_level(root, 0))


def bfs(source, target):
    print(source, target)
