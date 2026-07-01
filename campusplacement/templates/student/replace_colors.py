import re
import os

filepath = 'home.html'

with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Replace variables in :root
content = content.replace('--primary: #6c63ff;', '--primary: #f59e0b;') # gold
content = content.replace('--primary2: #a78bfa;', '--primary2: #fbbf24;') # lighter gold
content = content.replace('--accent: #00d4ff;', '--accent: #f8fafc;') # white/slate
content = content.replace('--dark: #080818;', '--dark: #0f172a;') # jss blue
content = content.replace('--dark2: #0f0f28;', '--dark2: #1e293b;') # jss blue lighter
content = content.replace('--dark3: #171730;', '--dark3: #334155;')

# Replace RGBA values
# Purple 108,99,255 -> Gold 245,158,11
content = re.sub(r'108,\s*99,\s*255', '245,158,11', content)
# Hex purple
content = content.replace('#6c63ff', '#f59e0b')

# Cyan 0,212,255 -> Slate/White 248,250,252
content = re.sub(r'0,\s*212,\s*255', '248,250,252', content)

# Dark backgrounds
# 8,8,24 -> 15,23,42 (jss blue)
content = re.sub(r'8,\s*8,\s*24', '15,23,42', content)
# 15,15,40 -> 30,41,59 (slate-800)
content = re.sub(r'15,\s*15,\s*40', '30,41,59', content)
# Sidebar gradients
content = re.sub(r'20,\s*20,\s*48', '15,23,42', content)
content = re.sub(r'10,\s*10,\s*32', '2,6,23', content)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(content)

print("Replacement done.")
