import re

def parse_readme_by_lines(input_file):
    """README dosyasını satır satır işleyerek firmware bilgilerini ayıklar."""
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    firmware_data = []
    general_info = []
    current_firmware = {}
    section = None
    capturing_general_info = True  # Genel bilgileri toplamak için flag

    for line in lines:
        line = line.strip()
        if capturing_general_info:
            if line.startswith("## ["):  # Firmware bilgileri başladığında genel bilgileri durdur
                capturing_general_info = False
            else:
                general_info.append(line)
                continue

        if line.startswith("## [") and "](" in line:  # Firmware başlığı
            if current_firmware:  # Önceki firmware'yi kaydet
                firmware_data.append(current_firmware)
                current_firmware = {}

            # Firmware adı ve bağlantısı
            name, link = re.findall(r"\[(.+?)\]\((.+?)\)", line)[0]
            current_firmware['name'] = f"[{name}]({link})"
            current_firmware['info'] = ""
            current_firmware['pros'] = ""
            current_firmware['cons'] = ""
        elif line.startswith("### Info:"):
            section = 'info'
        elif line.startswith("### Pros:"):
            section = 'pros'
        elif line.startswith("### Cons:"):
            section = 'cons'
        elif line.startswith("--------------------"):  # Çizgili satırı yok say
            section = None
        elif section and line:  # Aktif bölümde içerik varsa ekle
            current_firmware[section] += line + "<br>"

    if current_firmware:  # Son firmware'yi ekle
        firmware_data.append(current_firmware)

    return general_info, firmware_data


def create_markdown_table_with_general_info(general_info, firmware_data, output_file):
    """Firmware bilgileriyle Markdown tablosu oluşturur ve genel bilgileri ekler."""
    with open(output_file, 'w', encoding='utf-8') as file:
        # Genel bilgileri yaz
        for line in general_info:
            file.write(line + "\n")
        file.write("\n")

        # Tablo başlığı
        file.write("# Firmware Comparison Table\n\n")
        file.write("| Firmware | Info | Pros | Cons |\n")
        file.write("|:---------|:-----|:-----|:-----|\n")  # Ortalanmış sütunlar

        # Tablo satırları
        for item in firmware_data:
            file.write(
                f"| {item['name']} | {item['info'].strip()} | {item['pros'].strip()} | {item['cons'].strip()} |\n"
            )


if __name__ == "__main__":
    input_readme = "README.md"  # Giriş dosyası adı
    output_readme = "README_new.md"  # Çıkış dosyası adı
    general_info, firmware_data = parse_readme_by_lines(input_readme)
    create_markdown_table_with_general_info(general_info, firmware_data, output_readme)
