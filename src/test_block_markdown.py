import unittest

from block_markdown import (
    BlockType,
    markdown_to_blocks,
    block_to_block_type,
    code_helper,
    ordered_list_helper,
    unordered_list_helper,
    quotes_helper,
    markdown_to_html_node,
)

class TestMarkdownBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_block_multi_blank_lines(self):
        md = """
This is **bolded** paragraph


This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line


- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_block_to_block_type_plain_text(self):
        block = "this is some normal-style text"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)
    
    def test_block_to_block_type_heading(self):
        block =  "### This is a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.HEADING)

    def test_block_to_block_type_wrong_heading(self):
        block = "####### This is not a heading"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        block = "```\n This is a code block\n```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.CODE)

    def test_block_to_block_type_code_bad_format(self):
        block = "```This is a bad code block```"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_type_quote(self):
        block = ">This is a lovely quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)
    
    def test_block_to_block_type_multi_quote(self):
        block = ">This is a lovely quote\n>This is an even lovelier quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.QUOTE)

    def test_block_to_block_type_quote_with_bad_line(self):
        block = ">This is a lovely quote\nThis is a bad line\n>This is an even lovelier quote"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)

    def test_block_to_block_unordered_list(self):
        block = "- This is a list item\n- And another list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.UNORDERED_LIST)

    def test_block_to_block_ordered_list(self):
        block = "1. This is a list item\n2. This is another list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.ORDERED_LIST)

    def test_block_to_block_ordered_list_wrong_order(self):
        block = "1. This is a list item\n3. This is another list item"
        block_type = block_to_block_type(block)
        self.assertEqual(block_type, BlockType.PARAGRAPH)


    def test_code_helper(self):
        block = """
```
this is some text
this is the same 
```
"""
        pre_node = code_helper(block)
        self.assertEqual(
            "<pre><code>this is some text\nthis is the same</code></pre>", pre_node.to_html()
        )

    def test_ordered_list_helper(self):
        block = """
1. This is a list item
2. This is another list item
"""
        ordered_list = ordered_list_helper(block)
        self.assertEqual(
            "<ol><li>This is a list item</li><li>This is another list item</li></ol>", ordered_list.to_html()
        )

    def test_unordered_list_helper(self):
        block = """
- This is a list item
- This is another list item
"""
        unordered_list = unordered_list_helper(block)
        self.assertEqual(
            "<ul><li>This is a list item</li><li>This is another list item</li></ul>", unordered_list.to_html()
        )

    def test_quote_helper(self):
        block = """
> This is a quote
> This is another _quote_
"""
        quotes = quotes_helper(block)
        self.assertEqual(
            "<blockquote>This is a quote This is another <i>quote</i></blockquote>", quotes.to_html()
        )

    def test_paragraph(self):
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

    def test_codeblock(self):
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
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff</code></pre></div>",
        )


if __name__ == "__main__":
    unittest.main()