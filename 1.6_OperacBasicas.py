import cv2
import matplotlib.pyplot as plt

# - FUNÇÃO: Ajustar brilho e contraste
def ajustar_brilho_contraste(img_bgr, alpha=1.0, beta=0):
    """
    Ajusta o brilho e contraste da imagem.
    alpha: Contraste (1.0 = sem alteração, >1 aumenta contraste, <1 diminui contraste)
    beta: Brilho (0 = sem alteração, >0 aumenta brilho, <0 diminui brilho)
    """
    # Aplicar a transformação linear: nova_imagem = alpha * img_bgr + beta
    
    return cv2.convertScaleAbs(img_bgr, alpha=alpha, beta=beta)

# -FUNÇÃO: Redimensionar imagem
def redimensionar(img, largura=None, altura=None, escala=None):
    """
    Redimensiona a imagem de forma flexível.
    - Se escala fornecida: aplicar porcentagem (0.5 = 50% do tamanho)
    - Se largura ou altura fornecida: usa o tamanho absoluto
    - Se apenas largura ou altura fornecida: mantém a proporção automaticamente
    """
    h_orig, w_orig = img.shape[:2] # shape = (altura, largura, canais)

    if escala is not None:
        nova_larg = int(w_orig * escala)
        nova_altura = int(h_orig * escala)
    elif largura is not None:
            nova_larg, nova_altura = largura, altura
    elif largura:
         nova_larg = largura
         nova_altura = int(h_orig * largura/w_orig)
    elif altura:
         nova_altura = altura
         nova_larg = int(w_orig * altura/h_orig)
    else:
         return img  # Retorna a imagem original se nenhum parâmetro for fornecido
         
    # INTER_AREA é ideal para reduzir. INTER_LINEAR é ideal para ampliar
    # imagem de 4 pixels e ir para 2, posso ter de 2 e ir para 1.5
    interpol = cv2.INTER_AREA if nova_larg < w_orig else cv2.INTER_LINEAR
    return cv2.resize(img, (nova_larg, nova_altura), interpolation=interpol)

# - FUNÇÃO: cortar região de interesse
def cortar(img, x, y, largura, altura):
    """
    Recorta uma região retangular da imagem.
    x, y: coordenadas do canto superior esquerdo do retângulo (coluna, linha)
    Nota: o acesso ao array Numpy é [linha:linha, coluna:coluna]
    (y antes de x)
    """
    return img[y:y+altura, x:x+largura]

# - FUNÇÃO: Rotacionar imagem
def rotacionar(img, angulo, escala=1.0):
    """
    Rotaciona a imagem em torno do seu centro.
    angulo: ângulo em graus (positivo = sentido anti-horário)
    """
    h, w = img.shape[:2]
    centro = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(centro, angulo, 1.0)
    return cv2.warpAffine(img, M, (w, h))

image = cv2.imread("img/laranja.png")

# Usa cada função definida acima e vamos plotar os resultados em subplots
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
img_brilho = ajustar_brilho_contraste(image, alpha=0.5, beta=0)
# Aumenta a imagem, OBS: TESTEM com 0.5 e 0
img_redium = redimensionar(image, escala=0.5)
img_corte = cortar(image, 2100, 1200, 2500, 1600) # x=100, y=100, largura =800, altura=600
# Vamos testar com 2100, 1200, 2500, 1600)
img_rot = rotacionar(image, angulo=3.0)

plt.figure(figsize=(16, 10))

ax1 = plt.subplot(2, 3, 1)
ax1.imshow(image_rgb)
ax1.set_title("Original {image_rgb.shape}")
ax1.axis('off')

ax2 = plt.subplot(2, 3, 2)
ax2.imshow(cv2.cvtColor(img_brilho, cv2.COLOR_BGR2RGB))
ax2.set_title("Brilho/Contraste")
ax2.axis('off')

ax3 = plt.subplot(2, 3, 3)
ax3.imshow(cv2.cvtColor(img_redium, cv2.COLOR_BGR2RGB))
ax3.set_title("Redimensionar")
ax3.axis('off')

ax4 = plt.subplot(2, 3, 4)
ax4.imshow(cv2.cvtColor(img_corte, cv2.COLOR_BGR2RGB))
ax4.set_title("Cortar")
ax4.axis('off')

ax5 = plt.subplot(2, 3, 5)
ax5.imshow(cv2.cvtColor(img_rot, cv2.COLOR_BGR2RGB))
ax5.set_title("Rotacionar")
ax5.axis('off')

plt.tight_layout()
plt.show()