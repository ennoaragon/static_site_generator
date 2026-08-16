from textnode import TextNode, TextType

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

        split_text= node.text.split(delimiter)

        if len(split_text) % 2 == 0:
            raise ValueError("No closing delimiter is found, invalid Markdown syntax")

        count = 0
        for text in split_text:
            if text == "":
                count += 1
                continue

            if count%2 == 1:
                new_nodes.append(TextNode(text, DelimiterMap[delimiter]))
            else:
                new_nodes.append(TextNode(text, TextType.TEXT ))

            count += 1

    return new_nodes


# the code below is half complete, but more usefule for nested inline version of the problem
# it requires a stack to verify  the nested inlines are completed,
# needs the DelimiterMap to be included, which is missing
#

    #    i, j = 0,0
    #    while  i < len(node.text) and j < len(node.text):

    #        # we need to make sure that we can take account of double like **
    #        if node.text[j] == delimiter:
    #            new_nodes.append(TextNode(node.text[i:j], TextType.TEXT))
    #            j += 1
    #            i = j
    #            while node.text[j] != delimiter:
    #                j += 1
    #                if j >= len(node.text):
    #                    raise Exception("No closing delimiter is found, invalid Markdown syntax")

    #            new_nodes.append(TextNode(node.text[i:j], TextType.CODE))

    #            i = j+1
    #            new_nodes.append(TextNode(node.text[i:], TextType.CODE))

    #            i, j = len(node.text), len(node.text)

    #        j += 1

