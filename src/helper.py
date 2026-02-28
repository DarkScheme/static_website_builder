from markdown_blocks import markdown_to_html_node
import os
import shutil
from pathlib import Path


def copy_files_recursive(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    for filename in os.listdir(source_dir_path):
        from_path = os.path.join(source_dir_path, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_files_recursive(from_path, dest_path)



def extract_title(markdown):
    new_lines = markdown.split("\n")
    for new_line in new_lines:
        if new_line[0:2] == "# ":
            return new_line[2:]


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")

    with open(from_path, "r", encoding="utf-8") as f:
        read_md_from = f.read()

    with open(template_path, "r", encoding="utf-8") as f:
        read_template = f.read()

    html_string = markdown_to_html_node(read_md_from).to_html()
    title = extract_title(read_md_from)
    replaced_html = read_template.replace("{{ Title }}", title)
    replaced_html = replaced_html.replace("{{ Content }}", html_string)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(replaced_html)


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    listed_entries_in_dir = os.listdir(dir_path_content)
    for entry_str in listed_entries_in_dir:
        entry = os.path.join(dir_path_content, entry_str)
        desty = os.path.join(dest_dir_path, entry_str)
        if os.path.isfile(entry):
            desty = Path(desty).with_suffix(".html")
            generate_page(entry, template_path, desty)
        else:
            generate_pages_recursive(entry, template_path, desty)
