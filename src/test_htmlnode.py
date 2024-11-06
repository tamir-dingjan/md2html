import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_repr(self):
        node = HTMLNode(
            "div", "Hello, World!", children=None, props={"class": "my-class"}
        )
        self.assertEqual(
            node.__repr__(), "HTMLNode(div, Hello, World!, None, {'class': 'my-class'})"
        )

    def test_props_to_html(self):
        node = HTMLNode(
            "div", "Hello, World!", children=None, props={"class": "my-class"}
        )
        self.assertEqual(node.props_to_html(), ' class="my-class"')

    def test_props_to_html_multiple(self):
        node = HTMLNode(
            "div",
            "Hello, World!",
            children=None,
            props={"class": "my-class", "style": "color: red", "data-foo": "bar"},
        )
        self.assertEqual(
            node.props_to_html(), ' class="my-class" style="color: red" data-foo="bar"'
        )

    def test_leaf_node_value_is_none(self):
        node = LeafNode("p", None)
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_node_paragraph(self):
        node = LeafNode("p", "Hello, World!")
        self.assertEqual(node.to_html(), "<p>Hello, World!</p>")

    def test_leaf_node_paragraph_with_props(self):
        node = LeafNode("p", "Hello, World!", props={"class": "my-class"})
        self.assertEqual(node.to_html(), '<p class="my-class">Hello, World!</p>')

    def test_leaf_node_anchor(self):
        node = LeafNode("a", "Hello, World!", props={"href": "https://www.boot.dev"})
        self.assertEqual(
            node.to_html(), '<a href="https://www.boot.dev">Hello, World!</a>'
        )

    def test_leaf_node_anchor_with_props(self):
        node = LeafNode(
            "a",
            "Hello, World!",
            props={"href": "https://www.boot.dev", "class": "my-class"},
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.boot.dev" class="my-class">Hello, World!</a>',
        )

    def test_parent_node_tag_is_none(self):
        node = ParentNode(None, [LeafNode("p", "Hello, World!")])
        self.assertRaises(ValueError, node.to_html)

    def test_parent_node_children_is_none(self):
        node = ParentNode("div", None)
        self.assertRaises(ValueError, node.to_html)

    def test_parent_node_children_is_empty(self):
        node = ParentNode("div", [])
        self.assertRaises(ValueError, node.to_html)

    def test_parent_node_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>",
        )

    def test_parent_node_multiple_children_with_props(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text", props={"class": "my-class"}),
                LeafNode("p", "Normal text", props={"class": "my-class"}),
                LeafNode("i", "italic text", props={"class": "my-class"}),
                LeafNode("p", "Normal text", props={"class": "my-class"}),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<p><b class="my-class">Bold text</b><p class="my-class">Normal text</p><i class="my-class">italic text</i><p class="my-class">Normal text</p></p>',
        )

    def test_parent_node_with_nested_parent(self):
        node = ParentNode(
            "p",
            [
                ParentNode(
                    "b",
                    [LeafNode("i", "italic text"), LeafNode("i", "more italic text")],
                ),
                LeafNode("b", "Bold text", props={"class": "my-class"}),
                LeafNode("p", "Normal text", props={"class": "my-class"}),
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<p><b><i>italic text</i><i>more italic text</i></b><b class="my-class">Bold text</b><p class="my-class">Normal text</p></p>',
        )


if __name__ == "__main__":
    unittest.main()
