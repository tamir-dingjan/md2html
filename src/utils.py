from textnode import TextType, TextNode
from htmlnode import LeafNode, ParentNode
from blocktypes import BlockType
import re, os, logging


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
        "```": TextType.CODE,
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


def block_to_blocktype(text: str):
    if text.startswith("#"):
        header = text.split(" ")[0]
        match header:
            case "#":
                return BlockType.H1
            case "##":
                return BlockType.H2
            case "###":
                return BlockType.H3
            case "####":
                return BlockType.H4
            case "#####":
                return BlockType.H5
            case "######":
                return BlockType.H6
    elif text.startswith("```") and text.endswith("```"):
        return BlockType.CODE
    elif [x.startswith(">") for x in text.split("\n")].count(False) == 0:
        return BlockType.QUOTE
    elif [x.startswith("- ") or x.startswith("* ") for x in text.split("\n")].count(
        False
    ) == 0:
        return BlockType.UNORDERED_LIST
    elif text.startswith("1. "):
        i = 1
        for line in text.split("\n"):

            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH


def map_blocktype_to_tag(blocktype: BlockType):
    match blocktype:
        case BlockType.PARAGRAPH:
            return "p"
        case BlockType.H1:
            return "h1"
        case BlockType.H2:
            return "h2"
        case BlockType.H3:
            return "h3"
        case BlockType.H4:
            return "h4"
        case BlockType.H5:
            return "h5"
        case BlockType.H6:
            return "h6"
        case BlockType.CODE:
            return "pre"
        case BlockType.QUOTE:
            return "blockquote"
        case BlockType.UNORDERED_LIST:
            return "ul"
        case BlockType.ORDERED_LIST:
            return "ol"


def block_to_html_node(block: str):
    blocktype = block_to_blocktype(block)
    tag = map_blocktype_to_tag(blocktype)

    # The block type determines how the text should be packaged
    # The TextNodes represent inline text elements,
    # which the block needs to arrange depending on the block type:
    # A BlockType.PARAGRAPH block should wrap all of its TextNodes in a <p> tag
    # A BlockType.H1 block should wrap all of its TextNodes in a <h1> tag
    # A BlockType.H2 block should wrap all of its TextNodes in a <h2> tag
    # A BlockType.H3 block should wrap all of its TextNodes in a <h3> tag
    # A BlockType.H4 block should wrap all of its TextNodes in a <h4> tag
    # A BlockType.H5 block should wrap all of its TextNodes in a <h5> tag
    # A BlockType.H6 block should wrap all of its TextNodes in a <h6> tag
    # A BlockType.CODE block should wrap all of its TextNodes in a <pre> tag
    # A BlockType.QUOTE block should wrap all of its TextNodes in a <blockquote> tag
    # A BlockType.UNORDERED_LIST block should wrap all of its TextNodes in an <ul> tag
    # A BlockType.ORDERED_LIST block should wrap all of its TextNodes in an <ol> tag

    # Depending on the block type, we need to strip the MarkDown formatting characters
    # out of the text before converting the text to TextNodes
    if tag in ["h1", "h2", "h3", "h4", "h5", "h6"]:
        block = block.lstrip("# ")

    # For code blocks, we keep the backticks so that the TextNode can be correctly identified as code
    if tag == "pre":
        pass

    # For quote blocks, we need to remove the > at the start of each line
    if tag == "blockquote":
        block = "\n".join([x.lstrip("> ") for x in block.split("\n")])

    # For unordered lists, we need to remove the "- " or "* " at the start of each line
    if tag == "ul":
        if block.startswith("- "):
            block = "\n".join([x.lstrip("- ") for x in block.split("\n")])
        elif block.startswith("* "):
            block = "\n".join([x.lstrip("* ") for x in block.split("\n")])

    # For ordered lists, we need to remove the "X. " at the start of each line
    if tag == "ol":
        block = "\n".join([x.lstrip("1234567890. ") for x in block.split("\n")])

    # Depending on the BlockType, we may need to wrap each line of the block in a tag
    # For lists, we need to wrap each line in a <li> tag
    htmlnode = ParentNode(tag, children=[], props=None)

    if tag in ["ul", "ol"]:
        for line in block.split("\n"):
            textnodes = text_to_textnodes(line)
            node_to_add = ParentNode("li", children=[], props=None)
            for textnode in textnodes:
                node_to_add.children.append(text_node_to_html_node(textnode))
            htmlnode.children.append(node_to_add)

    # For non-list BlockTypes, we do not need to wrap each line of the block text
    else:
        textnodes = text_to_textnodes(block)
        for textnode in textnodes:
            htmlnode.children.append(text_node_to_html_node(textnode))

    return ParentNode(tag="div", children=[htmlnode], props=None)


def markdown_to_html_node(markdown: str):
    htmlnodes = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        htmlnodes.append(block_to_html_node(block))

    return ParentNode("div", children=htmlnodes, props=None)


def extract_title(markdown: str):
    title = None
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_blocktype(block)
        if block_type == BlockType.H1:
            title = block.strip("# ")
            break
    if title == None:
        raise Exception("No title found in markdown.")
    return title


def generate_page(from_path: str, template_path: str, dest_path: str):
    logging.info(
        f"Generating page from {from_path} to {dest_path} using template {template_path}"
    )
    with open(from_path, "r") as f:
        markdown = "".join(f.readlines())
    with open(template_path, "r") as f:
        template = "".join(f.readlines())

    html = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))

    with open(dest_path, "w") as f:
        f.write(template)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
):
    for item in os.listdir(dir_path_content):
        if os.path.isfile(os.path.join(dir_path_content, item)):
            generate_page(
                os.path.join(dir_path_content, item),
                template_path,
                os.path.join(dest_dir_path, os.path.splitext(item)[0] + ".html"),
            )
        elif os.path.isdir(os.path.join(dir_path_content, item)):
            generate_pages_recursive(
                os.path.join(dir_path_content, item),
                template_path,
                os.path.join(dest_dir_path, item),
            )
