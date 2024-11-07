from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode


def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node.__repr__())


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


if __name__ == "__main__":
    main()
