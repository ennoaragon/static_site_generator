from enum import Enum

from htmlnode import LeafNode


class TextType(Enum):
    PLAIN = "plain"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"
    TEXT = "text"


class TextNode:
    def __init__(
        self, text: str, text_type: TextType = TextType.PLAIN, url: str | None = None
    ):
        self.text = text
        self.text_type: TextType = text_type
        self.url = url

    def __eq__(self, other: object) -> bool:

        if not isinstance(other, TextNode):
            return False

        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode( {self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode) -> LeafNode:

    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text, None)

    if text_node.text_type == TextType.BOLD:
        return LeafNode("b", text_node.text, None)

    if text_node.text_type == TextType.ITALIC:
        return LeafNode("i", text_node.text, None)

    if text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text, None)


    if text_node.text_type == TextType.LINK:
        prop: dict[str, str] = {"href": f"{text_node.url}"}
        return LeafNode("a", text_node.text, prop)

    if text_node.text_type == TextType.IMAGE:
        prop: dict[str, str] = {"src": f"{text_node.url}", "alt": f"{text_node.text}"}
        return LeafNode("img", "", prop)

    raise ValueError("text node isn't correctly formated to produce a LeafNode")
