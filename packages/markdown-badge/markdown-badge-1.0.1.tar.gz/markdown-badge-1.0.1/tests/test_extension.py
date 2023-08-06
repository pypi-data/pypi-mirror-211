import markdown
import unittest


class TestBadge(unittest.TestCase):
    """ Test Badge Extension. """

    def setUp(self):
        self.md = markdown.Markdown(extensions=['badge'])

    def testRE(self):
        RE = self.md.inlinePatterns['badge'].compiled_re
        tests = [
            ('{{ note }}', ('note', None)),
            ('{{ note "Please Note" }}', ('note', 'Please Note')),
            ('{{ note "" }}', ('note', '')),
        ]
        for test, expected in tests:
            self.assertEqual(RE.match(test).groups(), expected)