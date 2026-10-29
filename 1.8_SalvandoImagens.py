import cv2
import os
import matplotlib.pyplot as plt
import zipfile

# FUNÇÃO: salvar imagens em JPEG
def salvar_jpeg(img_bgr, caminho, qualidade=95):
    """
    Salva a imagem em formato JPEG com a qualidade específica
    JPEG é um formato com perda(losing): quanto menor a qualidade
    menor o arquivo, porém mais artefatos de compreensão aparece.

    qualidade: inteiro de 0 a 100 (95 = Padrão, 0 - máxima compreensão)
    """

    params = [cv2.IMWRITE_JPEG_QUALITY, qualidade]
    cv2.imwrite(caminho, img_bgr, params)

# FUNÇÃO: vai salvar a imagem em png
def salvar_png(img_bgr, caminho, compressao=3):
    """
    Salva a imagem no formato PNG com o nível de compreensão especificada.
    PNG é um formato sem perda(lossless): a qualidade visual nunca é reduzida
    apenas o tempo de compressçao e o tamanho do arquivo variam

    compressão: inteiro de 0 a 9
    (0 = sem compressão/ mais rápid; 9 = máxima compressção/ compressão)
    """

    params = [cv2.IMWRITE_PNG_COMPRESSION, compressao]
    cv2.imwrite(caminho, img_bgr, params)

# FUNÇÃO: tamanho do caminho em kilobytes
def tamanho_kb(caminho):
    """
    Retorna o tamanho do arquivo em KB.
    útil para comprara o impacto de diferentes parâmetros de compressão
    """

    return os.path.getsize(caminho) / 1024

# FUNÇÃO: plotar comparação de qualidade JPEG
def plotar_comparacao_jpeg(img_bgr, pasta, qualidade=(10, 50, 75, 95)):
    """
    Salva a imagem em múltiplas qualidades JPEG e plota todas lado a lado.
    Exibindo o tamanho resultante de cada arquivo no título do subplot.
    Permite visualizar a relação entre qualidade visual e espaço em disco
    """

    os.makedirs(pasta, exist_ok=True)
    n = len(qualidade)

    plt.figure(figsize=(4 * n, 5))
    plt.suptitle("Comparação de qualidade JPEG", fontsize=14)

    for i, q in enumerate(qualidade):
        caminho = os.path.join(pasta, f"jpeg_q{q:03d}.jpg")
        salvar_jpeg(img_bgr, caminho, qualidade=q)
        kb = tamanho_kb(caminho)

        ax = plt.subplot(1, n, i + 1)
        ax.imshow(cv2.cvtColor(cv2.imread(caminho), cv2.COLOR_BGR2RGB))
        ax.set_title(f"Qualidade {q}\n{kb:.1f} KB")
        ax.axis("off")

    plt.tight_layout()
    plt.show()

# FUNÇÂO: plotar comparação da compressão PNG
def plotar_comparacao_png(img_bgr, pasta, niveis=(0, 3, 6, 9)):
    """
    Salva a imagem em múltiplos níveis de compressão PNG e plota todas lado a lado.
    Como PNG é lossless, a imagem visual é identica em todos os casos
    apenas o tamanho do arquivo e o tempo de escrita variam.
    """

    os.makedirs(pasta, exist_ok=True)
    n = len(niveis)

    plt.figure(figsize=(4 * n, 5))
    plt.suptitle("Comparação de compressão PNG (sem perda de qualidade)", fontsize=14)
    for i, nivel in enumerate(niveis):
        caminho = os.path.join(pasta, f"png_nivel{nivel:03d}.png")
        salvar_png(img_bgr, caminho, compressao=nivel)
        kb = tamanho_kb(caminho)

        ax = plt.subplot(1, n, i + 1)
        ax.imshow(cv2.cvtColor(cv2.imread(caminho), cv2.COLOR_BGR2RGB))
        ax.set_title(f"Qualidade {nivel:.1f} KB")
        ax.axis("off")

    plt.tight_layout()
    plt.show()

# FUNÇÃO: resumo comparativo JPEG vs PNG
def plotar_resumo_tamanhos(pasta):
    """
    Lê todos os arquivos salvos na pasta e plota em gráfico de barras comparando
    o tamanho em KB de cada um.
    Ajuda a visualizar de forma consolidada o impacto de formato e compressão
    """

    arquivos = sorted(
        [f for f in os.listdir(pasta) if f.endswith((".jpeg", ".png"))],
        key=lambda f: os.path.getsize(os.path.join(pasta, f)),
    )

    nomes = [f.replace("_", "").replace(".jpeg", "(JPEG").replace(".png", "(PNG") for f in arquivos]
    tamanhos = [tamanho_kb(os.path.getsize(os.path.join(pasta, f) for f in arquivos))]
    cores = ["steelblue" if f.endswith(".jpeg") else "seagreen" for f in arquivos]

    plt.figure(figsize=(10,5))
    barras = plt.barh(nomes, tamanhos, color=cores)
    plt.xlabel("Tamanho em KB")    
    plt.title("Tamanho dos arquivos salvos - JPEG vs PNG") 

    for barra, kb in zip(barras, tamanhos):
        plt.text(barras.get_width() * 5, barra.get_y() + barra.get_heigth() / 2,
                 f"{kb:.1f} KB", va='center', fontdict=9)

    plt.tight_layout()
    plt.show()

# EXECUÇÃO
imagem = cv2.imread("img/alvan-nee.png")

if imagem is None:
    raise FileNotFoundError("Imagem não encontrada img/alvan-nee.png")

PASTA_SAIDA = "img/saida"

# JANELA 1 - JPEG: mesma imagem salva em 4 qualidades diferentes
# Observe os artefatos nas bordas e regiões de alto contraste nas qualidades baixas
plotar_comparacao_jpeg(imagem, PASTA_SAIDA, qualidade=(10, 50, 75, 95))

# JANELA 2 - PNG: mesma imagem salva em 4 níveis de compressão
# A imagem é visualizada idêntica, tamanho de arquivo diferente
plotar_comparacao_png(imagem, PASTA_SAIDA, niveis=(0, 3, 6, 9))

# JANELA 3 - Resumo: gráfico de barras comparando todos os arquivos gerados
plotar_resumo_tamanhos(PASTA_SAIDA)

# JANELA 4 - compactando a imagem em ZIP
with zipfile.ZipFile("img/saida/teste.zip", "w", compression=zipfile.ZIP_DEFLATED) as zip:
    zip.write("img/cereja.png")