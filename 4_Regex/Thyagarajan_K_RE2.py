import sys; args = sys.argv[1:]
idx = int(args[0]) - 40

myRegexLst = []

# An Othello board is any string of length 64 made up of only the characters in "xX.Oo".
# An Othello edge is any string of length 8 made up of only the characters in "xX.Oo".

# Q40 - Write a regular expression that will match on an Othello board represented as a string.
myRegexLst.append(r'/^[xo.]{64}$/i')

# Q41 - Given a string of length 8, determine whether it could represent an Othello edge with exactly one hole.
myRegexLst.append(r'/^[xo]*\.[xo]*$/i')

# Q42 - Given an Othello edge as a string, determine whether there is a hole such that if X plays to the hole
# (assuming it could), it will be connected to one of the corners through X tokens. Specifically, this means that one
# of the ends must be a hole, or starting from an end there is a sequence of at least one x follow immediately by a
# sequence (possibly empty) of o, immediately followed by a hole.
myRegexLst.append(r'/^(x+o*)?\.|\.+(o*x+$)?$/i')

# XOOX....
# ..OO....
# XX.....O
# .XOOOO..
# XOXOOO.O
# XXXXXXX.

# Q43: Match on all strings of odd length
myRegexLst.append(r'/^.(..)*$/s')

# Q44: Match on all odd length binary strings starting with 0, and on even length binary strings starting with 1
myRegexLst.append(r'/^0([01]{2})*$|^1([01]{2})*[01]$/')

# Q45: Match all words having two adjacent vowels that differ
myRegexLst.append(r'/\w*(a[eiou]|e[aiou]|i[aeou]|o[aeiu]|u[aeio])\w*/i')
# myRegexLst.append(r'/\w*[aeiou][^\1bcdfghjklmnpqrstvqxyz]\w*/')
# myRegexLst.append(r'/\w*([aeiou])(?!\1)[aeiou]\w*/i')

# Q46: Match on all binary strings with DON'T contain the substring 110
myRegexLst.append(r'/^(1?0)*1*$/')

# Q47: Match on all non-empty strings over the alphabet {a,b,c} that contain at most one a
myRegexLst.append(r'/^[bc]+$|^[bc]*a[bc]*$/')

# Q48: Match on all non-empty strings over the alphabet {a,b,c} that contain an even number of a's
myRegexLst.append(r'/^([bc]+|(a[bc]*a))+$/')

# Q49: Match on all positive, even, base 3 integer strings
# myRegexLst.append(r'/^(2[02]*|(1[02]*){2})+$/')
myRegexLst.append(r'/(2|1[02]*1)[02]*)+/')

if idx < len(myRegexLst):
    print(myRegexLst[idx])

# Karthik Thyagarajan, Period 5, 2024