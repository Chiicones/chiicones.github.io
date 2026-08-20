import os
import re
import shutil

def extrair_campo(texto, campo):
    padrao = rf"^\s*{campo}:\s*(.+)$"
    match = re.search(padrao, texto, re.MULTILINE | re.IGNORECASE)
    return match.group(1).strip() if match else ""

def nome_pasta_valido(nome):
    """Remove caracteres inválidos para nomes de pasta no Windows."""
    return re.sub(r'[\\/:*?"<>|]', "", nome).strip()

def organizar_por_local(pasta="."):
    arquivos_md = [f for f in os.listdir(pasta) if f.endswith(".md")]

    if not arquivos_md:
        print("Nenhum arquivo .md encontrado na pasta.")
        return

    movidos = 0
    sem_local = []

    for arquivo in arquivos_md:
        caminho = os.path.join(pasta, arquivo)
        with open(caminho, encoding="utf-8-sig") as f:
            conteudo = f.read()

        local = extrair_campo(conteudo, "Local")

        if not local:
            sem_local.append(arquivo)
            continue

        subpasta = nome_pasta_valido(local)
        destino_dir = os.path.join(pasta, subpasta)
        os.makedirs(destino_dir, exist_ok=True)

        destino = os.path.join(destino_dir, arquivo)
        shutil.move(caminho, destino)
        print(f"  {arquivo} → {subpasta}/")
        movidos += 1

    print(f"\n{movidos} arquivo(s) movido(s).")

    if sem_local:
        print(f"{len(sem_local)} arquivo(s) sem campo 'Local:' (mantidos na pasta original):")
        for f in sem_local:
            print(f"  - {f}")

if __name__ == "__main__":
    pasta_script = os.path.dirname(os.path.abspath(__file__))
    organizar_por_local(pasta_script)