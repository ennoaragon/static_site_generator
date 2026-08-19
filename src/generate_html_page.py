import os

from extract_title import extra_title_markdown
from markdown_to_blocks import markdown_to_blocks, markdown_to_html_node


def generate_pages_recursive(dir_path_content: str, template_path, dest_dir_path, baseurl: str) -> None:

    dir_items = os.listdir(dir_path_content)

    for item in dir_items:
        target_path = os.path.join(dir_path_content, item)

        new_dest = os.path.join(dest_dir_path,item)
        if os.path.isfile(target_path):
            print(f" * {target_path} -> {new_dest}")
            generate_page(target_path, template_path, os.path.join(dest_dir_path, "index.html"), baseurl)
        else:
            generate_pages_recursive(target_path, template_path,  new_dest, baseurl)

    pass



def generate_page(from_path: str, template_path: str, dest_path: str, baseurl: str) -> None:

    print(f"from_path: {from_path}, template_path: {template_path}, dest_path: {dest_path}")
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    from_file = open(from_path, "r")
    file_contents = from_file.read()
    from_file.close()

    html_node = markdown_to_html_node(file_contents)

    contents = html_node.to_html()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    title = extract_title(file_contents)
    template = template.replace("{{ Title }}", title )

    file_completed = template.replace("{{ Content }}", contents )

    if baseurl != "/":
        file_completed = file_completed.replace('href="/', f'href="{baseurl}')
        file_completed = file_completed.replace('src="/', f'src="{baseurl}')

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(file_completed)

def extract_title(md: str) -> str:
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("no title found")
