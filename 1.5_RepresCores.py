import cv2
import matplotlib.pyplot as plt

# - FUNÇÃO: converter para HSV e visualizar os canais

def visualizar_hsv(img_bgr):
    """
    Converter a imagem para HSV e plota os 3 canais separadamente, além da imagem original.
    Útil para entender como cada canal se comporta em diferentes cenas
    """

    # Converter BGR (formato do OpenCV) para HSV
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

    # cv2.split divide o array 30m em 3 arrays 20
    h, s, v = cv2.split(img_hsv)

    fig, axes = plt.subplots(1, 4, figsize=(16,4))
    axes[0].imshow(img_rgb); axes[0].set_title("Original (RGB)")
    axes[1].imshow(h, cmap='hsv'); axes[1].set_title("M - Matriz (cor)")
    axes[2].imshow(s, cmap='gray'); axes[2].set_title("S - Saturação (pureza)")
    axes[3].imshow(v, cmap='gray'); axes[3].set_title("V - Valor (brilho)")
    for ax in axes:
        ax.axis('off')
    plt.tight_layout()
    plt.show()

imageColor = cv2.imread("img/laranja.png")

fig, axes = plt.subplots(1, 2, figsize=(12, 6))
axes[0].imshow(imageColor)
axes[0].set_title("Original (BGR)")
img_rgb = cv2.cvtColor(imageColor, cv2.COLOR_BGR2RGB)
axes[1].imshow(img_rgb)
axes[1].set_title("Original (RGB)")
plt.tight_layout()
plt.show()

visualizar_hsv(imageColor)
imageColor = cv2.imread("img/laranja.png")
visualizar_hsv(imageColor)
imageColor = cv2.imread("img/cereja.png")
visualizar_hsv(imageColor)
imageColor = cv2.imread("img/GuardaSol.png")