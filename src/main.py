import shutil

from textnode import TextNode, TextType
from  os    import path, listdir, mkdir
from shutil import copy, rmtree
from copystatic import copy_static_to_public

def main():
    text_node = TextNode("This is some anchor text", TextType.LINK,"https://www.boot.dev")
    copy_static_to_public()


if __name__ == "__main__":
    main()
