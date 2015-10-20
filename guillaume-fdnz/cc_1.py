# coding: utf-8
import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    result = ""
    for i in range(n): 
        result += string
    return result

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
  upperBound = min(len(nums),4)
  if 9 in nums[0:upperBound]:
      return True
  else:
      return False



# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
#Since the question is ambiguous, we'll consider two cases
#One seems closer to the meaning of the question, the other to the test values
#How many times the last 2 chars are in (substrings of string - itself) ?
def last2(string):
    subStringDict = {}
    subStringToLookFor = string[-2:]
    count = 0
    for i in range(len(string)-2):
        subString = string[i:i+2]
        if subString == subStringToLookFor:
            count += 1
    return count #countMax[0][1]

#How many times any 2-chars substring of string occurs in any substring of (string minus the last 2 chars)? return the maximum
def last2bis(string):
    subStringDict = {}
    for i in range(len(string)-2):
        subString = string[i:i+2]
        if subString in subStringDict:
            subStringDict[subString] += 1
        else:
            subStringDict[subString] = 1
    countMax = sorted(subStringDict.items(), key=lambda (k,v): (v,k), reverse=True)
    return countMax[0][1]

#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words(array):
    return map((lambda word: len(word)),array)

#write fizbuzz programm
def fizbuzz():
  for i in xrange(1, 101):
        if i % 15 == 0:
            print "FizzBuzz"
        elif i % 3 == 0:
            print "Fizz"
        elif i % 5 == 0:
            print "Buzz"
        else:
            print i
  return

#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
  digitList = []
  for char in str(number): digitList.append(int(char))
  return digitList

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking off the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):
  words = text.split()
  pigLatinSentence = ""
  for word in words: pigLatinSentence = pigLatinSentence + word[1:] + word[0].lower() + "ay "
  return pigLatinSentence[:-1].capitalize()

# Here's our "unit tests".
class Lesson1Tests(unittest.TestCase):

    def testArrayFront9(self):
        self.assertEqual(array_front9([1, 2, 9, 3, 4]) , True)
        self.assertEqual(array_front9([1, 2, 3, 4, 9]) , False)
        self.assertEqual(array_front9([1, 2, 3, 4, 5]) , False)

    def testStringTimes(self):
        self.assertEqual(string_times('Hel', 2),'HelHel' )
        self.assertEqual(string_times('Toto', 1),'Toto' )
        self.assertEqual(string_times('P', 4),'PPPP' )

    def testLast2(self):
        self.assertEqual(last2('hixxhi') , 1)
        self.assertEqual(last2('xaxxaxaxx') , 1)
        self.assertEqual(last2('axxxaaxx') , 2)

    def testLengthWord(self):
        self.assertEqual(length_words(['hello','toto']) , [5,4])
        self.assertEqual(length_words(['s','ss','59fk','flkj3']) , [1,2,4,5])

    def testNumber2Digits(self):
        self.assertEqual(number2digits(8849) , [8,8,4,9])
        self.assertEqual(number2digits(4985098) , [4,9,8,5,0,9,8])

    def testPigLatin(self):
        self.assertEqual(pigLatin("The quick brown fox") , "Hetay uickqay rownbay oxfay")



def main():
    unittest.main()

if __name__ == '__main__':
    main()

