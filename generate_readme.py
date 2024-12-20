import re

with open("features.md", "r") as features_file:
    features_content = features_file.read()

info_pattern = r"## Info:\n(.*?)\n\n"
pros_pattern = r"## Pros:\n(.*?)\n\n"
cons_pattern = r"## Cons:\n(.*?)\n\n"

info_matches = re.findall(info_pattern, features_content, re.DOTALL)
pros_matches = re.findall(pros_pattern, features_content, re.DOTALL)
cons_matches = re.findall(cons_pattern, features_content, re.DOTALL)

readme_content = "# Feature Comparison\n\n| Info | Pros | Cons |\n|------|------|\n"

for pros, cons in zip(info_matches, pros_matches, cons_matches):
    readme_content += f"| {pros.strip().replace('\n', '<br>')} | {cons.strip().replace('\n', '<br>')} |\n"

with open("README_new.md", "w") as readme_file:
    readme_file.write(readme_content)
