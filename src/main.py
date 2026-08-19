import shutil
import sys
from generate_html_page import generate_page, generate_pages_recursive
from textnode import TextNode, TextType
from copystatic import copy_static_to_public, helper_copy_all_content_dirs

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
dir_path_docs = "./docs"
template_path = "./template.html"

def main():
    text_node = TextNode("This is some anchor text", TextType.LINK,"https://www.boot.dev")

    base_url = "/"
    if len(sys.argv) > 1:
        base_url = sys.argv[1]

    copy_static_to_public(dir_path_static, dir_path_docs)
    generate_pages_recursive(dir_path_content, template_path, dir_path_docs, base_url)

if __name__ == "__main__":
    main()
