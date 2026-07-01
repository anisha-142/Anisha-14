import re

path = r'd:\Campusplacement\campusplacement\campusplacement\templates\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Pattern for the resources block.
# We want to join the lines inside the <a> tag start.
# Looking for occurrences of a href="... {% if not ... %} onclick="... " {% endif %}

def fix_link(match):
    # Join any newlines and extra spaces within the matched group
    return re.sub(r'\s+', ' ', match.group(0))

# We'll fix specifically the ones that are broken.
# 1. Hub / resources
content = re.sub(
    r'\{% if not\s+user\.is_authenticated\s+%\}onclick="[^"]+openLoginModal\(\'Study Materials Hub\', `\{% url \'resources\' %\} `\);"\s+\{% endif %\}',
    r"{% if not user.is_authenticated %}onclick=\"event.preventDefault(); openLoginModal('Study Materials Hub', `{% url 'resources' %}`);\" {% endif %}",
    content
)

# 2. Practice Arena
content = re.sub(
    r'\{% if not\s+user\.is_authenticated\s+%\}onclick="[^"]+openLoginModal\(\'Practice Arena\', `\{% url \'practice\' %\} `\);"\s+\{% endif %\}',
    r"{% if not user.is_authenticated %}onclick=\"event.preventDefault(); openLoginModal('Practice Arena', `{% url 'practice' %}`);\" {% endif %}",
    content
)

# 3. Video Tutorials
content = re.sub(
    r'\{% if not\s+user\.is_authenticated\s+%\}onclick="[^"]+openLoginModal\(\'Video Tutorials\', `\{% url \'video_resource\' %\} `\);"\s+\{% endif %\}',
    r"{% if not user.is_authenticated %}onclick=\"event.preventDefault(); openLoginModal('Video Tutorials', `{% url 'video_resource' %}`);\" {% endif %}",
    content
)

# Wait, the above might not match if there are weird quote issues or my regex is off.
# Let's try a simpler approach: finding the broken fragments and joining them.

# Fix broken tag starts:
content = re.sub(r'\{%\s+if not\s+user\.is_authenticated\s+%\}', r'{% if not user.is_authenticated %}', content)
content = re.sub(r'\{%\s+endif\s+%\}', r'{% endif %}', content)

# I suspect there might be some mess left from previous attempts.
# Let's look for specific mess:
content = content.replace('{% {%\n                    {% endif %}', '{% endif %}')
content = content.replace('{% {% endif %}', '{% endif %}')
content = content.replace('{% {%\n', '{%\n')

# Let's just reach for the known bad lines.
# Case 1: Resource 1
# Case 2: Resource 2
# Case 3: Resource 3

# I will use a very liberal search and replace for these three blocks.

# Resource 1:
res1_old = """<a href="{% if user.is_authenticated %}{% url 'resources' %}{% else %}#{% endif %}" {% if not
                    user.is_authenticated
                    %}onclick="event.preventDefault(); openLoginModal('Study Materials Hub', `{% url 'resources' %}`);" {% endif %}"""
res1_new = """<a href="{% if user.is_authenticated %}{% url 'resources' %}{% else %}#{% endif %}" {% if not user.is_authenticated %}onclick="event.preventDefault(); openLoginModal('Study Materials Hub', `{% url 'resources' %}`);" {% endif %}"""

# Resource 2:
res2_old = """<a href="{% if user.is_authenticated %}{% url 'practice' %}{% else %}#{% endif %}" {% if not
                    user.is_authenticated
                    %}onclick="event.preventDefault(); openLoginModal('Practice Arena', `{% url 'practice' %}`);" {% endif %}"""
res2_new = """<a href="{% if user.is_authenticated %}{% url 'practice' %}{% else %}#{% endif %}" {% if not user.is_authenticated %}onclick="event.preventDefault(); openLoginModal('Practice Arena', `{% url 'practice' %}`);" {% endif %}"""

# Resource 3:
res3_old = """<a href="{% if user.is_authenticated %}{% url 'video_resource' %}{% else %}#{% endif %}" {% if not
                    user.is_authenticated
                    %}onclick="event.preventDefault(); openLoginModal('Video Tutorials', `{% url 'video_resource' %}`);" {% endif %}"""
res3_new = """<a href="{% if user.is_authenticated %}{% url 'video_resource' %}{% else %}#{% endif %}" {% if not user.is_authenticated %}onclick="event.preventDefault(); openLoginModal('Video Tutorials', `{% url 'video_resource' %}`);" {% endif %}"""

# Join newlines just in case they are slightly different (spaces etc)
def normalize(s):
    return re.sub(r'\s+', ' ', s.strip())

# Since exact replacement is hard with spaces, I'll use a regex for each.

content = re.sub(
    r'<a href="\{% if user\.is_authenticated %\}\{% url \'resources\' %\}\{% else %\}#\{% endif %\}"\s+\{% if not\s+user\.is_authenticated\s+%\}onclick="event\.preventDefault\(\); openLoginModal\(\'Study Materials Hub\', `\{% url \'resources\' %\} `\);"\s+\{% endif %\}',
    res1_new,
    content,
    flags=re.MULTILINE
)

content = re.sub(
    r'<a href="\{% if user\.is_authenticated %\}\{% url \'practice\' %\}\{% else %\}#\{% endif %\}"\s+\{% if not\s+user\.is_authenticated\s+%\}onclick="event\.preventDefault\(\); openLoginModal\(\'Practice Arena\', `\{% url \'practice\' %\} `\);"\s+\{% endif %\}',
    res2_new,
    content,
    flags=re.MULTILINE
)

content = re.sub(
    r'<a href="\{% if user\.is_authenticated %\}\{% url \'video_resource\' %\}\{% else %\}#\{% endif %\}"\s+\{% if not\s+user\.is_authenticated\s+%\}onclick="event\.preventDefault\(\); openLoginModal\(\'Video Tutorials\', `\{% url \'video_resource\' %\} `\);"\s+\{% endif %\}',
    res3_new,
    content,
    flags=re.MULTILINE
)

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("COMPLETED")
