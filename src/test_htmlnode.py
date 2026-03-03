import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_default_constructor(self):
        node = HTMLNode()
        self.assertIsNone(node.tag)
        self.assertIsNone(node.value)
        self.assertIsNone(node.children)
        self.assertIsNone(node.props)

    def test_props_to_html_none(self):
        node = HTMLNode(props=None)
        result = node.props_to_html()
        self.assertEqual(result, "")

    def test_props_to_html_empty_dict(self):
        node = HTMLNode(props={})
        result = node.props_to_html()
        self.assertEqual(result, "")
    
    def test_props_to_html_multiple(self):
        node = HTMLNode(props={"href": "https://www.google.com", "target": "_blank"})
        result = node.props_to_html()
        self.assertIn('href="https://www.google.com"', result)
        self.assertIn('target="_blank"', result)
        self.assertTrue(result.startswith(" "))

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some random text")
        self.assertEqual(node.to_html(), "Just some random text")
    
    def test_leaf_to_html_none(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_multiple_children(self):
        child_node = LeafNode("span", "child")
        child_node_2 = LeafNode("b", "child")
        parent_node = ParentNode("div", [child_node, child_node_2])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span><b>child</b></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_no_children(self):
        node = ParentNode("div", None)
        with self.assertRaises(ValueError) as ctx:
            node.to_html()
        self.assertIn("children", str(ctx.exception))

    def test_to_html_empty_child_list(self):
        node = ParentNode("div", [])
        with self.assertRaises(ValueError) as ctx:
            node.to_html()
        self.assertIn("children", str(ctx.exception))
    
    def test_to_html_no_tag(self):
        node = ParentNode(None, [LeafNode("span", "child")])
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "some text")
        parent_node = ParentNode("div", [child_node], {"class": "container"})
        self.assertEqual(parent_node.to_html(), '<div class="container"><span>some text</span></div>')

if __name__ == "__main__":
    unittest.main()