import os

directories = [
    r"c:\_proekty\python\my_site\quartz\static\angiopikcha\kazan_2025"
]

for directory in directories:
    if not os.path.exists(directory):
        continue
    for filename in os.listdir(directory):
        if filename.endswith(".html"):
            filepath = os.path.join(directory, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                continue

            new_content = content.replace('АнгиоПикча 12 — Казань 2025', 'АнгиоПикча 2025')
            new_content = new_content.replace('АнгиоПикча 12', 'АнгиоПикча 2025')
            new_content = new_content.replace('<span class="picture"><b>PICTURE</b> 12 — Казань 2025</span>', '<span class="picture"><b>PICTURE</b> 2025</span>')
            new_content = new_content.replace('<span class="picture"><b>PICTURE</b> 12</span>', '<span class="picture"><b>PICTURE</b> 2025</span>')

            if new_content != content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print(f"Updated {filename}")

print("Done.")
