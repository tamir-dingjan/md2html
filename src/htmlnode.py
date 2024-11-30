class HTMLNode:
    def __init__(
        self, tag: str = None, value: str = None, children=None, props: dict = None
    ):
        """
        Initializes an HTMLNode object.

        Parameters
        ----------
        tag : str, optional
            The tag of the HTML element. The default is None.
        value : str, optional
            The value of the HTML element. The default is None.
        children : list, optional
            A list of child nodes. The default is None.
        props : dict, optional
            A dictionary of key-value pairs of the HTML element's properties. The default is None.
        """
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        """
        Converts the HTMLNode object into an HTML string.

        Raises
        ------
        NotImplementedError
            If not implemented by subclass.

        Returns
        -------
        str
            A string representation of the HTML structure.
        """
        raise NotImplementedError

    def props_to_html(self):
        """
        Converts the properties of the HTMLNode object into a string of HTML.

        Returns
        -------
        str
            A string of HTML representing the properties of the HTMLNode object.
        """
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])

    def __repr__(self):
        """
        Returns a string representation of the HTMLNode object.

        Returns
        -------
        str
            A string representation of the HTMLNode object.
        """
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"


class LeafNode(HTMLNode):
    def __init__(self, tag: str, value: str, props: dict = None):
        """
        Initializes a LeafNode object.

        Parameters
        ----------
        tag : str
            The tag of the HTML element.
        value : str
            The value of the HTML element.
        props : dict, optional
            A dictionary of key-value pairs of the HTML element's properties.
            The default is None.
        """
        super().__init__(tag=tag, value=value, children=None, props=props)

    def to_html(self):
        """
        Converts the LeafNode into an HTML string.

        Raises
        ------
        ValueError
            If the value is None.

        Returns
        -------
        str
            A string representation of the HTML structure.
        """
        if self.value is None:
            raise ValueError("All leaf nodes must have a value.")
        elif self.tag is None:
            return self.value

        if self.props is None:
            rendered = f"<{self.tag}>{self.value}</{self.tag}>"
        else:
            rendered = f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
        return rendered


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children: list, props: dict = None):
        """
        Initializes a ParentNode object.

        Parameters
        ----------
        tag : str
            The HTML tag for this node.
        children : list
            A list of child nodes.
        props : dict, optional
            A dictionary of HTML properties for the node.
        """
        super().__init__(tag=tag, value=None, children=children, props=props)

    def to_html(self):
        """
        Converts the ParentNode and its children into an HTML string.

        Raises
        ------
        ValueError
            If the tag is None or if children are None.

        Returns
        -------
        str
            A string representation of the HTML structure.
        """
        if self.tag is None:
            raise ValueError("ParentNode must have a tag.")
        if self.children is None or self.children == []:
            raise ValueError("ParentNode must have children.")

        if self.props is None:
            rendered = f"<{self.tag}>"
        else:
            rendered = f"<{self.tag}{self.props_to_html()}>"

        for child in self.children:
            rendered += child.to_html()
        rendered += f"</{self.tag}>"
        return rendered

    def add_child(self, child: HTMLNode):
        self.children.append(child)
