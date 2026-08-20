#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
corrigir_eventos.py
-------------------
Corrige arquivos .md de eventos com campos duplicados/vazios no cabeçalho.

Problema comum: o conversor gera campos vazios no topo e os valores reais
aparecem duplicados mais abaixo no arquivo (dentro do corpo do texto).

O script:
  1. Detecta campos vazios no cabeçalho
  2. Busca o valor no restante do arquivo
  3. Normaliza formatos de data (13 a 15/03/2026 → "13 a 15 de março de 2026")
  4. Remove as linhas duplicadas do corpo
  5. Salva o arquivo corrigido (sobrescreve ou em pasta separada)

Uso:
    python corrigir_eventos.py                      # corrige em /content, salva em /content-corrigido
    python corrigir_eventos.py --pasta content      # pasta de entrada
    python corrigir_eventos.py --inplace            # sobrescreve os originais (cuidado!)
    python corrigir_eventos.py --pasta content --inplace
"""

import os
import re
import sys
import argparse
import unicodedata
from pathlib import Path

# ─────────────────────────────────────────────
# Meses em português para conversão de datas
# ─────────────────────────────────────────────
MESES = {
    "01": "janeiro", "02": "fevereiro", "03": "março",
    "04": "abril",   "05": "maio",      "06": "junho",
    "07": "julho",   "08": "agosto",    "09": "setembro",
    "10": "outubro", "11": "novembro",  "12": "dezembro",
}

VERDE    = "\033[92m"
AMARELO  = "\033[93m"
VERMELHO = "\033[91m"
NEGRITO  = "\033[1m"
RESET    = "\033[0m"

# Todos os campos reconhecidos no cabeçalho
TODOS_CAMPOS = ["Title", "Date", "Category", "Tags", "Local", "Data", "Horario", "Entrada", "Slug"]

# ─────────────────────────────────────────────
# Helpers de data
# ─────────────────────────────────────────────

def normalizar_data(valor: str) -> str:
    """
    Converte formatos variados para texto legível.
    Exemplos:
        07/03/2026            → 7 de março de 2026
        13 a 15/03/2026       → 13 a 15 de março de 2026
        13 a 15/03/2026       → 13 a 15 de março de 2026
        2026-03-07            → já está ok, retorna como está
    """
    v = valor.strip()

    # Já está no formato texto ("7 de março de 2026") → não mexe
    if re.search(r'[a-zA-ZÀ-ú]', v):
        return v

    # Formato AAAA-MM-DD (Pelican Date) → não mexe
    if re.match(r'^\d{4}-\d{2}-\d{2}$', v):
        return v

    # "13 a 15/03/2026"
    m = re.match(r'^(\d{1,2})\s+a\s+(\d{1,2})[/\-](\d{2})[/\-](\d{4})$', v)
    if m:
        d1, d2, mes, ano = m.groups()
        return f"{int(d1)} a {int(d2)} de {MESES.get(mes, mes)} de {ano}"

    # "07/03/2026" ou "07-03-2026"
    m = re.match(r'^(\d{1,2})[/\-](\d{2})[/\-](\d{4})$', v)
    if m:
        dia, mes, ano = m.groups()
        return f"{int(dia)} de {MESES.get(mes, mes)} de {ano}"

    return v  # retorna como veio se não reconheceu


# ─────────────────────────────────────────────
# Leitura
# ─────────────────────────────────────────────

def ler_arquivo(caminho: Path):
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return caminho.read_text(encoding=enc)
        except (UnicodeDecodeError, ValueError):
            continue
    return None


# ─────────────────────────────────────────────
# Parser de campos (aceita duplicatas)
# ─────────────────────────────────────────────

def extrair_todos_campos(linhas: list) -> dict:
    """
    Percorre todas as linhas e coleta TODOS os valores de cada campo.
    Retorna dict: campo → lista de valores não-vazios encontrados.
    """
    encontrados = {}
    for linha in linhas:
        m = re.match(r'^([A-Za-zÀ-ú/_]+):\s*(.*)', linha)
        if m:
            campo = m.group(1).strip()
            valor = m.group(2).strip()
            if campo in TODOS_CAMPOS and valor:
                encontrados.setdefault(campo, []).append(valor)
    return encontrados


# ─────────────────────────────────────────────
# Correção principal
# ─────────────────────────────────────────────

def corrigir(conteudo: str) -> tuple[str, list]:
    """
    Retorna (conteudo_corrigido, lista_de_acoes).
    """
    acoes = []
    linhas = conteudo.replace("\r\n", "\n").splitlines()

    # Coleta todos os valores de todos os campos no arquivo inteiro
    todos = extrair_todos_campos(linhas)

    # ── Monta o cabeçalho corrigido ──────────────────────────────
    novo_cabecalho = []
    # Rastreia quais campos já foram escritos no cabeçalho
    cabecalho_escrito = {}

    # Processa linha a linha até a primeira linha em branco real
    # (depois que todos os campos forem resolvidos)
    i = 0
    cabecalho_terminou = False

    for i, linha in enumerate(linhas):
        # Detecta fim do cabeçalho (linha em branco após pelo menos Title)
        if not linha.strip() and "Title" in cabecalho_escrito:
            cabecalho_terminou = True
            break

        m = re.match(r'^([A-Za-zÀ-ú/_]+):\s*(.*)', linha)
        if not m:
            # linha estranha antes do fim do cabeçalho — ignora
            continue

        campo = m.group(1).strip()
        valor_atual = m.group(2).strip()

        if campo not in TODOS_CAMPOS:
            continue

        # Ignora campo "Slug" — não queremos no cabeçalho final
        if campo == "Slug":
            continue

        # Se já escrevemos este campo, pula (evita duplicata no cabeçalho)
        if campo in cabecalho_escrito:
            continue

        # Se o valor está vazio, pega do pool coletado
        if not valor_atual:
            valores_disponiveis = todos.get(campo, [])
            if valores_disponiveis:
                valor_final = valores_disponiveis[0]
                acoes.append(f"Campo '{campo}' vazio → preenchido com '{valor_final}'")
            else:
                valor_final = ""
                acoes.append(f"Campo '{campo}' vazio → nenhum valor encontrado no arquivo")
        else:
            valor_final = valor_atual

        # Normaliza Data (não o campo Date do Pelican, só o nosso "Data")
        if campo == "Data" and valor_final:
            valor_norm = normalizar_data(valor_final)
            if valor_norm != valor_final:
                acoes.append(f"Data normalizada: '{valor_final}' → '{valor_norm}'")
                valor_final = valor_norm

        novo_cabecalho.append(f"{campo}: {valor_final}")
        cabecalho_escrito[campo] = valor_final

    # ── Corpo: remove linhas duplicadas de campos ────────────────
    # Tudo após o cabeçalho
    resto_linhas = linhas[i+1:] if cabecalho_terminou else linhas[i:]

    corpo_limpo = []
    for linha in resto_linhas:
        m = re.match(r'^([A-Za-zÀ-ú/_]+):\s*(.*)', linha)
        if m and m.group(1).strip() in TODOS_CAMPOS:
            # É uma linha de campo duplicado no corpo — remove
            acoes.append(f"Linha duplicada removida do corpo: '{linha.strip()}'")
            continue
        corpo_limpo.append(linha)

    # Remove linhas em branco extras no início do corpo
    while corpo_limpo and not corpo_limpo[0].strip():
        corpo_limpo.pop(0)

    # ── Monta resultado final ────────────────────────────────────
    resultado = "\n".join(novo_cabecalho) + "\n\n" + "\n".join(corpo_limpo)

    # Garante que não termine com espaços em branco excessivos
    resultado = resultado.rstrip() + "\n"

    return resultado, acoes


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Corrige campos duplicados/vazios em arquivos .md de eventos.")
    parser.add_argument("--pasta",   "-p", default="content",           help="Pasta com os .md (padrão: content/)")
    parser.add_argument("--saida",   "-s", default="content-corrigido", help="Pasta de saída (padrão: content-corrigido/)")
    parser.add_argument("--inplace", "-i", action="store_true",         help="Sobrescreve os originais")
    args = parser.parse_args()

    pasta_entrada = Path(args.pasta)
    if not pasta_entrada.exists():
        print(f"{VERMELHO}Pasta não encontrada: {pasta_entrada}{RESET}")
        sys.exit(1)

    if args.inplace:
        pasta_saida = pasta_entrada
    else:
        pasta_saida = Path(args.saida)
        pasta_saida.mkdir(parents=True, exist_ok=True)

    arquivos = sorted(pasta_entrada.glob("*.md"))
    if not arquivos:
        print(f"{AMARELO}Nenhum .md encontrado em '{pasta_entrada}'.{RESET}")
        sys.exit(0)

    print(f"\nProcessando {len(arquivos)} arquivo(s) em '{pasta_entrada}'...\n")

    corrigidos = 0
    sem_alteracao = 0
    erros = 0

    for caminho in arquivos:
        conteudo = ler_arquivo(caminho)
        if conteudo is None:
            print(f"  {VERMELHO}❌ {caminho.name} — não foi possível ler{RESET}")
            erros += 1
            continue

        novo_conteudo, acoes = corrigir(conteudo)

        destino = pasta_saida / caminho.name
        destino.write_text(novo_conteudo, encoding="utf-8-sig")

        if acoes:
            print(f"  {VERDE}✅ {caminho.name}{RESET}")
            for a in acoes:
                print(f"     {AMARELO}→ {a}{RESET}")
            corrigidos += 1
        else:
            print(f"  {VERDE}✅ {caminho.name}{RESET} (sem alterações)")
            sem_alteracao += 1

    print(f"\n{'─'*60}")
    print(f"{NEGRITO}  Total: {len(arquivos)} | Corrigidos: {corrigidos} | Sem alteração: {sem_alteracao} | Erros: {erros}{RESET}")
    if not args.inplace:
        print(f"  Arquivos salvos em: {pasta_saida}/")
    print(f"{'─'*60}\n")


if __name__ == "__main__":
    main()
