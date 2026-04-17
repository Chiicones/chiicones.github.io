import os, re
from datetime import datetime, timedelta

content_dir = r'C:\Users\chico\projetos\chiicones\content'

TODAY = datetime.today()

def fmt(dt):
    return dt.strftime('%d-%m-%Y')

def parse_date(s):
    s = s.strip()
    m = re.match(r'(\d{1,2})/(\d{2})/(\d{4})', s)
    if m:
        try: return datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
        except: pass
    m = re.match(r'(\d{4})-(\d{2})-(\d{2})', s)
    if m:
        try: return datetime(int(m.group(1)), int(m.group(2)), int(m.group(3)))
        except: pass
    return None

def extrair_tags_de_data(valor):
    valor = valor.strip()

    # "Ate DD/MM/AAAA" ou "Até DD/MM/AAAA"
    m = re.match(r'[Aa]t[eé]\s+(\d{1,2})/(\d{2})/(\d{4})', valor)
    if m:
        fim = parse_date(f"{m.group(1)}/{m.group(2)}/{m.group(3)}")
        if fim:
            tags = []
            d = TODAY
            while d <= fim:
                tags.append(fmt(d))
                d += timedelta(days=1)
            return tags

    # "DD/MM a DD/MM/AAAA" — meses diferentes ex: "20/03 a 29/04/2026"
    m = re.match(r'(\d{1,2})/(\d{2})\s+a\s+(\d{1,2})/(\d{2})/(\d{4})', valor)
    if m:
        inicio = parse_date(f"{m.group(1)}/{m.group(2)}/{m.group(5)}")
        fim = parse_date(f"{m.group(3)}/{m.group(4)}/{m.group(5)}")
        if inicio and fim:
            tags = []
            d = inicio
            while d <= fim:
                tags.append(fmt(d))
                d += timedelta(days=1)
            return tags

    # "DD a DD/MM/AAAA" — mesmo mes ex: "20 a 22/03/2026"
    m = re.match(r'(\d{1,2})\s+a\s+(\d{1,2})/(\d{2})/(\d{4})', valor)
    if m:
        inicio = parse_date(f"{m.group(1)}/{m.group(3)}/{m.group(4)}")
        fim = parse_date(f"{m.group(2)}/{m.group(3)}/{m.group(4)}")
        if inicio and fim:
            tags = []
            d = inicio
            while d <= fim:
                tags.append(fmt(d))
                d += timedelta(days=1)
            return tags

    # "20, 21 e 22/03/2026" — multiplos dias mesmo mes
    m = re.match(r'([\d,\s]+e\s+\d{1,2})/(\d{2})/(\d{4})', valor)
    if m:
        mes, ano = m.group(2), m.group(3)
        dias = re.findall(r'\d{1,2}', m.group(1))
        tags = []
        for dia in dias:
            dt = parse_date(f"{dia}/{mes}/{ano}")
            if dt:
                t = fmt(dt)
                if t not in tags:
                    tags.append(t)
        return tags

    # Uma ou mais datas DD/MM/AAAA
    datas = re.findall(r'(\d{1,2})/(\d{2})/(\d{4})', valor)
    if datas:
        tags = []
        for d in datas:
            dt = parse_date(f"{d[0]}/{d[1]}/{d[2]}")
            if dt:
                t = fmt(dt)
                if t not in tags:
                    tags.append(t)
        return tags

    return []

fixed = 0

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
    data_val = None
    tags_idx = None

    for i, line in enumerate(lines):
        if re.match(r'^Data:', line, re.I):
            data_val = re.sub(r'^Data:\s*', '', line, flags=re.I).strip()
        if re.match(r'^Tags:', line, re.I):
            tags_idx = i
        if line.strip() == '' and data_val:
            break

    if not data_val or tags_idx is None:
        continue

    novas_tags = extrair_tags_de_data(data_val)
    if not novas_tags:
        print(f"IGNORADO: {fname} — Data: {data_val}")
        continue

    current_tags = lines[tags_idx]
    added = []
    for tag in novas_tags:
        if tag not in current_tags:
            current_tags = current_tags.rstrip() + f', {tag}'
            added.append(tag)

    if added:
        lines[tags_idx] = current_tags
        open(path, 'w', encoding='utf-8').write('\n'.join(lines))
        print(f"{fname}: +{len(added)} tags ({', '.join(added[:3])}{'...' if len(added) > 3 else ''})")
        fixed += 1

print(f"\nTotal: {fixed} arquivos atualizados")