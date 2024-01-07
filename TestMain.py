import unittest
from NotionUtils import get_all_markdown_links

class TestGetMarkdownLinks(unittest.TestCase):

    def test_basic(self):
        # Test extracting links from sample markdown
        test_md = '[Text](http://example.com)'
        links = get_all_markdown_links(test_md)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0][0], '[Text](http://example.com)')

    def test_multiple_links(self):
        # Test extracting multiple links
        test_md = '[Text1](http://example1.com)\n[Text2](http://example2.com)'
        links = get_all_markdown_links(test_md)
        self.assertEqual(len(links), 2)

    def test_no_links(self):
        # Test no links
        test_md = 'No links'
        links = get_all_markdown_links(test_md)
        self.assertEqual(len(links), 0)

    def test_url_links(self):
        # Test links with url encoding
        test_md = '[Text](http%3A%2F%2Fexample.com)'
        links = get_all_markdown_links(test_md)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0][2], 'http://example.com')

    def test_tricky_brackets(self):
        # Test links with url encoding
        test_md = '[x] [Text](http://example.com/page%281%29)\n[Text2](http://example.com/page)'
        links = get_all_markdown_links(test_md)
        self.assertEqual(len(links), 2)
        self.assertEqual(links[0][1], 'Text')
        self.assertEqual(links[1][1], 'Text2')

    def test_long_names(self):
        # Test links with url encoding
        test_md = '[S2E14 Right at the start, eh?](http://example.com/page)'
        links = get_all_markdown_links(test_md)
        self.assertEqual(len(links), 1)
        self.assertEqual(links[0][1], 'S2E14 Right at the start, eh?')
        



if __name__ == '__main__':
    unittest.main()
