import os
import glob

dir_path = r'c:\_proekty\python\my_site\quartz\static\angiopikcha\сочи_2023'
files = glob.glob(os.path.join(dir_path, 'YT_*.html'))

old_str = '<h2>⭐ Самое ценное</h2>'
new_str = '<h2>⭐ Самое ценное</h2><div style=\"font-size:12px; color:var(--muted); margin: -2px 6px 12px; line-height:1.3; font-style:italic;\">⚠️ Звёзды и сортировка «по важности» — это результат экспериментального машинного анализа контента, а не экспертная оценка научной значимости докладов.</div>'

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    if old_str in content and new_str not in content:
        content = content.replace(old_str, new_str)
        with open(f, 'w', encoding='utf-8') as file:
            file.write(content)
        print(f'Updated {os.path.basename(f)}')
    else:
        print(f'Skipped {os.path.basename(f)}')
