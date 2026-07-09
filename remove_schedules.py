import re

filepath = r"c:\_proekty\python\my_site\quartz\static\angiopikcha\сочи_2024\index.html"
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

content = re.sub(r'<details class="block">.*?</details>', '', content, flags=re.DOTALL)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)
print("Removed schedules from 2024 index.")
