import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from utils import *


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


class TestSplitTextNodes(unittest.TestCase):
    def test_split_text_node_italic(self):
        text_node = TextNode("Hello *world* it's me", TextType.TEXT, url=None)
        text_nodes = split_nodes_delimiter([text_node], "*", TextType.ITALIC)
        expected_split = [
            TextNode("Hello ", TextType.TEXT, url=None),
            TextNode("world", TextType.ITALIC, url=None),
            TextNode(" it's me", TextType.TEXT, url=None),
        ]
        self.assertEqual(text_nodes, expected_split)

    def test_split_text_node_bold(self):
        text_node = TextNode("Hello **world** it's me", TextType.TEXT, url=None)
        text_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        expected_split = [
            TextNode("Hello ", TextType.TEXT, url=None),
            TextNode("world", TextType.BOLD, url=None),
            TextNode(" it's me", TextType.TEXT, url=None),
        ]
        self.assertEqual(text_nodes, expected_split)

    def test_split_text_node_code(self):
        text_node = TextNode("Hello ```world``` it's me", TextType.TEXT, url=None)
        text_nodes = split_nodes_delimiter([text_node], "```", TextType.CODE)
        expected_split = [
            TextNode("Hello ", TextType.TEXT, url=None),
            TextNode("world", TextType.CODE, url=None),
            TextNode(" it's me", TextType.TEXT, url=None),
        ]
        self.assertEqual(text_nodes, expected_split)

    def test_split_text_node_italic_start_of_line(self):
        text_node = TextNode("*Hello* world it's me", TextType.TEXT, url=None)
        text_nodes = split_nodes_delimiter([text_node], "*", TextType.ITALIC)
        expected_split = [
            TextNode("", TextType.TEXT, url=None),
            TextNode("Hello", TextType.ITALIC, url=None),
            TextNode(" world it's me", TextType.TEXT, url=None),
        ]
        self.assertEqual(text_nodes, expected_split)

    def test_split_text_node_italic_end_of_line(self):
        text_node = TextNode("Hello world it's *me*", TextType.TEXT, url=None)
        text_nodes = split_nodes_delimiter([text_node], "*", TextType.ITALIC)
        expected_split = [
            TextNode("Hello world it's ", TextType.TEXT, url=None),
            TextNode("me", TextType.ITALIC, url=None),
            TextNode("", TextType.TEXT, url=None),
        ]
        self.assertEqual(text_nodes, expected_split)

    def test_split_text_node_bold_start_of_line(self):
        text_node = TextNode("**Hello** world it's me", TextType.TEXT, url=None)
        text_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        expected_split = [
            TextNode("", TextType.TEXT, url=None),
            TextNode("Hello", TextType.BOLD, url=None),
            TextNode(" world it's me", TextType.TEXT, url=None),
        ]
        self.assertEqual(text_nodes, expected_split)

    def test_split_text_node_bold_end_of_line(self):
        text_node = TextNode("Hello world it's **me**", TextType.TEXT, url=None)
        text_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        expected_split = [
            TextNode("Hello world it's ", TextType.TEXT, url=None),
            TextNode("me", TextType.BOLD, url=None),
            TextNode("", TextType.TEXT, url=None),
        ]
        self.assertEqual(text_nodes, expected_split)

    def test_split_text_node_code_start_of_line(self):
        text_node = TextNode("```Hello``` world it's me", TextType.TEXT, url=None)
        text_nodes = split_nodes_delimiter([text_node], "```", TextType.CODE)
        expected_split = [
            TextNode("", TextType.TEXT, url=None),
            TextNode("Hello", TextType.CODE, url=None),
            TextNode(" world it's me", TextType.TEXT, url=None),
        ]
        self.assertEqual(text_nodes, expected_split)

    def test_split_text_node_code_end_of_line(self):
        text_node = TextNode("Hello world it's ```me```", TextType.TEXT, url=None)
        text_nodes = split_nodes_delimiter([text_node], "```", TextType.CODE)
        expected_split = [
            TextNode("Hello world it's ", TextType.TEXT, url=None),
            TextNode("me", TextType.CODE, url=None),
            TextNode("", TextType.TEXT, url=None),
        ]
        self.assertEqual(text_nodes, expected_split)


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        alt_texts = ["rick roll", "obi wan"]
        image_urls = [
            "https://i.imgur.com/aKaOqIh.gif",
            "https://i.imgur.com/fJRm4Vk.jpeg",
        ]
        extracted = [(i, j) for i, j in zip(alt_texts, image_urls)]
        self.assertEqual(extracted, extract_markdown_images(text))


if __name__ == "__main__":
    unittest.main()
