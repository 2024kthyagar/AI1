# Karthik Thyagarajan
# Aug 24, 2022

# Warmup 1

def sleep_in(weekday, vacation):
    return not weekday or vacation


def monkey_trouble(a_smile, b_smile):
    return a_smile == b_smile


def sum_double(a, b):
    return a + b if a != b else 2 * (a + b)


def diff21(n):
    return abs(n - 21) * ((n > 21) + 1)


def parrot_trouble(talking, hour):
    return talking and (hour < 7 or hour > 20)


def makes10(a, b):
    return a == 10 or b == 10 or a + b == 10


def near_hundred(n):
    return abs(n - 100) <= 10 or abs(n - 200) <= 10


def pos_neg(a, b, negative):
    return (a < 0 and b < 0) if negative else (a > 0 and b < 0) or (a < 0 and b > 0)


# String 1

def hello_name(name):
    return "Hello " + name + "!"


def make_abba(a, b):
    return a + b + b + a


def make_tags(tag, word):
    return '<' + tag + '>' + word + '</' + tag + '>'


def make_out_word(out, word):
    return out[:len(out) // 2] + word + out[len(out) // 2:]


def extra_end(str):
    return (str[-2:]) * 3


def first_two(str):
    return str[:2]


def first_half(str):
    return str[:len(str) // 2]


def without_end(str):
    return str[1:-1]


# List 1

def first_last6(nums):
    return nums[0] == 6 or nums[0] == "6" or nums[-1] == 6 or nums[-1] == "6"


def same_first_last(nums):
    return bool(nums) and nums[0] == nums[-1]


def make_pi(n):
    return [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5, 8, 9, 7][:n]


def common_end(a, b):
    return a[0] == b[0] or a[-1] == b[-1]


def sum3(nums):
    return sum(nums)


def rotate_left3(nums):
    return nums[1:] + [nums[0]] if len(nums)>1 else nums


def reverse3(nums):
    return nums[::-1]


def max_end3(nums):
    return len(nums) * [max(nums[0], nums[-1])]


# Logic 1

def cigar_party(cigars, is_weekend):
    return cigars >= 40 if is_weekend else 40 <= cigars <= 60


def date_fashion(you, date):
    return 0 if you <= 2 or date <= 2 else (2 if you >= 8 or date >= 8 else 1)


def squirrel_play(temp, is_summer):
    return 60 <= temp <= 100 if is_summer else 60 <= temp <= 90


def caught_speeding(speed, is_birthday):
    return 0 if speed <= 60 + 5 * is_birthday else 1 if 60 + 5 * is_birthday < speed <= 80 + 5 * is_birthday else 2


def sorta_sum(a, b):
    return 20 if 10 <= a + b <= 19 else a + b


def alarm_clock(day, vacation):
    return ("10:00" if 0 < day < 6 else "off") if vacation else ("7:00" if 0 < day < 6 else "10:00")


def love6(a, b):
    return 6 in [a, b] or a + b == 6 or abs(a - b) == 6


def in1to10(n, outside_mode):
    return n <= 1 or n >= 10 if outside_mode else 1 <= n <= 10
