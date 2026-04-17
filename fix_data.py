import os, re

content_dir = r'C:\Users\chico\projetos\chiicones\content'

dias = [
    'segunda-feira', 'terca-feira', 'terça-feira',
    'quarta-feira', 'quinta-feira', 'sexta-feira',
    'sabado', 'sábado', 'domingo',
    'segunda', 'terca', 'terça', 'quarta', 'quinta', 'sexta',
    r'\(seg\)', r'\(ter\)', r'\(qua\)', r'\(qui\)', r'\(sex\)', r'\(sab\)', r'\(sáb\)', r'\(dom\)',
    r'\(segunda\)', r'\(terça\)', r'\(quarta\)', r'\(quinta\)', r'\(sexta\)', r'\(sábado\)', r'\(domingo\)',
]

pattern = re.compile(
    r'(' + '|'.join(dias) + r')[,\s]*',
    re.IGNORECASE
)

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

    lines = content.split('\n')
    new_lines = []
    changed = False

    for line in lines:
        if re.match(r'^Data:', line, re.I):
            new_line = re.sub(pattern, '', line).strip()
            # Remove parênteses vazios ou só com espaços
            new_line = re.sub(r'\(\s*\)', '', new_line)
            # Remove espaços duplos
            new_line = re.sub(r'\s{2,}', ' ', new_line).strip()
            # Remove pontuação solta no final
            new_line = new_line.rstrip(' |,')
            if new_line != line:
                print(f"{fname}:")
                print(f"  ANTES:  {line}")
                print(f"  DEPOIS: {new_line}")
                changed = True
            new_lines.append(new_line)
        else:
            new_lines.append(line)

    if changed:
        open(path, 'w', encoding='utf-8').write('\n'.join(new_lines))
        fixed += 1

print(f"\nTotal: {fixed} arquivos corrigidos")