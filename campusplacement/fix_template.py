path = r'd:\Campusplacement\campusplacement\campusplacement\templates\index.html'
with open(path, 'rb') as f:
    d = f.read()
target = b' %}`);" {%\r\n                    {% endif %}'
replacement = b' %}`);" {% endif %}'
if target not in d:
    target = b' %}`);" {%\n                    {% endif %}'
new_d = d.replace(target, replacement)
with open(path, 'wb') as f:
    f.write(new_d)
print("REPLACED" if new_d != d else "NOT FOUND")
