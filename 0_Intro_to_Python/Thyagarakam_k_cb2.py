# Karthik Thyagarajan
# Aug 28, 2022

# Warmup 2

def string_times(str, n):
    return str * n


def front_times(str, n):
    return n * str[:3]


def string_bits(str):
    return str[::2]


def string_splosion(str):
    return "".join([str[:i + 1] for i in range(len(str))])


def last2(str):
    return sum((str[i] + v) == str[-2:] for i, v in enumerate(str[1:-1]))


def array_count9(nums):
    return nums.count(9)


def array_front9(nums):
    return 9 in nums[:4]


def array123(nums):
    return any(nums[i:i + 3] == [1, 2, 3] for i in range(len(nums) - 2))


def string_match(a, b):
    return sum(a[i:i + 2] == b[i:i + 2] for i in range(len(a) - 1))


# Logic 2

def make_bricks(small, big, goal):
    return goal - 5 * big <= small and goal % 5 <= small


def lone_sum(a, b, c):
    return sum(v for v in [a, b, c] if [a, b, c].count(v) == 1)


def lucky_sum(a, b, c):
    return a * (a != 13) + b * (13 not in [a, b]) + c * (13 not in [a, b, c])


def no_teen_sum(a, b, c):
    return sum(v * (not (12 < v < 15 or 16 < v < 20)) for v in [a, b, c])


def round_sum(a, b, c):
    return sum((v + 5) // 10 * 10 for v in [a, b, c])


def close_far(a, b, c):
    return sum(v in [0, 1] for v in [abs(a - b), abs(a - c), abs(b - c)]) == 1


def make_chocolate(small, big, goal):
    return ((n := (goal % 5 + 5 * max(0, goal // 5 - big))) + 1) * (n <= small) - 1


# String 2

def double_char(str):
    return "".join(i * 2 for i in str)


def count_hi(str):
    return str.count('hi')


def cat_dog(str):
    return str.count('cat') == str.count('dog')


def count_code(str):
    return sum(str[i:i + 2] == "co" and str[i + 3] == 'e' for i in range(len(str) - 3))


def end_other(a, b):
    return a.lower() == b[0 - len(a):].lower() or b.lower() == a[0 - len(b):].lower()


def xyz_there(str):
    return str.count("xyz") > str.count(".xyz")


# List 2

def count_evens(nums):
    return sum(v % 2 == 0 for v in nums)


def big_diff(nums):
    return max(nums) - min(nums)


def centered_average(nums):
    return sum(sorted(nums)[1:-1]) // (len(nums) - 2)


def sum13(nums):
    return sum(nums[i] for i in range(len(nums)) if nums[i] != 13 and (nums[i - 1] != 13 or i - 1 == -1))


def sum67(nums):
    return sum67(nums[:(x := nums.index(6))] + nums[nums.index(7, x) + 1:]) if 6 in nums else sum(nums)


def has22(nums):
    return any(a == b == 2 for a, b in zip(nums, nums[1:]))


# print(has22([2, 2, 4, 3, 7, 8, 9, 7, 7]))

# Karthik Thyagarajan, 5, 2024
