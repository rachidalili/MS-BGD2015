import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    if(n == 0):
        return ""
    else:
        return string + string_times(string, n-1)

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.
def array_front9(nums):
    for i in range(min(len(nums), 4)):
        if(nums[i] == 9):
            return True
    return False


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the end substring).
def last2(string):
    couples = {}
    n = len(string)
    if(n < 2):
        return 0
    for i in range(len(string) - 1):
        couple = string[i:i+2]
        if couple in couples.keys():
            couples[couple] += 1
        else:
            couples[couple] = 0
    return couples[string[n-2:n]]


#Write a program that maps a list of words into a list of
#integers representing the lengths of the correponding words.
def length_words(array):
    return [len(w) for w in array]

#write fizbuzz programm
def fizbuzz():
    for i in range(100):
        add = ""
        if(i % 3 == 0):
            add += "Fizz"
        if(i % 5 == 0):
            add += "Buzz"
        print(str(i) + " " + add)
    return

#Write a function that takes a number and returns a list of its digits.
def number2digits(number):
    return [int(c) for c in str(number)]

#Write function that translates a text to Pig Latin and back.
#English is translated to Pig Latin by taking the first letter of every word,
#moving it to the end of the word and adding 'ay'
def pigLatin(text):
    def pigWord(word):
        if(len(word)<2):
            return word + 'ay'
        firstLetter = word[0]
        secondLetter = word[1]
        if(firstLetter.isupper()):
            secondLetter = secondLetter.upper()
            firstLetter = firstLetter.lower()
        return secondLetter + word[2:len(word)] + firstLetter + 'ay'
    solution = ''
    for word in text.split(' '):
        solution += pigWord(word) + ' '
    return solution[:-1] #delete the last space

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

