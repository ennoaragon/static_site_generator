import unittest

from markdown_to_blocks import BlockType, markdown_to_blocks, block_to_block_type, markdown_to_html_node


class TestMarkDown(unittest.TestCase):

    def test_markdown_block_code(self):

        case_1 = '```\nprint("This starts with backticks and a newline")\n```'

        case_2 = '```python print("This has a language tag, so it should fail")```'

        case_3 = "```\nSingle line content\n```"


        self.assertEqual(block_to_block_type(case_1), BlockType.CODE)
        self.assertNotEqual(block_to_block_type(case_2), BlockType.CODE)
        self.assertEqual(block_to_block_type(case_3), BlockType.CODE)


    def test_markdown_block_heading(self):

        case_1 = "# Level 1"
        case_2 = "###### Level 6"
        case_3 = "####### Too many"
        case_4 = "#NoSpace"

        self.assertEqual(block_to_block_type(case_1), BlockType.HEADING)
        self.assertEqual(block_to_block_type(case_2), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type(case_3), BlockType.HEADING)
        self.assertNotEqual(block_to_block_type(case_4), BlockType.HEADING)

    def test_markdown_block_quote(self):
        # Case 1: Standard quote with spaces
        case_1 = "> This is a quote "

        # Case 2: Quote without spaces (Allowed per your rules)
        case_2 = ">No space here\n>Still a quote"

        # Case 3: Mixed (One line has space, one doesn't)
        case_3 = "> Line one\n>Line two"

        # Case 4: Invalid (One line is missing the '>')
        case_4 = "> Line one\nLine two is missing the symbol"

        self.assertEqual(BlockType.QUOTE, block_to_block_type(case_1))
        self.assertEqual(BlockType.QUOTE, block_to_block_type(case_2))
        self.assertEqual(BlockType.QUOTE, block_to_block_type(case_3))
        self.assertNotEqual(BlockType.QUOTE, block_to_block_type(case_4))

    def test_markdown_unordered_list(self):
        # Valid: Every line starts with "- "
        case_1 = "- Item 1\n- Item 2\n- Item 3"
        # Invalid: Missing space
        case_2 = "-Item 1\n- Item 2"
        # Invalid: One line doesn't have the dash
        case_3 = "- Item 1\nItem 2"

        self.assertEqual(block_to_block_type(case_1), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type(case_2), BlockType.UNORDERED_LIST)
        self.assertNotEqual(block_to_block_type(case_3), BlockType.UNORDERED_LIST)

    def test_markdown_ordered_list(self):
        # Valid: Starts at 1 and increments
        case_1 = "1. First\n2. Second\n3. Third"
        # Invalid: Starts at 2
        case_2 = "2. First\n3. Second"
        # Invalid: Skips a number
        case_3 = "1. First\n3. Second"
        # Invalid: Missing space or dot
        case_4 = "1 First\n2 Second"

        self.assertEqual(block_to_block_type(case_1), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type(case_2), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type(case_3), BlockType.ORDERED_LIST)
        self.assertNotEqual(block_to_block_type(case_4), BlockType.ORDERED_LIST)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and _more_ items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )

    def test_code(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
if __name__ == "__main__":
    unittest.main()
