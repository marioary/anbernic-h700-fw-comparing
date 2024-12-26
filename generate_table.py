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

        # Firmware adı ve bağlantısı
        name_match = re.search(r"## \[(.+?)\]\((.+?)\)", section)
        if name_match:
            name = name_match.group(1)
            link = name_match.group(2)
        else:
            continue  # Geçersiz bölüm

        # Info, Pros, ve Cons bölümleri
        info = clean_text(extract_section(section, "### Info:"))
        pros = clean_text(extract_section(section, "### Pros:"))
        cons = clean_text(extract_section(section, "### Cons:"))

        firmware_data.append({
            "name": f"[{name}]({link})",
            "info": info,
            "pros": pros,
            "cons": cons,
        })
    return firmware_data


def extract_section(content, section_header):
    """Belirli bir başlık altındaki içeriği çıkarır."""
    match = re.search(rf"{section_header}([\s\S]*?)(\n### |\Z)", content)
    return match.group(1).strip() if match else "N/A"


def clean_text(section_content):
    """Markdown tablosu için metni işler."""
    if section_content == "N/A":
        return "N/A"
    return section_content.replace("\n", "<br>").strip()


def create_markdown_table(data, output_file):
    """Firmware bilgileriyle Markdown tablosu oluşturur."""
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write("# Firmware Comparison Table\n\n")
        file.write("| Firmware | Info | Pros | Cons |\n")
        file.write("|----------|------|------|------|\n")

        for item in data:
            file.write(
                f"| {item['name']} | {item['info']} | {item['pros']} | {item['cons']} |\n"
            )


if __name__ == "__main__":
    input_readme = "README.md"  # Giriş dosyası adı
    output_readme = "README_new.md"  # Çıkış dosyası adı
    firmware_data = parse_readme(input_readme)
    create_markdown_table(firmware_data, output_readme)
