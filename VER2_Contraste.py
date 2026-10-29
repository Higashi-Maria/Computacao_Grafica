import cv2
import matplotlib.pyplot as plt

# Calcular histograma de imagem em tons de cinza
def histograma_pb(img_gray):
    """
    Retorna o histograma dos 256 níveis de intensidade da imagem.
    """
    return cv2.calcHist([img_gray], [0], None, [256], [0, 256])

# Calcular histograma dos canais BGR (ordem usada pelo OpenCV)
def histograma_rgb(img_bgr):
    """
    Retorna os histogramas dos canais B, G e R, nessa ordem.
    """
    return [cv2.calcHist([img_bgr], [i], None, [256], [0, 256]) for i in range(3)]
    
# Aplicar CLAHE em imagem em tons de cinza
def clahe_pb(img_gray, clip_limit=2.0, tile_size=(8, 8)):
    """
    Aplica CLAHE (equalização adaptativa de histograma com limite de contraste).

    clip_limit: limita o quanto o contraste pode ser amplificado em cada bloco
    tile_size: quantidade de blocos na horizontal e na vertical
    """

    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
    return clahe.apply(img_gray)


def clahe_colorido(img_bgr, clip_limit=2.0, tile_size=(8,8)):
    
    clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=tile_size)
    lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    l_corr = clahe.apply(l)
    lab_corr = cv2.merge((l_corr, a, b))

    return cv2.cvtColor(lab_corr, cv2.COLOR_LAB2BGR)


def plotar_comparacao_pb(img_orig, img_corr):
    """
    Abre uma janela com quatro subplots:
    imagem P&B original | histograma original
    imagem P&B corrigida | histograma corrigido
    """

    hist_orig = histograma_pb(img_orig)
    hist_corr = histograma_pb(img_corr)


    plt.figure(figsize=(12,10))

    ax1 = plt.subplot(2,2,1)
    ax1.imshow(img_orig, cmap='gray')
    ax1.set_title('Original P&B')
    ax1.axis('off')

    ax2 = plt.subplot(2,2,2)
    ax2.plot(hist_orig, color='black')
    ax2.fill_between(range(256), hist_orig.flatten(), alpha=0.3, color='gray')
    ax2.set_title("Histograma original P&B")
    ax2.set_xlabel("Intensidade")
    ax2.set_ylabel("Pixels")

    ax3 = plt.subplot(2,2,3)
    ax3.imshow(img_corr, cmap='gray')
    ax3.set_title('P&B COM CLAHE')
    ax3.axis('off')

    ax4 = plt.subplot(2,2,4)
    ax4.plot(hist_corr, color='black')
    ax4.fill_between(range(256), hist_corr.flatten(), alpha=0.3, color='gray')
    ax4.set_title('Histograma P&B com CLAHE')
    ax4.set_xlabel("Intensidade")
    ax4.set_ylabel("Pixels")

    plt.tight_layout()
    plt.show()

def plotar_comparacao_colorida(img_orig_bgr, img_corr_bgr):
    rgb_orig = cv2.cvtColor(img_orig_bgr, cv2.COLOR_BGR2RGB)
    rgb_corr = cv2.cvtColor(img_corr_bgr, cv2.COLOR_BGR2RGB)

    hist_orig = histograma_rgb(img_orig_bgr)
    hist_corr = histograma_rgb(img_corr_bgr)

    cores = ("b", "g", "r")
    rotulos = ("Azul", "Verde", "Vermelho")

    plt.figure(figsize=(12,10))

    ax1 = plt.subplot(2,2,1)
    ax1.imshow(rgb_orig)
    ax1.set_title('Original colorida')
    ax1.axis('off')

    ax2 = plt.subplot(2,2,2)
    for hist, cor, rot in zip(hist_orig, cores, rotulos):
        ax2.plot(hist, color=cor, label=rot)
    ax2.set_title('Histograma original')
    ax2.set_xlabel('Intensidade')
    ax2.set_ylabel('Pixels')
    ax2.legend(loc='upper left', fontsize='small')

    ax3 = plt.subplot(2,2,3)
    ax3.imshow(rgb_corr)
    ax3.set_title('Colorida com CLAHE (via Lab)')
    ax3.axis('off')
    
    ax4 = plt.subplot(2,2,4)
    for hist, cor, rot in zip(hist_corr, cores, rotulos):
        ax4.plot(hist, color=cor, label=rot)
    ax4.set_title('Histograma corrigida com CLAHE')
    ax4.set_xlabel('Intensidade')
    ax4.set_ylabel('Pixels')
    ax4.legend(loc='upper right', fontsize='small')

    plt.tight_layout()
    plt.show()


def main():
    caminho_imagem = "C:\Users\Maria\Desktop\CG\img/img/alvan-nee.png"
    image = cv2.imread(str(caminho_imagem))
    if image is None:
        raise FileNotFoundError(f"Não foi possível carregar a imagem: {caminho_imagem}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray_corr = clahe_pb(gray)
    plotar_comparacao_pb(gray, gray_corr)

    color_corr = clahe_colorido(image)
    plotar_comparacao_colorida(image, color_corr)

