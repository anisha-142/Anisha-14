import re

path = r'd:\Campusplacement\campusplacement\campusplacement\templates\index.html'
with open(path, 'r', encoding='utf-8') as f:
    content = f.read()

# Resource 1: Study Materials
old1 = r'<!-- Resource Card 1: Study Materials -->\s+<a href="\{% if user\.is_authenticated %\}\{% url \'resources\' %\}\{% else %\}#\{% endif %\}"\s+\{% if not user\.is_authenticated %\}onclick="event\.preventDefault\(\); openLoginModal\(\'Study Materials Hub\', `\{% url \'resources\' %\} `\);"\s+\{% endif %\}\s+class="group'
new1 = r'''<!-- Resource Card 1: Study Materials -->
                {% if user.is_authenticated %}
                <a href="{% url 'resources' %}"
                {% else %}
                <a href="#" onclick="event.preventDefault(); openLoginModal('Study Materials Hub', `{% url 'resources' %}`);"
                {% endif %}
                    class="group'''

# Resource 2: Practice Arena
old2 = r'<!-- Resource Card 2: Practice Arena -->\s+<a href="\{% if user\.is_authenticated %\}\{% url \'practice\' %\}\{% else %\}#\{% endif %\}"\s+\{% if not user\.is_authenticated %\}onclick="event\.preventDefault\(\); openLoginModal\(\'Practice Arena\', `\{% url \'practice\' %\} `\);"\s+\{% endif %\}\s+class="group'
new2 = r'''<!-- Resource Card 2: Practice Arena -->
                {% if user.is_authenticated %}
                <a href="{% url 'practice' %}"
                {% else %}
                <a href="#" onclick="event.preventDefault(); openLoginModal('Practice Arena', `{% url 'practice' %}`);"
                {% endif %}
                    class="group'''

# Resource 3: Video Tutorials
old3 = r'<!-- Resource Card 3: Video Tutorials -->\s+<a href="\{% if user\.is_authenticated %\}\{% url \'video_resource\' %\}\{% else %\}#\{% endif %\}"\s+\{% if not user\.is_authenticated %\}onclick="event\.preventDefault\(\); openLoginModal\(\'Video Tutorials\', `\{% url \'video_resource\' %\} `\);"\s+\{% endif %\}\s+class="group'
new3 = r'''<!-- Resource Card 3: Video Tutorials -->
                {% if user.is_authenticated %}
                <a href="{% url 'video_resource' %}"
                {% else %}
                <a href="#" onclick="event.preventDefault(); openLoginModal('Video Tutorials', `{% url 'video_resource' %}`);"
                {% endif %}
                    class="group'''

# Using a simpler re.sub for safety, since the exact strings might vary with spaces.
# I will just find the blocks and replace them.

def fix_resource(content, tag_name, url_name, modal_title):
    pattern = r'<!-- Resource Card \d: ' + re.escape(tag_name) + r' -->\s+<a href="[^"]+"\s+[^>]+class="group'
    
    # Let's just do a direct string replace for the components I know are bad.
    # The view_file output showed:
    # <a href="{% if user.is_authenticated %}{% url 'resources' %}{% else %}#{% endif %}" {% if not user.is_authenticated %}onclick="event.preventDefault(); openLoginModal('Study Materials Hub', `{% url 'resources' %}`);" {% endif %}
    
    match_str = f'''<a href="{{% if user.is_authenticated %}}{{% url '{url_name}' %}}{{% else %}}#{{% endif %}}" {{% if not user.is_authenticated %}}onclick="event.preventDefault(); openLoginModal('{modal_title}', `{{% url '{url_name}' %}}`);" {{% endif %}}'''
    
    replacement = f'''{{% if user.is_authenticated %}}
                <a href="{{% url '{url_name}' %}}"
                {{% else %}}
                <a href="#" onclick="event.preventDefault(); openLoginModal('{modal_title}', `{{% url '{url_name}' %}}`);"
                {{% endif %}}'''
    
    # We need to account for slight variation in spaces/quotes in the actual file.
    # But since I just wrote it with fix_tags_v3, it should be exact.
    
    return content.replace(match_str, replacement)

content = fix_resource(content, "Study Materials", "resources", "Study Materials Hub")
content = fix_resource(content, "Practice Arena", "practice", "Practice Arena")
content = fix_resource(content, "Video Tutorials", "video_resource", "Video Tutorials")

with open(path, 'w', encoding='utf-8') as f:
    f.write(content)
print("REPLACEMENT COMPLETED")
