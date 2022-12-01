import random


class HeapPriorityQueue():
    def __init__(self):
        self.queue = ['dummy']
        self.current = 1

    def next(self):
        if self.current >= len(self.queue):
            raise StopIteration

        out = self.queue[self.current]
        self.current += 1

        return out

    def __iter__(self):
        return self

    __next__ = next

    def isEmpty(self):
        return len(self.queue) == 1

    def swap(self, a, b):
        self.queue[a], self.queue[b] = self.queue[b], self.queue[a]

    def remove(self, index):
        val = self.queue[index]
        del self.queue[index]
        self.reheap()
        return val

    def pop(self):
        val = self.queue[1]
        self.swap(1, -1)
        self.queue.pop(-1)
        self.heapDown(1, len(self.queue)-1)
        return val

    def push(self, value):
        self.queue.append(value)
        self.heapUp(len(self.queue) - 1)

    def peek(self):
        return self.queue[1]

    def reheap(self):
        for k in range(len(self.queue) // 2, 0, -1):
            self.heapDown(k, len(self.queue) - 1)

    def heapDown(self, k, size):
        left, right = 2 * k, 2 * k + 1

        if left == size and self.queue[k] > self.queue[size]:
            self.swap(k, size)

        elif right <= size:
            min_child = left if self.queue[left] <= self.queue[right] else right

            if self.queue[k] > self.queue[min_child]:
                self.swap(k, min_child)
                self.heapDown(min_child, size)

    def heapUp(self, k):
        parent = k // 2 if k > 1 else k
        if self.queue[k] < self.queue[parent]:
            self.swap(k, parent)
            self.heapUp(parent)

    def isEmpty(self):
        return len(self.queue) <= 1


def isHeap(queue, k):
    return all(i <= 2 * i and i <= 2 * i + 1 for i in range(k, len(queue) // 2 - 1))


def main():
    pq = HeapPriorityQueue()  # create a HeapPriorityQueue object

    print("Check if dummy 0 is still dummy:", pq.queue[0])

    # assign random integers into the pq
    for i in range(20):
        t = random.randint(10, 99)
        print(t, end=" ")
        pq.push(t)

    print()

    # print the pq which is a min-heap
    for x in pq:
        print(x, end=" ")
    print()

    # remove test
    print("Index 4 is removed:", pq.remove(4))

    # check if pq is a min-heap
    for x in pq:
        print(x, end=" ")
    print("\nIs a min-heap?", isHeap(pq.queue, 1))

    temp = []
    while not pq.isEmpty():
        temp.append(pq.pop())
        print(temp[-1], end=" ")

    print("\nIn ascending order?", temp == sorted(temp))


# if __name__ == '__main__':
#     main()
