import unittest


# Given a string and a non-negative int n, return a larger string
# that is n copies of the original string.

def string_times(string, n):
    return string * n

# Given an array of ints, return True if one of the first 4 elements
# in the array is a 9. The array length may be less than 4.


def array_front9(nums):
    return


# Given a string, return the count of the number of times
# that a substring length 2 appears  in the string and also as
# the last 2 chars of the string, so "hixxxhi" yields 1 (we won't count the
# end substring).


def last2(string):
    return


# Write a program that maps a list of words into a list of
# integers representing the lengths of the correponding words.
def length_words(array):
    return

# write fizbuzz programm


def fizbuzz():
    for i in range(1, 101):
        if i/15. == i//15:
            print 'fizbuzz'
        elif i/5. == i//5:
            print 'buzz'
        elif i/3. == i//3:
            print 'fiz'
        else:
            print str(i)
    return

# Write a function that takes a number and returns a list of its digits.


def number2digits(number):
    s = str(i)
    return [c for c in str]

# Write function that translates a text to Pig Latin and back.
# English is translated to Pig Latin by taking the first letter of every word,
# moving it to the end of the word and adding 'ay'


def pigLatin(text):
    return ' '.join([word[1:] + word[0] + 'ay' for word in text.split(' ')])

# Here's our "unit tests".


class Lesson1Tests(unittest.TestCase):

    def testArrayFront9(self):
        self.assertEqual(array_front9([1, 2, 9, 3, 4]), True)
        self.assertEqual(array_front9([1, 2, 3, 4, 9]), False)
        self.assertEqual(array_front9([1, 2, 3, 4, 5]), False)

    def testStringTimes(self):
        self.assertEqual(string_times('Hel', 2), 'HelHel')
        self.assertEqual(string_times('Toto', 1), 'Toto')
        self.assertEqual(string_times('P', 4), 'PPPP')

    def testLast2(self):
        self.assertEqual(last2('hixxhi'), 1)
        self.assertEqual(last2('xaxxaxaxx'), 1)
        self.assertEqual(last2('axxxaaxx'), 2)

    def testLengthWord(self):
        self.assertEqual(length_words(['hello', 'toto']), [5, 4])
        self.assertEqual(length_words(['s', 'ss', '59fk', 'flkj3']),
                         [1, 2, 4, 5])

    def testNumber2Digits(self):
        self.assertEqual(number2digits(8849), [8, 8, 4, 9])
        self.assertEqual(number2digits(4985098), [4, 9, 8, 5, 0, 9, 8])

    def testPigLatin(self):
        self.assertEqual(pigLatin("The quick brown fox"),
                         "Hetay uickqay rownbay oxfay")


def main():
    fizbuzz()
    # unittest.main()

if __name__ == '__main__':
    main()
