from enum import Enum
import re

from SplitNodes import text_to_textnodes
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(text: str) -> list[str]:
    blocks = text.split("\n\n")
    filtered = []

    for block in blocks:
        if block == "":
            continue
        block = block.strip()
        filtered.append(block)

    return filtered


def block_to_block_type(block: str) -> BlockType:

    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE
    if block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST

    return BlockType.PARAGRAPH

def markdown_to_html_node(text: str) -> ParentNode:

    markdown_blocks = markdown_to_blocks(text)

    leaf_nodes: list[HTMLNode] = []

    for block in markdown_blocks:
        leaf_nodes.append(block_to_html_node(block))

    return ParentNode("div", leaf_nodes)


def block_to_html_node(text: str) -> ParentNode:

    block_type = block_to_block_type(text)

    match (block_type):
        case BlockType.HEADING:
            return heading_helper_html_node(text)

        case BlockType.PARAGRAPH:
            return paragraph_helper_node(text)

        case BlockType.QUOTE:
            return quote_helper_html_node(text)

        case BlockType.CODE:
            return code_block_helper(text)

        case BlockType.UNORDERED_LIST:
            return unordered_list_helper(text)

        case BlockType.ORDERED_LIST:
            return ordered_list_helper(text)

        case _:
            raise ValueError("invalid block type")


def paragraph_helper_node(text: str) -> ParentNode:
    broken_text = text.split("\n")
    line =  " ".join(broken_text)

    children = text_to_child(line)

    return ParentNode("p", children)

def code_block_helper(text) -> ParentNode:

    if not text.startswith("```") or not text.endswith("```"):
        raise ValueError("invalid code block")

    new_text = text[4:-3]

    raw_text_node= TextNode(new_text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child])

    return ParentNode("pre", [code])


def ordered_list_helper(text) -> ParentNode:

    html_nodes:list[HTMLNode] = []

    items = text.split("\n")

    for item in items:

        line = item.split(". ")[1]
        children = text_to_child(line)
        html_nodes.append(ParentNode("li", children))

    return ParentNode("ol", html_nodes)

def unordered_list_helper(text) -> ParentNode:

    html_nodes:list[HTMLNode] = []

    items = text.split("\n")

    for item in items:

        line =item[2:]
        children = text_to_child(line)
        html_nodes.append(ParentNode("li", children))

    return ParentNode("ul", html_nodes)

def heading_helper_html_node(text) -> ParentNode:

    count = 0
    for ch in text:
        if ch == "#":
            count += 1
        else:
            break

    if count + 1 >= len(text):
        raise ValueError(f"invalid heading level: {count}")

    content = text[count + 1: ]
    children = text_to_child(content)

    return ParentNode(f"h{count}", children)

def quote_helper_html_node(text) -> ParentNode:

    lines = text.split("\n")

    text_nodes: list[TextNode] = []

    items = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        items.append(line.lstrip(">").strip())

    content = " ".join(items)
    children = text_to_child(content)

    return ParentNode("blockquote", children)

def text_to_child(text) -> list[HTMLNode]:

    text_nodes = text_to_textnodes(text)
    nodes: list[HTMLNode] = []
    for node in text_nodes:
        nodes.append(text_node_to_html_node(node))

    return nodes
