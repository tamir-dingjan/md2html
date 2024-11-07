import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from main import text_node_to_html_node


class TestHTMLNode(unittest.TestCase):
    def test_convert_text(self):
        textnode = TextNode("Hello world", TextType.TEXT, url=None)
        leafnode = LeafNode(tag=None, value="Hello world", props=None)
        converted_node = text_node_to_html_node(textnode)
        self.assertEqual(leafnode.to_html(), converted_node.to_html())

    def test_convert_bold(self):
        textnode = TextNode("Hello world", TextType.BOLD, url=None)
        leafnode = LeafNode(tag="b", value="Hello world", props=None)
        converted_node = text_node_to_html_node(textnode)
        self.assertEqual(leafnode.to_html(), converted_node.to_html())

    def test_convert_italic(self):
        textnode = TextNode("Hello world", TextType.ITALIC, url=None)
        leafnode = LeafNode(tag="i", value="Hello world", props=None)
        converted_node = text_node_to_html_node(textnode)
        self.assertEqual(leafnode.to_html(), converted_node.to_html())

    def test_convert_code(self):
        textnode = TextNode("Hello world", TextType.CODE, url=None)
        leafnode = LeafNode(tag="code", value="Hello world", props=None)
        converted_node = text_node_to_html_node(textnode)
        self.assertEqual(leafnode.to_html(), converted_node.to_html())

    def test_convert_link(self):
        textnode = TextNode("Hello world", TextType.LINK, url="https://www.boot.dev")
        leafnode = LeafNode(
            tag="a", value="Hello world", props={"href": "https://www.boot.dev"}
        )
        converted_node = text_node_to_html_node(textnode)
        self.assertEqual(leafnode.to_html(), converted_node.to_html())

    def test_convert_image(self):
        textnode = TextNode("Hello world", TextType.IMAGE, url="https://www.boot.dev")
        leafnode = LeafNode(
            tag="img",
            value="",
            props={"src": "https://www.boot.dev", "alt": "Hello world"},
        )
        converted_node = text_node_to_html_node(textnode)
        self.assertEqual(leafnode.to_html(), converted_node.to_html())


if __name__ == "__main__":
    unittest.main()
