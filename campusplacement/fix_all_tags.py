import os

path = r'd:\Campusplacement\campusplacement\campusplacement\templates\index.html'
with open(path, 'rb') as f:
    content = f.read()

# Fix occurrences of split tags.
# We're looking for patterns like `{% \n {% endif %}` and joining them.
# The previous multi-replace mistake created a extra `{%` and potentially a newline.

# Fixing Study Materials Hub (Resource 1)
t1 = b" Hub', `{% url 'resources' %}`);\"\n                    {% endif %}"
r1 = b" Hub', `{% url 'resources' %}`);\" {% endif %}"

# Fixing Video Tutorials (Resource 3)
t3 = b" Tutorials', `{% url 'video_resource' %}`);\"\n                    {% endif %}"
r3 = b" Tutorials', `{% url 'video_resource' %}`);\" {% endif %}"

new_content = content
for t, r in [(t1, r1), (t3, r3)]:
    new_content = new_content.replace(t, r)
    # Also try with \r\n
    t_cr = t.replace(b'\n', b'\r\n')
    new_content = new_content.replace(t_cr, r)

if new_content != content:
    with open(path, 'wb') as f:
        f.write(new_content)
    print("FIXED")
else:
    print("NO CHANGE")
