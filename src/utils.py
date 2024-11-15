from textnode import TextType, TextNode
from htmlnode import LeafNode
import re


def text_node_to_html_node(text_node: "TextNode"):
    match TextType(text_node.text_type):
        case TextType.TEXT:
            return LeafNode(tag=None, value=text_node.text)
        case TextType.BOLD:
            return LeafNode(tag="b", value=text_node.text)
        case TextType.ITALIC:
            return LeafNode(tag="i", value=text_node.text)
        case TextType.CODE:
            return LeafNode(tag="code", value=text_node.text)
        case TextType.LINK:
            return LeafNode(
                tag="a", value=text_node.text, props={"href": text_node.url}
            )
        case TextType.IMAGE:
            return LeafNode(
                tag="img", value="", props={"src": text_node.url, "alt": text_node.text}
            )
        case _:
            print(text_node.__repr__())
            raise ValueError(f"Invalid TextType value: {text_node.text_type}")


def split_nodes_delimiter(old_nodes: list, delimiter: str, text_type: TextType):
    new_nodes = []
    # For each node in the old_nodes list
    for node in old_nodes:
        # Find the text fields which are bordered by the delimiter string
        node_text = node.text
        if delimiter not in node_text:
            new_nodes.append(node)
            continue

        # Construct a regex match using negative lookbehind and negative lookahead
        # to avoid matching on adjacent delimiters
        # This will exclude text containing empty delimiter pairs: i.e., ``````
        # It will also prevent matching on italics "*" from also matching bold "**" delimeters
        # Because the asterisk character is a wildcard for regex expressions, escape all characters of
        # the delimiter string:
        delimiter = re.escape(delimiter)
        regex = f"(?<![{delimiter}]){delimiter}(?![{delimiter}])"
        fields = re.split(regex, node_text)

        # Only split text with delimiter pairs, which will always produce an odd number of text fields
        if len(fields) % 2 == 0:
            raise NotImplementedError(
                f"Unpaired delimiter '{delimiter}' found in input text: {node_text}"
            )

        # Create new textnodes with the provided text_type for the delimited text fields
        # Treat the first text field as normal text, and do not apply the provided TextType to this
        normal_text = True
        for text_field in fields:
            if normal_text:
                new_nodes.append(TextNode(text_field, TextType.TEXT))
                normal_text = False
            else:
                new_nodes.append(TextNode(text_field, text_type))
                normal_text = True

    return new_nodes


def extract_markdown_images(text: str):
    alt_texts = re.findall("\!\[(.*?)\]", text)
    urls = re.findall("\((.*?)\)", text)
    extracted = [(i, j) for i, j in zip(alt_texts, urls)]
    return extracted


def extract_markdown_links(text: str):
    links = re.findall("\[(.*?)\]", text)
    urls = re.findall("\((.*?)\)", text)
    extracted = [(i, j) for i, j in zip(links, urls)]
    return extracted


def split_nodes_image(old_nodes: list):
    new_nodes = []
    for node in old_nodes:
        # If there are no markdown images in this node, append it the output as-is
        extracted = extract_markdown_images(node.text)
        if extracted == []:
            new_nodes.append(node)
            continue
        # Extract the normal text fields from the textnode
        # We can do this by splitting the text by the appropriate regex
        # Python will keeep the matched text when capture groups are used in the regex pattern
        # This means we don't actually need to extract any fields, we can just process the node text
        # with a rotating filter for how to handle each element
        text_fields = re.split("\!\[(.*?\]\(.*?)\)", node.text)

        # The first element will always be the normal text, because the split regex will return
        # an empty string as the first element if the text begins with a matching field
        field_type = "text"

        while len(text_fields) > 0:
            _text = text_fields.pop(0)
            if field_type == "text":
                new_nodes.append(TextNode(_text, TextType.TEXT))
                field_type = "image"
            elif field_type == "image":
                alt_text, url = _text.split("](")
                new_nodes.append(TextNode(alt_text, TextType.IMAGE, url=url))
                field_type = "text"

    return new_nodes


def split_nodes_link(old_nodes: list):
    new_nodes = []
    for node in old_nodes:
        # If there are no markdown links in this node, append it the output as-is
        extracted = extract_markdown_links(node.text)
        if extracted == []:
            new_nodes.append(node)
            continue
        # Extract the normal text fields from the textnode
        # We can do this by splitting the text by the appropriate regex
        # Python will keeep the matched text when capture groups are used in the regex pattern
        # This means we don't actually need to extract any fields, we can just process the node text
        # with a rotating filter for how to handle each element
        text_fields = re.split("\[(.*?\]\(.*?)\)", node.text)

        # The first element will always be the normal text, because the split regex will return
        # an empty string as the first element if the text begins with a matching field
        field_type = "text"

        while len(text_fields) > 0:
            _text = text_fields.pop(0)
            if field_type == "text":
                new_nodes.append(TextNode(_text, TextType.TEXT))
                field_type = "link"
            elif field_type == "link":
                alt_text, url = _text.split("](")
                new_nodes.append(TextNode(alt_text, TextType.LINK, url=url))
                field_type = "text"

    return new_nodes


def text_to_textnodes(text: str):
    node = [TextNode(text, TextType.TEXT, url=None)]
    delims = {
        "**": TextType.BOLD,
        "*": TextType.ITALIC,
        "`": TextType.CODE,
    }
    for delim, text_type in delims.items():
        node = split_nodes_delimiter(node, delim, text_type)

    node = split_nodes_image(node)
    node = split_nodes_link(node)

    return node


def markdown_to_blocks(markdown: str):
    blocks = markdown.split("\n\n")
    return blocks
