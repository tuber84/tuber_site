import os
import re

directories = [
    r"c:\_proekty\python\my_site\quartz\static\angiopikcha\сочи_2024",
    r"c:\_proekty\python\my_site\quartz\static\angiopikcha\kazan_2025",
    r"c:\_proekty\python\my_site\quartz\static\angiopikcha\сочи_2023"
]

description = "Скриншоты и таймкоды докладов. Внимание: звёзды и сортировка — результат экспериментального ИИ-анализа, а не оценка научной значимости."

for directory in directories:
    if not os.path.exists(directory):
        continue
    for filename in os.listdir(directory):
        if filename.startswith("YT_") and filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                continue

            if 'property="og:description"' in content:
                print(f"Skipping {filename}, already has OG tags.")
                continue

            # Extract title
            title_match = re.search(r'<title>(.*?)</title>', content)
            title = title_match.group(1) if title_match else "АнгиоПикча - Разбор"

            og_tags = f'\n<meta property="og:title" content="{title}">\n<meta property="og:description" content="{description}">\n'

            # Inject after <head>
            content = content.replace('<head>', f'<head>{og_tags}', 1)

            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Added OG tags to {filename}")

print("Done.")
