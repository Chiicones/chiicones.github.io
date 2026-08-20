#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validar_eventos.py
------------------
Valida arquivos .md de eventos para o Pelican antes de publicar.

Uso:
    python validar_eventos.py
    python validar_eventos.py --pasta minha_pasta_content

Requisitos: Python 3.7+, sem dependências externas.
"""

import os
import re
import sys
import argparse
from datetime import datetime
from pathlib import Path

# ─────────────────────────────────────────────
# Configuração
# ─────────────────────────────────────────────

CAMPOS_OBRIGATORIOS = ["Title", "Date", "Category", "Local", "Data", "Horario", "Entrada"]
CAMPOS_LINKS        = ["Instagram", "Site/Ingressos", "Programação", "WhatsApp"]
FORMATO_DATE        = "%Y-%m-%d"

# Caracteres que indicam encoding corrompido (latin-1 lido como UTF-8)
PADROES_CORROMPIDOS = ["â€", "Ã§", "Ã£", "Ã©", "Ã¡", "Ã­", "Ã³", "Ãº", "â€™", "â€œ"]

# Cores ANSI para o terminal
VERDE   = "\033[92m"
AMARELO = "\033[93m"
VERMELHO= "\033[91m"
NEGRITO = "\033[1m"
RESET   = "\033[0m"

# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def ler_arquivo(caminho: Path):
    """Lê o arquivo tentando UTF-8, depois latin-1."""
    for enc in ("utf-8-sig", "utf-8", "latin-1"):
        try:
            return caminho.read_text(encoding=enc), enc
        except (UnicodeDecodeError, ValueError):
            continue
    return None, None


def extrair_metadados(conteudo: str) -> dict:
    """Extrai campos chave:valor do cabeçalho Pelican."""
    meta = {}
    for linha in conteudo.splitlines():
        if not linha.strip():
            break  # cabeçalho termina na primeira linha em branco
        m = re.match(r"^([^:]+):\s*(.*)", linha)
        if m:
            meta[m.group(1).strip()] = m.group(2).strip()
    return meta


def extrair_corpo(conteudo: str) -> str:
    """Retorna o texto após o cabeçalho (após a primeira linha em branco)."""
    partes = re.split(r"\n\s*\n", conteudo, maxsplit=1)
    return partes[1].strip() if len(partes) > 1 else ""


def gerar_slug(titulo: str) -> str:
    """Gera slug a partir do título (igual ao converter.py)."""
    import unicodedata
    s = unicodedata.normalize("NFKD", titulo)
    s = s.encode("ascii", "ignore").decode("ascii")
    s = s.lower()
    s = re.sub(r"[^\w\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    s = re.sub(r"-+", "-", s).strip("-")
    return s


def slug_esperado(titulo: str) -> str:
    return gerar_slug(titulo) + ".md"


# ─────────────────────────────────────────────
# Validação
# ─────────────────────────────────────────────

def validar_arquivo(caminho: Path) -> dict:
    """
    Retorna dict com:
        erros   → lista de strings (bloqueadores)
        avisos  → lista de strings (não bloqueadores)
        links_vazios → lista de campos de link em branco
    """
    erros, avisos, links_vazios = [], [], []

    # 1. Leitura e encoding
    conteudo, enc = ler_arquivo(caminho)
    if conteudo is None:
        erros.append("Não foi possível ler o arquivo (encoding desconhecido)")
        return {"erros": erros, "avisos": avisos, "links_vazios": links_vazios}

    if enc == "latin-1":
        avisos.append(f"Arquivo lido em latin-1 — considere salvar em UTF-8")

    # 2. Caracteres corrompidos
    for padrao in PADROES_CORROMPIDOS:
        if padrao in conteudo:
            erros.append(f"Possível encoding corrompido — encontrado '{padrao}'")
            break

    # 3. Normalização \r\n
    if "\r\n" in conteudo:
        avisos.append("Quebras de linha Windows (\\r\\n) detectadas — converter para \\n")

    # 4. Metadados
    meta = extrair_metadados(conteudo)

    for campo in CAMPOS_OBRIGATORIOS:
        if campo not in meta:
            erros.append(f"Campo obrigatório ausente: '{campo}'")
        elif not meta[campo]:
            erros.append(f"Campo obrigatório vazio: '{campo}'")

    # 5. Formato do Date
    if "Date" in meta and meta["Date"]:
        try:
            datetime.strptime(meta["Date"], FORMATO_DATE)
        except ValueError:
            erros.append(f"Campo 'Date' com formato inválido: '{meta['Date']}' (esperado AAAA-MM-DD)")

    # 6. Tags em lowercase
    if "Tags" in meta and meta["Tags"]:
        tags = [t.strip() for t in meta["Tags"].split(",")]
        tags_erradas = [t for t in tags if t != t.lower()]
        if tags_erradas:
            avisos.append(f"Tags com maiúsculas: {', '.join(tags_erradas)}")

    # 7. Slug do nome de arquivo
    if "Title" in meta and meta["Title"]:
        esperado = slug_esperado(meta["Title"])
        atual = caminho.name
        if atual != esperado:
            avisos.append(f"Nome do arquivo '{atual}' difere do slug esperado '{esperado}'")

    # 8. Corpo vazio
    corpo = extrair_corpo(conteudo)
    if not corpo:
        avisos.append("Corpo do arquivo vazio (sem descrição do evento)")

    # 9. Links em branco
    for campo in CAMPOS_LINKS:
        if campo in meta:
            if not meta[campo]:
                links_vazios.append(campo)
        else:
            links_vazios.append(campo)  # campo nem existe

    return {"erros": erros, "avisos": avisos, "links_vazios": links_vazios}


# ─────────────────────────────────────────────
# Relatório
# ─────────────────────────────────────────────

def imprimir_relatorio(resultados: list):
    total      = len(resultados)
    ok         = [r for r in resultados if not r["erros"] and not r["avisos"]]
    com_avisos = [r for r in resultados if not r["erros"] and r["avisos"]]
    com_erros  = [r for r in resultados if r["erros"]]

    print()
    print(f"{NEGRITO}{'─'*60}{RESET}")
    print(f"{NEGRITO}  RELATÓRIO DE VALIDAÇÃO — {total} arquivo(s){RESET}")
    print(f"{'─'*60}{RESET}")

    # Erros críticos
    if com_erros:
        print(f"\n{VERMELHO}{NEGRITO}❌  {len(com_erros)} erro(s) crítico(s):{RESET}")
        for r in com_erros:
            print(f"\n  {VERMELHO}{NEGRITO}{r['arquivo']}{RESET}")
            for e in r["erros"]:
                print(f"    {VERMELHO}• {e}{RESET}")
            if r["avisos"]:
                for a in r["avisos"]:
                    print(f"    {AMARELO}⚠ {a}{RESET}")

    # Avisos
    if com_avisos:
        print(f"\n{AMARELO}{NEGRITO}⚠   {len(com_avisos)} arquivo(s) com avisos:{RESET}")
        for r in com_avisos:
            print(f"\n  {AMARELO}{r['arquivo']}{RESET}")
            for a in r["avisos"]:
                print(f"    {AMARELO}• {a}{RESET}")

    # Links vazios (resumo separado)
    arquivos_com_links_vazios = [r for r in resultados if r["links_vazios"]]
    if arquivos_com_links_vazios:
        print(f"\n{AMARELO}{NEGRITO}🔗  Links em branco:{RESET}")
        for r in arquivos_com_links_vazios:
            campos = ", ".join(r["links_vazios"])
            print(f"  {AMARELO}{r['arquivo']}{RESET} → {campos}")

    # OK
    if ok:
        print(f"\n{VERDE}{NEGRITO}✅  {len(ok)} arquivo(s) sem problemas{RESET}")
        for r in ok:
            sufixo = f"  {AMARELO}(links: {', '.join(r['links_vazios'])}){RESET}" if r["links_vazios"] else ""
            print(f"  {VERDE}{r['arquivo']}{RESET}{sufixo}")

    # Resumo final
    print(f"\n{'─'*60}")
    status = VERDE if not com_erros else VERMELHO
    print(f"{status}{NEGRITO}  Total: {total} | ✅ OK: {len(ok)} | ⚠ Avisos: {len(com_avisos)} | ❌ Erros: {len(com_erros)}{RESET}")
    print(f"{'─'*60}\n")

    if com_erros:
        print(f"{VERMELHO}  Corrija os erros críticos antes de publicar.{RESET}\n")
    elif com_avisos or arquivos_com_links_vazios:
        print(f"{AMARELO}  Sem erros críticos — verifique os avisos antes de publicar.{RESET}\n")
    else:
        print(f"{VERDE}  Tudo certo! Pode publicar.{RESET}\n")


# ─────────────────────────────────────────────
# Main
# ─────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Valida arquivos .md de eventos para o Pelican.")
    parser.add_argument(
        "--pasta", "-p",
        default="content",
        help="Pasta com os arquivos .md (padrão: content/)"
    )
    args = parser.parse_args()

    pasta = Path(args.pasta)
    if not pasta.exists():
        print(f"{VERMELHO}Pasta não encontrada: {pasta}{RESET}")
        sys.exit(1)

    arquivos = sorted(pasta.glob("*.md"))
    if not arquivos:
        print(f"{AMARELO}Nenhum arquivo .md encontrado em '{pasta}'.{RESET}")
        sys.exit(0)

    print(f"\nValidando {len(arquivos)} arquivo(s) em '{pasta}'...")

    resultados = []
    for caminho in arquivos:
        resultado = validar_arquivo(caminho)
        resultado["arquivo"] = caminho.name
        resultados.append(resultado)

    imprimir_relatorio(resultados)

    # Código de saída: 1 se houver erros críticos (útil para CI/CD)
    if any(r["erros"] for r in resultados):
        sys.exit(1)


if __name__ == "__main__":
    main()