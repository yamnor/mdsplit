import json
import sys
from datetime import datetime


def add_part(current_part, json_structure):
    # Adds the current part to the JSON structure and resets it
    if current_part:
        json_structure["sections"].append(current_part)
        current_part = None
    return current_part


def add_subsection(current_subsection, current_section):
    # Adds the current subsection to the current section and resets it
    if current_subsection:
        current_section["Chapter"]["sub_items"].append(current_subsection)
        current_section["Chapter"]["content"] += f"- [{current_subsection['Chapter']['name']}]({current_subsection['Chapter']['path']}.md)\n"
        current_subsection = None
    return current_subsection


def add_section(current_section, json_structure):
    # Adds the current section to the JSON structure and resets it
    if current_section:
        json_structure["sections"].append(current_section)
        current_section = None
    return current_section


def parse_markdown(content):
    # Parses markdown content and organizes it into a structured JSON format
    lines = content.split("\n")
    json_structure = {"sections": [], "__non_exhaustive": None}
    current_part = None
    current_section = None
    current_subsection = None
    section_count = 0
    subsection_count = 0
    page_count = 0

    for line in lines:
        if line.startswith("# "):
            # Detects a new part in the markdown
            current_part = {
                "PartTitle": line[2:],
            }
        elif line.startswith("## "):
            # Detects a new section in the markdown
            section_count += 1
            subsection_count = 0
            page_count += 1
            current_subsection = add_subsection(current_subsection, current_section)
            current_section = add_section(current_section, json_structure)
            current_part = add_part(current_part, json_structure)
            title = line[3:]
            path = f"{page_count}"
            if page_count == 1:
                path = "index"
            if " | " in line:
                title, path = line[3:].split(" | ")
            content = f"# {title}\n"
            current_section = {
                "Chapter": {
                    "name": title,
                    "content": content,
                    "number": [section_count],
                    "sub_items": [],
                    "parent_names": [],
                    "path": path,
                    "page": page_count,
                }
            }
        elif line.startswith("### "):
            # Detects a new subsection in the markdown
            subsection_count += 1
            page_count += 1
            current_subsection = add_subsection(current_subsection, current_section)
            title = line[4:]
            path = f"{page_count}"
            if page_count == 1:
                path = "index"
            if " | " in line:
                title, path = line[4:].split(" | ")
            content = f"## {title}\n"
            current_subsection = {
                "Chapter": {
                    "name": title,
                    "content": content,
                    "number": [section_count, subsection_count],
                    "sub_items": [],
                    "parent_names": [current_section["Chapter"]["name"]],
                    "path": path,
                    "page": page_count,
                }
            }
        else:
            # Handles regular content lines in the markdown
            content = f"{line}\n"
            if current_subsection is not None:
                current_subsection["Chapter"]["content"] += content
            elif current_section is not None:
                current_section["Chapter"]["content"] += content

    # Adds any remaining subsection and section to the JSON structure
    add_subsection(current_subsection, current_section)
    add_section(current_section, json_structure)

    return json_structure


if __name__ == "__main__":
    # Main execution: Parses markdown content and outputs structured JSON
    if len(sys.argv) > 1:
        if sys.argv[1] == "supports":
            sys.exit(0)

    context, book = json.load(sys.stdin)
    content = book["sections"][0]["Chapter"]["content"]
    splited_content = parse_markdown(content)
    print(json.dumps(splited_content))
