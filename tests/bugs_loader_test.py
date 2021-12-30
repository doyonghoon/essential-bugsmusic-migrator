import unittest
from bugs_loader import Loader

class TestBugsLoader(unittest.TestCase):
    def test_remove_commented_out_line(self):
        empty_line = Loader().remove_commented_out_line('// nothing to be remained')
        complete_url = Loader().remove_commented_out_line('https://music.bugs.co.kr/musicpd/albumview/37533 // comment should be dropped.')
        self.assertEqual(empty_line, '')
        self.assertEqual(complete_url, 'https://music.bugs.co.kr/musicpd/albumview/37533')

if __name__ == '__main__':
    unittest.main()
