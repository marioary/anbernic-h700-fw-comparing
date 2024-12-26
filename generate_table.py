import re

def parse_readme(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        content = file.read()

    sections = re.split(r"-{20,}", content)
    firmware_data = []

    for section in sections:
        lines = section.strip().splitlines()
        if len(lines) < 3:  # Skip small sections
            continue

        header = lines[0].strip()
        info_lines = [line.strip() for line in lines if line.startswith("### Info:")]
        pros_lines = [line.strip() for line in lines if line.startswith("### Pros:")]
        cons_lines = [line.strip() for line in lines if line.startswith("### Cons:")]

        firmware_data.append({
            "name": header,
            "info": "\n".join(info_lines),
            "pros": "\n".join(pros_lines),
            "cons": "\n".join(cons_lines),
        })
    return firmware_data


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
