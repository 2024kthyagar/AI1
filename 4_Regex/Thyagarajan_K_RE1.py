import sys; args = sys.argv[1:]
idx = int(args[0]) - 30


myRegexLst = []
# 30: Determine whether a string is either 0, 100, or 101.
myRegexLst.append(r'/^0$|^10[01]$/')
# 31: Determine whether a given string is a binary string (ie. composed only of  0 and 1 characters).
myRegexLst.append(r'/^[01]*$/')
# 32: Given a binary integer string, what regular expression determines whether it is even?
# myRegexLst.append(r'/^[01]*0$/')
myRegexLst.append(r'/0$/')
# 33: What is a regular expression to determine (ie. match) those words in a text that have at least two vowels?
myRegexLst.append(r'/\w*[aeiou]\w*[aeiou]\w*/i')
# 34: Given a string, determine whether it is a non-negative, even binary integer string.
myRegexLst.append(r'/^0$|^1[01]*0$/')
# 35: Determine whether a given string is a binary string containing 110 as a substring.
myRegexLst.append(r'/^[01]*110[01]*$/')
# 36: Match on all strings of length at least two, but at most four.
myRegexLst.append(r'/^.{2,4}$/s')
# 37: social security number
myRegexLst.append(r'/^\d{3} *-? *\d\d *-? *\d{4}$/')
# 38: Determine a regular expression to help you find the first word of each line of text with a  d  in it: Match through the end of the first word with a d on each line that has a d.
myRegexLst.append(r'/^.*?d\w*/mi')
# 39: Determine whether a string is a binary string that has the same number of 01 substrings as 10 substrings.
myRegexLst.append(r'/^[01]?$|^0[01]*0$|^1[01]*1$/')

print(myRegexLst)





if idx < len(myRegexLst):
    print(myRegexLst[idx])

# Karthik Thyagarajan, Period 5, 2024