import re

def parse_readme(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    sections = re.split(r"\n-{20,}\n", content)  # Bölümleri ayır
    firmware_data = []

    for section in sections:
        lines = section.strip().splitlines()
        if not lines or len(lines) < 2:
            continue

        # Firmware adı
        name_match = re.search(r"## \[(.+?)\]\((.+?)\)", section)
        name = name_match.group(1) if name_match else "Unknown"
        link = name_match.group(2) if name_match else "#"

        # Info, Pros, ve Cons bölümleri
        info = extract_section(section, "### Info:")
        pros = extract_section(section, "### Pros:")
        cons = extract_section(section, "### Cons:")

        firmware_data.append({
            "name": f"[{name}]({link})",
            "info": info,
            "pros": pros,
            "cons": cons,
        })
    return firmware_data


def extract_section(content, section_header):
    match = re.search(rf"{section_header}([\s\S]*?)(\n### |\Z)", content)
    return match.group(1).strip() if match else "N/A"


def create_markdown_table(data, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("# Firmware Comparison Table\n\n")
        file.write("| Firmware | Info | Pros | Cons |\n")
        file.write("|----------|------|------|------|\n")

        for item in data:
            file.write(f"| {item['name']} | {item['info']} | {item['pros']} | {item['cons']} |\n")


if __name__ == "__main__":
    input_readme = "README.md"
    output_readme = "README_new.md"
    firmware_data = parse_readme(input_readme)
    create_markdown_table(firmware_data, output_readme)
