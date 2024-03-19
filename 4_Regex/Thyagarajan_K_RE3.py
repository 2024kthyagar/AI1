import sys; args = sys.argv[1:]
idx = int(args[0]) - 50


myRegexLst = []

# 50: Match all strings where some letter appears twice in the same word.
myRegexLst.append(r'/(\w)+\w*\1\w*/i')
# 51: Match all strings where some letter appears four times in the same word.
myRegexLst.append(r'/\b(\w)+(\w*\1){3}\w*\b/i')
# 52: Match all non-empty binary strings with the same number of 01 substrings as 10 substrings.
# myRegexLst.append(r'/^[01]$|^([01])[01]*\1$/')
myRegexLst.append(r'/^([01])([01]*\1)?$/')
# 53: Match all six letter words containing the substring cat.
myRegexLst.append(r'/\b(?=\w*cat)\w{6}\b/i')
# 54: Match all 5 to 9 letter words containing both the substrings bri and ing.
myRegexLst.append(r'/\b(?=\w*bri)(?=\w*ing)\w{5,9}\b/i')
# 55: Match all six letter words not containing the substring cat.
myRegexLst.append(r'/\b(?!\w*cat)\w{6}\b/i')
# 56: Match all words with no repeated characters.
myRegexLst.append(r'/\b((\w)(?!\w*\2))+\b/i')
# 57: Match all binary strings not containing the forbidden substring 10011.
myRegexLst.append(r'/^(?![01]*10011)[01]*$/')
# 58: Match all words having two different adjacent vowels.
myRegexLst.append(r'/\w*([aeiou])(?!\1)[aeiou]\w*/i')
# 59: Match all binary strings containing neither 101 nor 111 as substrings.
myRegexLst.append(r'/^(0|1(?!.1))*$/')

print(myRegexLst)





if idx < len(myRegexLst):
    print(myRegexLst[idx])

# Karthik Thyagarajan, Period 5, 2024