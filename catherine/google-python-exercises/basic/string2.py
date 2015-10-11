#!/usr/bin/python2.4 -tt
# Copyright 2010 Google Inc.
# Licensed under the Apache License, Version 2.0
# http://www.apache.org/licenses/LICENSE-2.0

# Google's Python Class
# http://code.google.com/edu/languages/google-python-class/

# Additional basic string exercises

import re

# D. verbing
# Given a string, if its length is at least 3,
# add 'ing' to its end.
# Unless it already ends in 'ing', in which case
# add 'ly' instead.
# If the string length is less than 3, leave it unchanged.
# Return the resulting string.
def verbing(s):
    result = s
    if len(s) > 2:
        if s[len(s)-3:] == "ing":
            result += "ly"
        else:
            result += "ing"
    return result


# E. not_bad
# Given a string, find the first appearance of the
# substring 'not' and 'bad'. If the 'bad' follows
# the 'not', replace the whole 'not'...'bad' substring
# with 'good'.
# Return the resulting string.
# So 'This dinner is not that bad!' yields:
# This dinner is good!
def not_bad(s):
    result = ""
    lpat = re.split('(\W+)', s)
    jumpto = 0
    for i in range(0, len(lpat)):
        if jumpto != 0 and i < jumpto:
            continue
        else:
            jumpto = 0
        if lpat[i] != 'not':
            result += lpat[i]
        else:
            if lpat[i] == 'not':
                erasenot = False
                for j in range(i+1, len(lpat)):
                    if lpat[j] == 'not':
                        break
                    else:
                        if lpat[j] == 'bad':
                            result += 'good'
                            jumpto = j+1
                            erasenot = True
                            break
                if not erasenot:
                    result += lpat[i]
    return result


# F. front_back
# Consider dividing a string into two halves.
# If the length is even, the front and back halves are the same length.
# If the length is odd, we'll say that the extra char goes in the front half.
# e.g. 'abcde', the front half is 'abc', the back half 'de'.
# Given 2 strings, a and b, return a string of the form
#  a-front + b-front + a-back + b-back
def front_back(a, b):
    result = ""
    splita = len(a)/2 + (len(a) % 2)
    splitb = len(b)/2 + (len(b) % 2)
    afront = a[0:splita]
    aback = a[splita:]
    bfront = b[0:splitb]
    bback = b[splitb:]
    result = afront+bfront+aback+bback
    return result


# Simple provided test() function used in main() to print
# what each function returns vs. what it's supposed to return.
def test(got, expected):
  if got == expected:
    prefix = ' OK '
  else:
    prefix = '  X '
  print '%s got: %s expected: %s' % (prefix, repr(got), repr(expected))


# main() calls the above functions with interesting inputs,
# using the above test() to check if the result is correct or not.
def main():
  print 'verbing'
  test(verbing('hail'), 'hailing')
  test(verbing('swiming'), 'swimingly')
  test(verbing('do'), 'do')

  print
  print 'not_bad'
  test(not_bad('This movie is not so bad'), 'This movie is good')
  test(not_bad('This dinner is not that bad!'), 'This dinner is good!')
  test(not_bad('This tea is not hot'), 'This tea is not hot')
  test(not_bad("It's bad yet not"), "It's bad yet not")

  print
  print 'front_back'
  test(front_back('abcd', 'xy'), 'abxcdy')
  test(front_back('abcde', 'xyz'), 'abcxydez')
  test(front_back('Kitten', 'Donut'), 'KitDontenut')

if __name__ == '__main__':
  main()
