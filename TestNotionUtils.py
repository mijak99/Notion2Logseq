import unittest
from NotionUtils import *

class TestGetMarkdownLinks(unittest.TestCase):

    # New tests
    
    def test_empty_string(self):
        test_md = ''
        links = get_all_markdown_links(test_md)
        self.assertEqual(len(links), 0)

    def test_no_links_with_brackets(self):
        test_md = '[Text] No links'
        links = get_all_markdown_links(test_md)
        print(links)
        self.assertEqual(len(links), 0)

    def test_invalid_url(self):
        test_md = '[Text](invalidurl)'
        links = get_all_markdown_links(test_md)
        self.assertEqual(len(links), 1)  #should not care about url content


class TestReplaceNotionTags(unittest.TestCase):

    def test_replace_notion_tags(self):
        content = "# My Header\n\ntags: a, spaced tag\nCreated Date: 20 20 20\n\n Some text\n## Subheader"
        expected = "notion-heading:: My Header\ntags:: a, spaced tag\nCreated-Date:: 20 20 20\n\n Some text\n## Subheader"
        result, count = replace_notion_tags(content)
        self.assertEqual(result, expected)
        self.assertEqual(count, 3)




    
if __name__ == '__main__':
    unittest.main()
