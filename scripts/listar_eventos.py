import os
import re

def extrair_campo(texto, campo):
    """Extrai o valor de um campo no formato 'Campo: Valor'."""
    padrao = rf"^\s*{campo}:\s*(.+)$"
    match = re.search(padrao, texto, re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else "(não encontrado)"

def gerar_lista_eventos(pasta="."):
    arquivos_md = [f for f in os.listdir(pasta) if f.endswith(".md")]

    if not arquivos_md:
        print("Nenhum arquivo .md encontrado na pasta.")
        return

    eventos = []

    for arquivo in sorted(arquivos_md):
        caminho = os.path.join(pasta, arquivo)
        with open(caminho, encoding="utf-8-sig") as f:
            conteudo = f.read()

        titulo = extrair_campo(conteudo, "Title")
        local = extrair_campo(conteudo, "Local")
        eventos.append((titulo, local))

    caminho_saida = os.path.join(pasta, "eventos.txt")
    with open(caminho_saida, "w", encoding="utf-8") as f:
        f.write("LISTA DE EVENTOS\n")
        f.write("=" * 40 + "\n\n")
        for titulo, local in eventos:
            f.write(f"Evento: {titulo}\n")
            f.write(f"Local:  {local}\n")
            f.write("-" * 40 + "\n")

    print(f"{len(eventos)} evento(s) encontrado(s). Resultado salvo em: {caminho_saida}")

if __name__ == "__main__":
    # Roda na mesma pasta onde o script está
    pasta_script = os.path.dirname(os.path.abspath(__file__))
    gerar_lista_eventos(pasta_script)