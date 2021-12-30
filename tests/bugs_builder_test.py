import unittest
from bugs_builder import Builder

class TestBugsBuilder(unittest.TestCase):
    def test_delete_hangul(self):
        builder = Builder()
        suffix = builder.delete_hangul('this includes hangul (한글)')
        missing_parenthesis = builder.delete_hangul('missing parenthesis w/ 한글')
        prefix = builder.delete_hangul('(음악 )this includes music')
        middle = builder.delete_hangul('part of (음악 ) string with hangul')
        missing_pmiddle = builder.delete_hangul('part of 음악  string with hangul')

        self.assertEqual(suffix, 'this includes hangul')
        self.assertEqual(missing_parenthesis, 'missing parenthesis w/ 한글')
        self.assertEqual(prefix, 'this includes music')
        self.assertEqual(middle, 'part of string with hangul')
        self.assertEqual(missing_pmiddle, 'part of 음악  string with hangul')

if __name__ == '__main__':
    unittest.main()
