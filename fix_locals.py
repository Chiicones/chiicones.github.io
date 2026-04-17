import os, re

content_dir = r'C:\Users\chico\projetos\chiicones\content'

fixed = 0
for fname in os.listdir(content_dir):
    if not fname.endswith('.md'):
        continue
    path = os.path.join(content_dir, fname)
    
    content = None
    for enc in ['utf-8', 'latin-1', 'cp1252']:
        try:
            content = open(path, encoding=enc).read()
            break
        except:
            continue
    if content is None:
        continue

    # Remove any line starting with Local: that appears AFTER the first blank line (i.e. in the body)
    header_end = content.find('\n\n')
    if header_end == -1:
        continue
    
    header = content[:header_end]
    body = content[header_end:]
    
    # Remove Local: lines from body
    new_body = re.sub(r'\n+Local:.*$', '', body, flags=re.MULTILINE)
    
    if new_body != body:
        open(path, 'w', encoding='utf-8').write(header + new_body)
        print(f"Fixed: {fname}")
        fixed += 1

print(f"\nTotal: {fixed} arquivos corrigidos")
