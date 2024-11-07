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
