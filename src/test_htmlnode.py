import unittest
from htmlnode import HTMLNode


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


if __name__ == "__main__":
    unittest.main()
