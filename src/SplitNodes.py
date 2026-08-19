from textnode import TextNode, TextType
from extract_makedown_links import extract_markdown_links, extract_markdown_images

DelimiterMap = {
    "`": TextType.CODE,
    "_": TextType.ITALIC,
    "**": TextType.BOLD
}

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:

    new_nodes:list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("invalid markdown, formatted section not closed")

        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))

        new_nodes.extend(split_nodes)

    return new_nodes

def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:

    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        reduced_text = node.text
        split_nodes = extract_markdown_links(node.text)

        for text, link in split_nodes:
            split_text = reduced_text.split(f"[{text}]({link})")
            if len(split_text[0]) > 0:
                new_nodes.append(
                    TextNode(split_text[0], TextType.TEXT)
                )
            reduced_text = "".join(split_text[1:])
            new_nodes.append(TextNode(text, TextType.LINK, link))

        if len(reduced_text) > 0:
            new_nodes.append(TextNode(reduced_text, TextType.TEXT))


    return new_nodes



def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes: list[TextNode] = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        reduced_text = node.text

        split_nodes = extract_markdown_images(node.text)

        for text, link in split_nodes:
            split_text = reduced_text.split(f"![{text}]({link})")
            if len(split_text[0]) > 0:
                new_nodes.append(
                    TextNode(split_text[0], TextType.TEXT)
                )

            reduced_text = "".join(split_text[1:])
            new_nodes.append(TextNode(text, TextType.IMAGE, link))


        if len(reduced_text) > 0:
            new_nodes.append(TextNode(reduced_text, TextType.TEXT))

    return new_nodes

def text_to_textnodes(text:str) -> list[TextNode]:

    text_node = TextNode(text, TextType.TEXT)
    nodes:list[TextNode] = [text_node]

    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    return nodes

