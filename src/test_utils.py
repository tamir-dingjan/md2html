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
        text_node = TextNode("`Hello` world it's me", TextType.TEXT, url=None)
        text_nodes = split_nodes_delimiter([text_node], "`", TextType.CODE)
        expected_split = [
            TextNode("", TextType.TEXT, url=None),
            TextNode("Hello", TextType.CODE, url=None),
            TextNode(" world it's me", TextType.TEXT, url=None),
        ]
        self.assertEqual(text_nodes, expected_split)

    def test_split_text_node_code_end_of_line(self):
        text_node = TextNode("Hello world it's `me`", TextType.TEXT, url=None)
        text_nodes = split_nodes_delimiter([text_node], "`", TextType.CODE)
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

    def test_extract_markdown_images_no_image_in_input(self):
        text = "Just text here"
        extracted = []
        self.assertEqual(extracted, extract_markdown_images(text))


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        links = ["to boot dev", "to youtube"]
        urls = ["https://www.boot.dev", "https://www.youtube.com/@bootdotdev"]
        extracted = [(i, j) for i, j in zip(links, urls)]
        self.assertEqual(extracted, extract_markdown_links(text))


class TestSplitNodesImage(unittest.TestCase):
    def test_split_node_with_image_in_middle_of_line(self):
        text = "This is a text line with ![an image](https://link.to.an.image) an image in the middle of it"
        text_node = TextNode(text, TextType.TEXT, url=None)
        nodes = [
            TextNode("This is a text line with ", TextType.TEXT, url=None),
            TextNode("an image", TextType.IMAGE, url="https://link.to.an.image"),
            TextNode(" an image in the middle of it", TextType.TEXT, url=None),
        ]
        split_nodes = split_nodes_image([text_node])
        self.assertEqual(nodes, split_nodes)

    def test_split_node_with_image_at_start_of_line(self):
        text = "![an image](https://link.to.an.image) an image at the start of it"
        text_node = TextNode(text, TextType.TEXT, url=None)
        nodes = [
            TextNode("", TextType.TEXT, url=None),
            TextNode("an image", TextType.IMAGE, url="https://link.to.an.image"),
            TextNode(" an image at the start of it", TextType.TEXT, url=None),
        ]
        split_nodes = split_nodes_image([text_node])
        self.assertEqual(nodes, split_nodes)

    def test_split_node_with_image_at_end_of_line(self):
        text = "This is a text line with an image at the very end ![an image](https://link.to.an.image)"
        text_node = TextNode(text, TextType.TEXT, url=None)
        nodes = [
            TextNode(
                "This is a text line with an image at the very end",
                TextType.TEXT,
                url=None,
            ),
            TextNode("an image", TextType.IMAGE, url="https://link.to.an.image"),
            TextNode("", TextType.TEXT, url=None),
        ]


class TestSplitNodesLink(unittest.TestCase):
    def test_split_node_with_link_in_middle_of_line(self):
        text = "This is a text line with [a link](https://link.to.a.link) a link in the middle of it"
        text_node = TextNode(text, TextType.TEXT, url=None)
        nodes = [
            TextNode("This is a text line with ", TextType.TEXT, url=None),
            TextNode("a link", TextType.LINK, url="https://link.to.a.link"),
            TextNode(" a link in the middle of it", TextType.TEXT, url=None),
        ]
        split_nodes = split_nodes_link([text_node])
        self.assertEqual(nodes, split_nodes)

    def test_split_node_with_link_at_start_of_line(self):
        text = "[a link](https://link.to.a.link) a link at the start of it"
        text_node = TextNode(text, TextType.TEXT, url=None)
        nodes = [
            TextNode("", TextType.TEXT, url=None),
            TextNode("a link", TextType.LINK, url="https://link.to.a.link"),
            TextNode(" a link at the start of it", TextType.TEXT, url=None),
        ]
        split_nodes = split_nodes_link([text_node])
        self.assertEqual(nodes, split_nodes)

    def test_split_node_with_link_at_end_of_line(self):
        text = "a link at the end of it [a link](https://link.to.a.link)"
        text_node = TextNode(text, TextType.TEXT, url=None)
        nodes = [
            TextNode("a link at the end of it ", TextType.TEXT, url=None),
            TextNode("a link", TextType.LINK, url="https://link.to.a.link"),
            TextNode("", TextType.TEXT, url=None),
        ]
        split_nodes = split_nodes_link([text_node])
        self.assertEqual(nodes, split_nodes)


class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode(
                "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
            TextNode("", TextType.TEXT),
        ]
        self.assertEqual(nodes, text_to_textnodes(text))


if __name__ == "__main__":
    unittest.main()
