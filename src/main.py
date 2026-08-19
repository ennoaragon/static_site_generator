import shutil
import os
from extract_title import extra_title_markdown
from generate_html_page import generate_page, generate_pages_recursive
from textnode import TextNode, TextType
from  os    import path, listdir, mkdir
from shutil import copy, rmtree
from copystatic import copy_static_to_public, helper_copy_all_content_dirs

dir_path_static = "./static"
dir_path_public = "./public"
dir_path_content = "./content"
template_path = "./template.html"

def main():
    text_node = TextNode("This is some anchor text", TextType.LINK,"https://www.boot.dev")

    #TODO: make it so this func takes in files
    copy_static_to_public()

    generate_pages_recursive(dir_path_content, template_path, dir_path_public)

 #   generate_page(os.path.join(dir_path_content, "index.md"), "template.html", os.path.join(dir_path_public, "index.html"))

 #   generate_page(os.path.join(dir_path_content, "blog/glorfindel/index.md"), "template.html", os.path.join(dir_path_public, "blog/glorfindel/index.html"))

 #   generate_page(os.path.join(dir_path_content, "blog/tom/index.md"), "template.html", os.path.join(dir_path_public, "blog/tom/index.html"))

 #   generate_page(os.path.join(dir_path_content, "blog/majesty/index.md"), "template.html", os.path.join(dir_path_public, "blog/majesty/index.html"))

 #   generate_page(os.path.join(dir_path_content, "contact/index.md"), "template.html", os.path.join(dir_path_public, "contact/index.html"))
if __name__ == "__main__":
    main()
