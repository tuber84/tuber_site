import re

file_path = r'c:\_proekty\python\my_site\quartz\static\angiopikcha\index.html'

with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Using regex to remove the entire details block
# Starts with <details class="block"><summary>📅 Официальное расписание
# Ends with </details> before <div class="rooms-grid">

pattern = re.compile(r'<details class="block"><summary>📅 Официальное расписание 30\.05\.25.*?</details>', re.DOTALL)
new_content = pattern.sub('', content)

with open(file_path, 'w', encoding='utf-8') as f:
    f.write(new_content)

print('Done removing schedule')
