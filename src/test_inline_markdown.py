import unittest
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )
    def test_delim_bold_mulitword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )
    
    def test_delim_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )
    
    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes
        )

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "this is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
            ("image", "https://i.imgur.com/zjjcJKZ.png"),
        ],
        matches)

    def test_extract_markdown_images_empty_string(self):
        matches = extract_markdown_images("")
        self.assertListEqual([], matches)
    
    def test_extract_markdown_images_none(self):
        text = None
        with self.assertRaises(TypeError):
            extract_markdown_images(text)
    
    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "this is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([
            ("to boot dev", "https://www.boot.dev"),
            ("to youtube", "https://www.youtube.com/@bootdotdev"),
        ], matches)

    def test_extract_markdown_links_empty_string(self):
        matches = extract_markdown_links("")
        self.assertListEqual([], matches)
    
    def test_extract_markdown_links_none(self):
        text = None
        with self.assertRaises(TypeError):
            extract_markdown_links(text)
    
    def test_split_nodes_image(self):
        node = TextNode("testing this ![image](url) image link", TextType.TEXT)
        old_nodes = [node]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("testing this ",  TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url"),
                TextNode(" image link", TextType.TEXT),
            ], new_nodes
        )

    def test_split_nodes_image_at_end(self):
        node = TextNode("this is text with an ![image](url)", TextType.TEXT)
        old_nodes = [node]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("this is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url"),
            ], new_nodes
        )

    def test_split_nodes_image_at_start(self):
        node = TextNode("![image](url) This is some text", TextType.TEXT)
        old_nodes = [node]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "url"),
                TextNode(" This is some text", TextType.TEXT),
            ], new_nodes
        )

    def test_split_nodes_image_two_images(self):
        node = TextNode(
            "Test for this ![image1](url1) and this ![image2](url2)", TextType.TEXT
        )
        old_nodes = [node]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual(
            [
                TextNode("Test for this ", TextType.TEXT),
                TextNode("image1", TextType.IMAGE, "url1"),
                TextNode(" and this ", TextType.TEXT),
                TextNode("image2", TextType.IMAGE, "url2"),
            ], new_nodes
        )

    def test_split_nodes_image_no_image(self):
        node = TextNode("this is some random text", TextType.TEXT)
        old_nodes = [node]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_image_non_text(self):
        node = TextNode("this is some bold text", TextType.BOLD)
        old_nodes = [node]
        new_nodes = split_nodes_image(old_nodes)
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_link(self):
        node = TextNode("this tests a [link](url) split", TextType.TEXT)
        old_nodes = [node]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("this tests a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
                TextNode(" split", TextType.TEXT),
            ], new_nodes
        )

    def test_split_nodes_link_at_end(self):
        node = TextNode("this is a test [link](url)", TextType.TEXT)
        old_nodes = [node]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("this is a test ", TextType.TEXT),
                TextNode("link", TextType.LINK, "url"),
            ], new_nodes
        )

    def test_split_nodes_link_at_start(self):
        node = TextNode("[link](url) this is a test", TextType.TEXT)
        old_nodes = [node]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("link", TextType.LINK, "url"),
                TextNode(" this is a test", TextType.TEXT),
            ], new_nodes
        )

    def test_split_nodes_link_two_links(self):
        node = TextNode(
            "Test for this [link1](url1) and this [link2](url2) split", TextType.TEXT
        )
        old_nodes = [node]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual(
            [
                TextNode("Test for this ", TextType.TEXT),
                TextNode("link1", TextType.LINK, "url1"),
                TextNode(" and this ", TextType.TEXT),
                TextNode("link2", TextType.LINK, "url2"),
                TextNode(" split", TextType.TEXT),
            ], new_nodes
        )

    def test_split_nodes_link_no_link(self):
        node = TextNode("this is some text", TextType.TEXT)
        old_nodes = [node]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual([node], new_nodes)

    def test_split_nodes_link_non_text(self):
        node = TextNode("this is bold text", TextType.BOLD)
        old_nodes = [node]
        new_nodes = split_nodes_link(old_nodes)
        self.assertListEqual([node], new_nodes)

    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ], new_nodes
        )

    def test_text_to_textnodes_multiple_same_type(self):
        text = "This is **text** with multiple **bold** words _and_ multiple _italic_ words"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with multiple ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" words ", TextType.TEXT),
                TextNode("and", TextType.ITALIC),
                TextNode(" multiple ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" words", TextType.TEXT),
            ], new_nodes
        )

    def test_text_to_textnodes_plain_text(self):
        text = "this is some plain text"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual([TextNode("this is some plain text", TextType.TEXT)], new_nodes)

    def test_text_to_textnodes_one_markdown_type(self):
        text = "this is text with some ![image](url) markdown"
        new_nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("this is text with some ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "url"),
                TextNode(" markdown", TextType.TEXT),
            ], new_nodes
        )

    
if __name__ == "__main__":
    unittest.main()