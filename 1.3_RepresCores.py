import cv2
import matplotlib.pyplot as plt

# — FUNÇÃO: separar canais RGB —
def separar_canais_rgb(img_bgr):
    """
    Separa os 3 canais de uma imagem BGR.
    Retorna (vermelho, verde, azul) como arrays 2D (escala de cinza).
    Nota: no OpenCV a ordem é BGR, então [:,:,0]=Azul, [:,:,2]=Vermelho.
    """
    # img[:, :, 0] = primeiro canal = Azul   (Blue)
    # img[:, :, 1] = segundo canal  = Verde  (Green)
    # img[:, :, 2] = terceiro canal = Vermelho (Red)
    azul     = img_bgr[:, :, 0]
    verde    = img_bgr[:, :, 1]
    vermelho = img_bgr[:, :, 2]
    return vermelho, verde, azul

# — FUNÇÃO: visualizar canais —
def visualizar_canais(img_bgr):
    """Plota a imagem original e seus 3 canais R, G, B lado a lado."""
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    r, g, b = separar_canais_rgb(img_bgr)

    fig, axes = plt.subplots(1, 4, figsize=(16, 4))
    axes[0].imshow(img_rgb);         axes[0].set_title("Original (RGB)")
    axes[1].imshow(r, cmap="gray");  axes[1].set_title("Canal R (Vermelho)")
    axes[2].imshow(g, cmap="gray");  axes[2].set_title("Canal G (Verde)")
    axes[3].imshow(b, cmap="gray");  axes[3].set_title("Canal B (Azul)")
    for ax in axes: ax.axis("off")
    plt.tight_layout(); plt.show()

# Entendendo vetores
imageColor = cv2.imread("img/bernie-almanzar.png", cv2.IMREAD_COLOR)
imageBlack = cv2.imread("img/bernie-almanzar.png", cv2.IMREAD_GRAYSCALE)

print("-> Conteúdo numérico da imagem imageBlack.png (escala de cinza)")
print("Forma do vetor:", imageBlack.shape)
print("Primeiros 3x3 pixels:\n", imageBlack[:3, :3])

print("\n -- \n")

print("-> Conteúdo numérico da imagem imageColor.png (colorida)")
print("Forma do vetor:", imageColor.shape)
print("Primeiros 3x3 pixels (BGR):\n", imageColor[:3, :3, :])

# Exibição de canais
imageColor = cv2.imread("img/bernie-almanzar.png")
visualizar_canais(imageColor)
imageColor = cv2.imread("img/cereja.png")
visualizar_canais(imageColor)
imageColor = cv2.imread("img/connor-ward.png")
visualizar_canais(imageColor)
imageColor = cv2.imread("img/laranja.png")
visualizar_canais(imageColor)
imageColor = cv2.imread("img/GuardaSol.png")
visualizar_canais(imageColor)

