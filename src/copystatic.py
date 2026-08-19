from os import path, listdir, mkdir
from  shutil import rmtree, copy

static_path = "./static"
public_path = "./public"

def copy_static_to_public() -> None:

    public_path = path.abspath("public")

    if path.exists(public_path):
        rmtree(public_path)

    helper_copy_all_content_dirs(static_path, public_path)

def helper_copy_all_content_dirs(cur_path: str, dest: str) -> None:

    if not path.exists(dest):
        mkdir(dest)

    dir_items = listdir(cur_path)

    for item in dir_items:
        target_path = path.join(cur_path, item)

        new_dest = path.join(dest,item)
        if path.isfile(target_path):
            print(f" * {target_path} -> {new_dest}")
            copy(target_path, dest)
        else:
            helper_copy_all_content_dirs(target_path, new_dest)

