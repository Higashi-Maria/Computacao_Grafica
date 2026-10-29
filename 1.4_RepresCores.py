import cv2
import matplotlib.pyplot as plt


# - FUNÇÃO: separar canais RGB
def separar_canais_rgb(img_brg):
    """
    Separar os 3 canais de uma RGB.
    Retorna (vermelho,verde, azul) como arrqay 30 (escala de cinza) e 1 (canal único).
    Nota: no OpenCV a ordem é BGR, então [:, :, 0] é azul, [:, :, 1] é verde e [:, :, 2] é vermelho.

    """
    # img[:, :, 0] =primeiro canal = azul(Blue)
    # img[:, :, 1] =segundo canal = verde(Green)
    # img[:, :, 2] =terceiro canal = vermelho(Red)

    azul = img_brg[:, :, 0]
    verde = img_brg[:, :, 1]
    vermelho = img_brg[:, :, 2]

    return vermelho, verde, azul

# FUNÇÃO: visualizar canais RGB
def visualizar_canais_rgb(img_brg):
    """
    Plota a imagem original e os 3 canais RGB lado a lado.
    """
    img_bgr = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)  # Converte BGR para RGB para exibição correta no Matplotlib
    r, g, b = separar_canais_rgb(img_bgr)

    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    axes[0].imshow(img_bgr);   axes[0].set_title("Original(RGB)")
    axes[1].imshow(r, cmap='gray');  axes[1].set_title("Canal Vermelho (R)")
    axes[2].imshow(g, cmap='gray');  axes[2].set_title("Canal Verde(G)")
    axes[3].imshow(b, cmap='gray');  axes[3].set_title("Canal Azul (B)")

    for ax in axes: ax.axis('off')  # Remove eixos para todas as subplots
    plt.tight_layout(); plt.show()  # Exibe o plot

# Entendendo os vetores
imageColor = cv2.imread("img/bernie-almanzar.png", cv2.IMREAD_COLOR)
imageBlack = cv2.imread("img/bernie-almanzar.png", cv2.IMREAD_GRAYSCALE)

print("-> Conteúdo numérico da imagem ImageGray.png (escala de cinza)")
print("Forma do vetor : ", imageBlack.shape) # Tamanho e formato da imagem
print("Primeiro 3x3 pixels (BGR)", imageColor[:3, :3, 0]) # Mostra os primeiros 3x3 pixels do canal azul

# Exibição de canais
ImageColor = cv2.imread("img/bernie-almanzar.png")
visualizar_canais_rgb(ImageColor)
ImageColor = cv2.imread("img/cereja.png")
visualizar_canais_rgb(ImageColor)
ImageColor = cv2.imread("img/connor-ward.png")
visualizar_canais_rgb(ImageColor)
ImageColor = cv2.imread("img/laranja.png")
visualizar_canais_rgb(ImageColor)
ImageColor = cv2.imread("img/GuardaSol.png")
visualizar_canais_rgb(ImageColor)