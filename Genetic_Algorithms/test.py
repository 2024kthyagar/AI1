import time

currtime = time.time()
def test():
    count = 0
    while count < 100000000:

        count += 1
    pass
test()
print(time.time() - currtime)

currtime = time.time()

def test2():
    count = 0
    for i in range(100000000):
        count += 1
    pass
test2()
print(time.time() - currtime)
