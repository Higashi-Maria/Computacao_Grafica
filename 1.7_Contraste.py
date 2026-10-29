import cv2
import matplotlib.pyplot as plt

# FUNÇÃO: calcular histograma de imagem P&B
def histograma_pb(img_gray):
    """
    Retorna o histograma da imagem em escala de cinza.
    O histograma conta quantos pixels existem em cada nível de intensidade (0-255)
    """

    return cv2.calcHist([img_gray],[0],None,[256],[0,256])

# FUNÇÃo: calcular histograma dos canais RGB
def histograma_rgb(img_rgb):
    """
    Retorna uma lista com o histograma de cada canal da imagem colorida (R, G, B)
    Cada histograma conta os pixels em cada nível de intensidade para aquele canal
    """
    return [cv2.calcHist([img_rgb],[i],None,[256],[0,256]) for i in range(3)]

# FUNÇÃO: aplicar o CLAHE em imagem P&B
def clahe_pb(img_bgr, clip_limit=2.0, title_size=(8, 8)):
    """
    Aplica CLAHE (contrast Limited Adaptive Histogram Equalization) em P&G
    Diferente da equilização global, o CLAHE divide a imagem em blocos (tiles)
    e equaliza cada um separadamente, evitando amplificar o ruído nas regiões 
    uniformes.

    clip_limit: limita o quanto o contraste pode ser amplificado em cada bloco
    clipe_size: tamanho da imagem em cada bloco de análise (largura, altura)
    """

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=title_size )
    return clahe.apply(img_bgr)

def clahe_colorido(img_bgr, clip_limit=2.0, title_size=(8, 8)):
    """
    Aplica CLAHE apenas no canal de luminância(L) do espaço de cor LAB.
    Isso melhora o contraste sem alterar as cores originais da imagem,
    pois os canais A (Verde-Vermelho) e B (Azul-Amarelo) permanecem intactos.

    Fluxo: BGR -> LAB -> CLAHE no L -> LAB -> BGR
    """

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=title_size)

    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l_corr = clahe.apply(l)
    lab_corr = cv2.merge((l_corr, a, b))

    return cv2.cvtColor(lab_corr, cv2.COLOR_LAB2BGR)

# FUNÇÃO: Plotar comparação P&B (Antes e depois com histograma)
def plotar_comparacao_pb(imag_orig,img_corr):
    """
    Abre uma janela com quatro sun=bplots:
    Imagem P&B original | histograma principal
    Imagem P&B corrigida | histograma corrigida
    """

    hist_orig = histograma_pb(imag_orig)
    hist_corr = histograma_pb(img_corr)

    plt.figure(figsize=(12, 10))

    ax1 = plt.subplot(2, 2, 1)
    ax1.imshow(imag_orig, cmap='gray')
    ax1.set_title('Original P&B')
    ax1.axis('off')

    ax2 = plt.subplot(2, 2, 2)
    ax2.plot(hist_orig, color='black')
    ax2.fill_between(range(256), hist_orig.flatten(), alpha=0.3, color='gray')
    ax2.set_title('Histograma Original P&B')
    ax2.set_xlabel('Intensidade')
    ax2.set_ylabel('Pixels')

    ax3 = plt.subplot(2, 2, 3)
    ax3.imshow(img_corr, cmap='gray')
    ax3.set_title('P&B com CLAHE')
    ax3.axis('off')

    ax4 = plt.subplot(2, 2, 4)
    ax4.plot(hist_corr, color='black')
    ax4.fill_between(range(256), hist_corr.flatten(), alpha=0.3, color='gray')
    ax4.set_title('Histograma P&B com CLAHE')
    ax4.set_xlabel('Intensidade')
    ax4.set_ylabel('Pixels')

    plt.tight_layout()
    plt.show()

# FUNÇÃO: plotar comparação colorida (antes e depois com histograma)
def plotar_comparacao_colorida(img_orig_bgr, img_corr_bgr):
    """
    Abre uma janela com quatro subplots:
    Imagem colorida original | histograma RGB original
    Imagem colorida corrigida | histograma RGB corrigida
    Converte BGR -> RGB internamente para exibição correta na matplotlib
    """

    if len(img_orig_bgr.shape) == 2:
        rgb_orig = cv2.cvtColor(img_orig_bgr, cv2.COLOR_GRAY2RGB)
    else:
        rgb_orig = cv2.cvtColor(img_orig_bgr, cv2.COLOR_BGR2RGB)

    if len(img_corr_bgr.shape) == 2:
        rgb_corr = cv2.cvtColor(img_corr_bgr, cv2.COLOR_GRAY2RGB)
    else:
        rgb_corr = cv2.cvtColor(img_corr_bgr, cv2.COLOR_BGR2RGB)

    hist_orig = histograma_rgb(rgb_orig)
    hist_corr = histograma_rgb(rgb_corr)

    cores = ("r", "g", "b")
    rotulos = ("Vermelho", "Verde", "Azul")

    plt.figure(figsize=(12, 10))

    ax1 = plt.subplot(2, 2, 1)
    ax1.imshow(rgb_orig)
    ax1.set_title('Original colorida')
    ax1.axis('off')

    ax2 = plt.subplot(2, 2, 2)
    for hist, cor, rot in zip(hist_orig, cores, rotulos):
        ax2.plot(hist, color=cor, label=rot)
    ax2.set_title('Histograma original colorida')
    ax2.set_xlabel('Intensidade')
    ax2.set_ylabel('Pixels')
    ax2.legend(loc='upper left', fontsize='small')

    ax3 = plt.subplot(2, 2, 3) 
    ax3.imshow(rgb_corr)
    ax3.set_title('Colorida com CLAHE (Via LAB)')
    ax3.axis('off')

    ax4 = plt.subplot(2, 2, 4)
    for hist, cor, rot in zip(hist_corr, cores, rotulos):
        ax4.plot(hist, color=cor, label=rot)
    ax4.set_title('Histograma com CLAHE colorida')
    ax4.set_xlabel('Intensidade')
    ax4.set_ylabel('Pixels')
    ax4.legend(loc='upper left', fontsize='small')

    plt.tight_layout()
    plt.show()

# EXECUÇÃO

image = cv2.imread("img/alvan-nee.png")
if image is None:
    raise FileNotFoundError("Imagem não encontrada em img/alvan-nee.png")

# JANELA 1 - P&B: converte para cinza, aplica CLAHE e compara
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray_corr = clahe_pb(gray)
plotar_comparacao_pb(gray, gray_corr)

# JANELA 2 - Colorida: aplica CLAHE no canal L (LAB) e compara
color_corr = clahe_colorido(image)
plotar_comparacao_colorida(image, color_corr)