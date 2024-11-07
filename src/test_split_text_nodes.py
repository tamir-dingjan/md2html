import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from utils import *


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


if __name__ == "__main__":
    unittest.main()
