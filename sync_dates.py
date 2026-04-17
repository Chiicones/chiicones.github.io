import os, re
from datetime import datetime

content_dir = r'C:\Users\chico\projetos\chiicones\content'

# Formatos de data para tentar parsear
formatos = [
    r'(\d{2}/\d{2}/\d{4})',   # 21/03/2026
    r'(\d{4}-\d{2}-\d{2})',   # 2026-03-21
]

def extrair_primeira_data(valor):
    """Extrai a primeira data encontrada no campo Data:"""
    # Tenta DD/MM/AAAA
    m = re.search(r'(\d{2})/(\d{2})/(\d{4})', valor)
    if m:
        try:
            return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except:
            pass
    # Tenta AAAA-MM-DD
    m = re.search(r'(\d{4})-(\d{2})-(\d{2})', valor)
    if m:
        try:
            return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except:
            pass
    # Tenta "06 a 08/03/2026" — pega a primeira data
    m = re.search(r'(\d{1,2})\s+a\s+\d{1,2}/(\d{2})/(\d{4})', valor)
    if m:
        try:
            return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except:
            pass
    # Tenta "Até DD/MM/AAAA"
    m = re.search(r'[Aa]t[eé]\s+(\d{2})/(\d{2})/(\d{4})', valor)
    if m:
        try:
            return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except:
            pass
    return None

fixed = 0
skipped = 0

for fname in sorted(os.listdir(content_dir)):
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
    data_valor = None
    date_idx = None

    for i, line in enumerate(lines):
        if re.match(r'^Data:', line, re.I):
            data_valor = re.sub(r'^Data:\s*', '', line, flags=re.I).strip()
        if re.match(r'^Date:', line, re.I):
            date_idx = i
        if line.strip() == '' and data_valor:
            break  # saiu do header

    if not data_valor or date_idx is None:
        skipped += 1
        continue

    nova_data = extrair_primeira_data(data_valor)
    if not nova_data:
        print(f"IGNORADO (não parseou data): {fname} — Data: {data_valor}")
        skipped += 1
        continue

    nova_date_str = nova_data.strftime('%Y-%m-%d')
    date_atual = re.sub(r'^Date:\s*', '', lines[date_idx], flags=re.I).strip()

    if date_atual == nova_date_str:
        continue  # já está correto

    lines[date_idx] = f'Date: {nova_date_str}'
    open(path, 'w', encoding='utf-8').write('\n'.join(lines))
    print(f"{fname}: {date_atual} → {nova_date_str}")
    fixed += 1

print(f"\nTotal: {fixed} corrigidos, {skipped} ignorados")
