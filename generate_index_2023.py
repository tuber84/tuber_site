import os
import re
import glob

dir_path = r"c:\_proekty\python\my_site\quartz\static\angiopikcha\сочи_2023"
files = glob.glob(os.path.join(dir_path, "YT_*.html"))

days = {'26_мая_2023': [], '27_мая_2023': []}

for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    filename = os.path.basename(f)
    
    day_key = None
    for k in days.keys():
        if k in filename:
            day_key = k
            break
            
    if not day_key:
        continue
        
    room_title = "Зал"
    if 'Желтый' in filename: room_title = '🩸 Желтый зал'
    elif 'Зеленый' in filename: room_title = '🧒 Зеленый зал'
    elif 'Красный' in filename: room_title = '🧠 Красный зал'
    elif 'Синий' in filename: room_title = '🦶 Синий зал'

    # get main youtube link
    yt_match = re.search(r'<div class="src">🔗 <a href="(https://youtu\.be/[^"]+)"', content)
    yt_base = yt_match.group(1) if yt_match else "#"

    # get blocks
    blocks = []
    # look for <summary class="bname">1. Название<span class="bspan">1:20–50:20</span></summary>
    block_matches = re.finditer(r'<summary class="bname">(\d+\.\s+.*?)(<span class="bspan">([^<]+)</span>)?</summary>', content)
    
    for match in block_matches:
        title = match.group(1).strip()
        timespan = match.group(3)
        start_time_str = "0:00"
        if timespan:
            start_time_str = timespan.split('–')[0].split('-')[0].strip()
        
        # calculate seconds for the youtube link
        parts = start_time_str.split(':')
        seconds = 0
        if len(parts) == 3:
            seconds = int(parts[0])*3600 + int(parts[1])*60 + int(parts[2])
        elif len(parts) == 2:
            seconds = int(parts[0])*60 + int(parts[1])
            
        blocks.append({
            'title': title,
            'time_str': start_time_str,
            'seconds': seconds
        })
        
    days[day_key].append({
        'filename': filename,
        'room': room_title,
        'yt': yt_base,
        'blocks': blocks
    })

# Now generate HTML
html = """<!doctype html><html lang="ru"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>АнгиоПикча Сочи 2023</title>
<meta property="og:title" content="АнгиоПикча Сочи 2023 - Разбор записей">
<meta property="og:description" content="Скриншоты и кликабельные таймкоды. Внимание: анализ видео произведен алгоритмом, возможны неточности.">
<style>
:root{--bg:#0b0e14;--card:#151a24;--muted:#8b93a7;--fg:#e7ebf3;--acc:#e0231e;--navy:#1c3a73;}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);
font:16px/1.6 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif}
.wrap{max-width:1180px;margin:0 auto;padding:28px 20px 80px}
header{border-bottom:1px solid #262b36;padding-bottom:20px;margin-bottom:22px;
display:flex;align-items:center;gap:16px;background:linear-gradient(135deg,#111726,#0b0e14 60%);
border-radius:16px;padding:20px 24px;border:1px solid #232a3a}
header .brand{display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.wordmark{line-height:1.05}
.wordmark .angio{color:var(--acc);font-size:30px;font-weight:900;letter-spacing:.02em;
display:block;font-family:Arial Black,Arial,sans-serif}
.wordmark .picture{color:#dfe4ee;font-size:15px;font-weight:700;letter-spacing:.14em;display:block}
.wordmark .picture b{color:var(--navy);background:#dfe4ee;padding:0 4px;border-radius:3px}
.tags{color:var(--muted);font-size:13px;margin-top:8px}
.tag{background:#20242e;border-radius:6px;padding:2px 8px;margin-right:6px}
.tocswitch{display:flex;gap:6px;margin:0 0 22px}
.tsw{flex:1;background:#1b1f28;border:1px solid #2a2f3a;color:var(--muted);border-radius:10px;
padding:12px 8px;font-size:15px;font-weight:600;cursor:pointer;font-family:inherit}
.tsw.active{background:linear-gradient(135deg,#20242e,#1c2333);color:var(--fg);border-color:var(--acc)}
.rooms-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));gap:18px}
.card{background:var(--card);border:1px solid #232834;border-radius:14px;padding:16px 18px;
border-top:3px solid var(--theme-color, var(--navy));
box-shadow: inset 0 40px 50px -40px var(--theme-shadow, transparent);
transition: transform 0.25s cubic-bezier(0.4, 0, 0.2, 1), box-shadow 0.25s cubic-bezier(0.4, 0, 0.2, 1), border-color 0.25s ease;}
.card:hover{transform: translateY(-4px);
box-shadow: 0 12px 24px -12px var(--theme-shadow, rgba(0,0,0,0.5)), inset 0 40px 50px -40px var(--theme-shadow, transparent);
border-color: #333a4a; border-top-color: var(--theme-color, var(--navy));}
.card h3{margin:0 0 4px;font-size:18px; transition: color 0.2s ease;}
.card:hover h3{color: var(--theme-color, var(--fg));}
.card .roomlink{font-size:12px;color:var(--acc);text-decoration:none;font-weight:600}
.lectures{list-style:none;margin:10px 0 0;padding:0}
.lectures li{padding:6px 0;border-top:1px solid #232834;font-size:14px;display:flex;gap:8px;align-items:baseline}
.lectures li:first-child{border-top:none}
.ts{color:#7fb0ff;text-decoration:none;font-variant-numeric:tabular-nums;font-weight:600;flex-shrink:0}
.ts:hover{text-decoration:underline}
.lname{flex:1}
.miniref{color:var(--muted);text-decoration:none;flex-shrink:0}
.miniref:hover{color:var(--fg)}
@media(max-width:700px){header{flex-wrap:wrap}}
</style></head><body><div class="wrap"><header><div class="brand">
<svg viewBox="0 0 100 100" width="56" height="56" aria-hidden="true">
  <path d="M18 8 L34 34 L14 40 Z" fill="#132a52"/>
  <path d="M82 8 L66 34 L86 40 Z" fill="#132a52"/>
  <circle cx="50" cy="52" r="34" fill="#132a52"/>
  <ellipse cx="50" cy="60" rx="21" ry="17" fill="#f3f5f8"/>
  <circle cx="40" cy="52" r="7.5" fill="#f3f5f8"/>
  <circle cx="60" cy="52" r="7.5" fill="#f3f5f8"/>
  <circle cx="40" cy="53" r="4" fill="#132a52"/>
  <circle cx="60" cy="53" r="4" fill="#132a52"/>
  <circle cx="41.3" cy="51.6" r="1.3" fill="#fff"/>
  <circle cx="61.3" cy="51.6" r="1.3" fill="#fff"/>
  <ellipse cx="50" cy="63" rx="4" ry="2.6" fill="#132a52"/>
</svg>
<div class="wordmark"><span class="angio">ANGIO</span><span class="picture"><b>PICTURE</b> Сочи 2023</span></div></div><div><div class="tags" style="margin-top:0;font-size:15px;color:#dfe4ee;font-weight:600">АнгиоПикча Сочи 2023</div><div class="tags"><span class="tag">medicine</span><span class="tag">conference</span><span class="tag">endovascular</span> · 8 записей · 2 дня · скриншоты + кликабельные таймкоды на YouTube</div></div></header><div style="margin-bottom:18px;"><a href="../index.html" style="color:var(--muted); text-decoration:none; font-size:14px; display:inline-flex; align-items:center; gap:6px; background:#1b1f28; padding:8px 14px; border-radius:10px; border:1px solid #2a2f3a; font-weight:600; transition: color 0.2s, border-color 0.2s;" onmouseover="this.style.color='#e7ebf3'; this.style.borderColor='#4da6ff'" onmouseout="this.style.color='var(--muted)'; this.style.borderColor='#2a2f3a'">← Назад ко всем конференциям</a></div><div class="tocswitch"><button class="tsw active" data-day="26">26.05.23</button><button class="tsw " data-day="27">27.05.23</button></div>
"""

day_keys = [('26_мая_2023', '26'), ('27_мая_2023', '27')]

for (dk, did) in day_keys:
    display_style = ' style="display:none"' if did != '26' else ''
    html += f'<div id="day-{did}" class="daypanel"{display_style}><div class="rooms-grid">'
    
    # Sort rooms logically
    room_order = ['🩸 Желтый зал', '🧒 Зеленый зал', '🧠 Красный зал', '🦶 Синий зал']
    sorted_rooms = sorted(days[dk], key=lambda x: room_order.index(x['room']) if x['room'] in room_order else 99)
    
    for room in sorted_rooms:
        html += f'<section class="card"><h3>{room["room"]}</h3><a class="roomlink" href="{room["filename"]}" target="_blank" rel="noopener">📄 Открыть полный разбор ({len(room["blocks"])} тем)</a><ul class="lectures">'
        for b in room["blocks"]:
            html += f'<li><a class="ts" href="{room["yt"]}?t={b["seconds"]}s" target="_blank" rel="noopener">▶ {b["time_str"]}</a><span class="lname">{b["title"]}</span><a class="miniref" href="{room["filename"]}" target="_blank" rel="noopener" title="Открыть разбор">📄</a></li>'
        html += '</ul></section>'
        
    html += '</div></div>'

html += """<script>
document.querySelectorAll('.tsw').forEach(function(btn){
  btn.addEventListener('click', function(){
    document.querySelectorAll('.tsw').forEach(function(b){b.classList.remove('active');});
    btn.classList.add('active');
    document.querySelectorAll('.daypanel').forEach(function(p){p.style.display='none';});
    document.getElementById('day-' + btn.dataset.day).style.display = '';
  });
});
</script>
</body></html>"""

with open(os.path.join(dir_path, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(html)
print("Index generated successfully!")
