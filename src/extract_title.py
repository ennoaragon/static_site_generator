import os

from markdown_to_blocks import markdown_to_blocks


def extra_title_markdown(file_path: str) -> str:
    # need to read first line and verify if it's the correct time,
    # maybe use the md to block, perhaps it isn't what we need and just check it here
    # raise exception

    abs_path = os.path.abspath(file_path)

    text = ""
    with open(abs_path, "r") as f:
        first_line = f.readline()
        if not first_line.startswith("# "):
            raise Exception(f"the given {file_path} doesn't have a title or is empty")

        text = first_line

    if len(text) < 3:
        raise Exception(f"the given {file_path} doesn't have a title or is empty")




    return text[2:].strip()


