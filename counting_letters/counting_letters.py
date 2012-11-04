import collections
import string

# Use sets for fast check
VOWELS = set(['a', 'A', 'e', 'E', 'i', 'I', 'o', 'O', 'u', 'U'])
CONSONANTS = set(string.ascii_letters)

def count_letters(text):
        """ Returns a dict counts for each vowel and aggreate count
        of all consonatns"""
        counter = collections.defaultdict(int)
        for letter in text:
                if letter in VOWELS:
                        counter[letter.lower()] += 1
                elif letter in CONSONANTS:
                        counter['consonants'] += 1
                else:
                        # skip the character
                        pass
        return counter


def tests():
        def equals_dicts(a, b):
                return set(a.items()) == set(b.items())

        def test_ok(text, counts):
                assert equals_dicts(count_letters(text), counts)

        def test_ko(text, counts):
                assert not equals_dicts(count_letters(text), counts)

        # test example
        test_ok('This is the string', dict(e=1, i=3, consonants=11))

        # test example with non english characters
        test_ok('This is%$!" the string', dict(e=1, i=3, consonants=11))

        # test lower/upper case
        test_ok('aAeEiIoOuUbcDF', dict(a=2, e=2, i=2, o=2, u=2, consonants=4))

        # test corner cases
        test_ok('', dict())

        try:
                test_ok(None, dict())
                # You normally prefer to raise an exception if None is passed
                # so is easier to spot possible errors. Unless you explicity
                # want to support it
                assert False
        except TypeError:
                pass

        # test unicode
        test_ok(u'My name is \xd3scar \u6c49\u8bed/\u6f22\u8a9e',
                {'consonants': 8, u'a': 2, u'e': 1, u'i': 1})

        print "done."

if __name__ == '__main__':
        tests()
