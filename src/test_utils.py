import unittest
from textnode import TextNode, TextType
from htmlnode import LeafNode
from utils import *


class TestHTMLNode(unittest.TestCase):

    def test_texttype_coverage(self):
        # Make sure the conversion to HTML gives a LeafNode for every valid TextType
        for text_type in TextType:
            text_node = TextNode("Iterating over TextTypes", text_type, url=None)
            self.assertIsInstance(text_node_to_html_node(text_node), LeafNode)

    def test_convert_text(self):
        textnode = TextNode("Hello world", TextType.TEXT, url=None)
        leafnode = LeafNode(tag=None, value="Hello world", props=None)
        converted_node = text_node_to_html_node(textnode)

        # Test the LeafNode conversion gives the right result
        self.assertEqual(leafnode.__repr__(), converted_node.__repr__())

        # Test the HTML output works
        html = "Hello world"
        self.assertEqual(html, leafnode.to_html())
        self.assertEqual(html, converted_node.to_html())

    def test_convert_bold(self):
        textnode = TextNode("Hello world", TextType.BOLD, url=None)
        leafnode = LeafNode(tag="b", value="Hello world", props=None)
        converted_node = text_node_to_html_node(textnode)
        html = "<b>Hello world</b>"
        self.assertEqual(leafnode.__repr__(), converted_node.__repr__())
        self.assertEqual(html, leafnode.to_html())
        self.assertEqual(html, converted_node.to_html())

    def test_convert_italic(self):
        textnode = TextNode("Hello world", TextType.ITALIC, url=None)
        leafnode = LeafNode(tag="i", value="Hello world", props=None)
        converted_node = text_node_to_html_node(textnode)
        html = "<i>Hello world</i>"
        self.assertEqual(leafnode.__repr__(), converted_node.__repr__())
        self.assertEqual(html, leafnode.to_html())
        self.assertEqual(html, converted_node.to_html())

    def test_convert_code(self):
        textnode = TextNode("Hello world", TextType.CODE, url=None)
        leafnode = LeafNode(tag="code", value="Hello world", props=None)
        converted_node = text_node_to_html_node(textnode)
        html = "<code>Hello world</code>"
        self.assertEqual(leafnode.__repr__(), converted_node.__repr__())
        self.assertEqual(html, leafnode.to_html())
        self.assertEqual(html, converted_node.to_html())

    def test_convert_link(self):
        textnode = TextNode("Hello world", TextType.LINK, url="https://www.boot.dev")
        leafnode = LeafNode(
            tag="a", value="Hello world", props={"href": "https://www.boot.dev"}
        )
        converted_node = text_node_to_html_node(textnode)
        html = '<a href="https://www.boot.dev">Hello world</a>'
        self.assertEqual(leafnode.__repr__(), converted_node.__repr__())
        self.assertEqual(html, leafnode.to_html())
        self.assertEqual(html, converted_node.to_html())

    def test_convert_image(self):
        textnode = TextNode("Hello world", TextType.IMAGE, url="https://www.boot.dev")
        leafnode = LeafNode(
            tag="img",
            value="",
            props={"src": "https://www.boot.dev", "alt": "Hello world"},
        )
        converted_node = text_node_to_html_node(textnode)
        html = '<img src="https://www.boot.dev" alt="Hello world"></img>'
        self.assertEqual(leafnode.__repr__(), converted_node.__repr__())
        self.assertEqual(html, leafnode.to_html())
        self.assertEqual(html, converted_node.to_html())


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

    def test_split_text_node_bold_unspaced(self):
        text_node = TextNode("**Hello**: world it's me", TextType.TEXT, url=None)
        text_nodes = split_nodes_delimiter([text_node], "**", TextType.BOLD)
        expected_split = [
            TextNode("", TextType.TEXT, url=None),
            TextNode("Hello", TextType.BOLD, url=None),
            TextNode(": world it's me", TextType.TEXT, url=None),
        ]
        self.assertEqual(text_nodes, expected_split)

    def test_split_text_node_code(self):
        text_node = TextNode(
            """```
def hello_world():
    print("Hello, world!")
```""",
            TextType.TEXT,
            url=None,
        )
        text_nodes = split_nodes_delimiter([text_node], "```", TextType.CODE)
        expected_split = [
            TextNode("", TextType.TEXT, url=None),
            TextNode(
                """
def hello_world():
    print("Hello, world!")
""",
                TextType.CODE,
                url=None,
            ),
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

    def test_split_text_node_code_single_delimiter_char(self):
        text_node = TextNode(
            "deities (the `Valar` and `Maiar`)", TextType.TEXT, url=None
        )
        text_nodes = split_nodes_delimiter([text_node], "`", TextType.CODE)
        expected_split = [
            TextNode("deities (the ", TextType.TEXT, url=None),
            TextNode("Valar", TextType.CODE, url=None),
            TextNode(" and ", TextType.TEXT, url=None),
            TextNode("Maiar", TextType.CODE, url=None),
            TextNode(")", TextType.TEXT, url=None),
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
        text = "This is **text** with an *italic* word and a ```code block``` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
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


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        text = """# This is a H1 heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""
        blocks = markdown_to_blocks(text)
        self.assertEqual(3, len(blocks))
        self.assertEqual("# This is a H1 heading", blocks[0])
        self.assertEqual(
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            blocks[1],
        )
        self.assertEqual(
            """* This is the first list item in a list block
* This is a list item
* This is another list item""",
            blocks[2],
        )


class TestBlockToBlockType(unittest.TestCase):
    def test_block_to_block_type_paragraph(self):
        text = "This is a normal\nparagraph with some\nnew linesof text.\n"
        self.assertEqual(BlockType.PARAGRAPH, block_to_blocktype(text))

    def test_block_to_block_type_heading(self):
        text = "## This is a H2 heading"
        self.assertEqual(BlockType.H2, block_to_blocktype(text))

    def test_block_to_block_type_code(self):
        text = "```This is a code block```"
        self.assertEqual(BlockType.CODE, block_to_blocktype(text))

    def test_block_to_block_type_unordered_list(self):
        text = """* This is the first list item in a list block
* This is a list item
* This is another list item"""
        self.assertEqual(BlockType.UNORDERED_LIST, block_to_blocktype(text))

    def test_block_to_block_type_ordered_list(self):
        text = """1. This is the first list item in a list block
2. This is a list item
3. This is another list item"""
        self.assertEqual(BlockType.ORDERED_LIST, block_to_blocktype(text))


class TestBlockToHtmlNode(unittest.TestCase):
    def test_block_to_html_node_h1(self):
        text = """# This is a H1 heading"""
        html = block_to_html_node(text)
        target = "<div><h1>This is a H1 heading</h1></div>"
        self.assertEqual(target, html.to_html())

    def test_block_to_html_node_code(self):
        text = """```
def hello_world():
    print("Hello, world!")
```"""
        html = block_to_html_node(text)
        target = """<div><pre><code>
def hello_world():
    print("Hello, world!")
</code></pre></div>"""
        self.assertEqual(target, html.to_html())


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_h1(self):
        text = """# This is a H1 heading"""
        html = markdown_to_html_node(text)
        target = "<div><div><h1>This is a H1 heading</h1></div></div>"
        self.assertEqual(target, html.to_html())

    def test_h2_bold(self):
        text = """## This is a H2 heading with **bold** text"""
        html = markdown_to_html_node(text)
        target = (
            "<div><div><h2>This is a H2 heading with <b>bold</b> text</h2></div></div>"
        )
        self.assertEqual(target, html.to_html())

    def test_unordered_list(self):
        text = """- Here is an unordered list
- With multiple items
- In no particular order"""
        html = markdown_to_html_node(text)
        target = """<div><div><ul><li>Here is an unordered list</li><li>With multiple items</li><li>In no particular order</li></ul></div></div>"""
        self.assertEqual(target, html.to_html())

    def test_ordered_list(self):
        text = """1. And here is an ordered list
2. With another item
3. And some more"""
        html = markdown_to_html_node(text)
        target = """<div><div><ol><li>And here is an ordered list</li><li>With another item</li><li>And some more</li></ol></div></div>"""
        self.assertEqual(target, html.to_html())

    def test_quote(self):
        text = """> This is a blockquote.
> It has multiple lines
> Across the page"""
        html = markdown_to_html_node(text)
        target = """<div><div><blockquote>This is a blockquote.
It has multiple lines
Across the page</blockquote></div></div>"""
        self.assertEqual(target, html.to_html())

    def test_link(self):
        text = "[This is a link](https://example.com)"
        html = markdown_to_html_node(text)
        target = """<div><div><p><a href="https://example.com">This is a link</a></p></div></div>"""
        self.assertEqual(target, html.to_html())

    def test_image(self):
        text = "![Alt text for an image](https://example.com/image.jpg)"
        html = markdown_to_html_node(text)
        target = """<div><div><p><img src="https://example.com/image.jpg" alt="Alt text for an image"></img></p></div></div>"""
        self.assertEqual(target, html.to_html())

    def test_code(self):
        text = """```
def hello_world():
    print("Hello, world!")
```"""

        html = markdown_to_html_node(text)
        target = """<div><div><pre><code>
def hello_world():
    print("Hello, world!")
</code></pre></div></div>"""

        self.assertEqual(target, html.to_html())

    def test_code_single_char_delimiter(self):
        text = "deities (the `Valar` and `Maiar`)"
        html = markdown_to_html_node(text)
        target = """<div><div><p>deities (the <code>Valar</code> and <code>Maiar</code>)</p></div></div>"""
        self.assertEqual(target, html.to_html())

    def test_document(self):
        self.maxDiff = None
        text = """# Heading 1

## Heading 2

This is a paragraph with **bold text**, normal text, 
and *italic text* on two lines.

- Here is an unordered list
- With multiple items
- In no particular order

1. And here is an ordered list
2. With another item
3. And some more

A blockquote might appear as:

> This is a blockquote.
> It has multiple lines
> Across the page

[This is a link](https://example.com)

![Alt text for an image](https://example.com/image.jpg)

```
def hello_world():
    print("Hello, world!")
```"""
        target = [
            "<div><div><h1>Heading 1</h1></div>",
            "<div><h2>Heading 2</h2></div>",
            """<div><p>This is a paragraph with <b>bold text</b>, normal text, 
and <i>italic text</i> on two lines.</p></div>""",
            "<div><ul><li>Here is an unordered list</li><li>With multiple items</li><li>In no particular order</li></ul></div>",
            "<div><ol><li>And here is an ordered list</li><li>With another item</li><li>And some more</li></ol></div>",
            "<div><p>A blockquote might appear as:</p></div>",
            """<div><blockquote>This is a blockquote.
It has multiple lines
Across the page</blockquote></div>""",
            '<div><p><a href="https://example.com">This is a link</a></p></div>',
            '<div><p><img src="https://example.com/image.jpg" alt="Alt text for an image"></img></p></div>',
            """<div><pre><code>
def hello_world():
    print("Hello, world!")
</code></pre></div></div>""",
        ]

        target = "".join(target)

        html = markdown_to_html_node(text)
        self.assertEqual(target, html.to_html())


class TestExtractTitle(unittest.TestCase):
    def test_extract_title(self):
        text = """# This is a H1 heading"""
        title = extract_title(text)
        self.assertEqual("This is a H1 heading", title)

    def test_extract_error(self):
        text = """No heading here"""
        self.assertRaises(Exception, extract_title, text)


if __name__ == "__main__":
    unittest.main()
