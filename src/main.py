from textnode import TextType, TextNode


def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    print(node.__repr__())


main()
