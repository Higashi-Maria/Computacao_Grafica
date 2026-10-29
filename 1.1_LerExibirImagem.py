import cv2
import matplotlib.pyplot as plt

# Exibição utilizando OpenCV
imagemColor = cv2.imread("img/bernie-almanzar.png")

cv2.imshow("Mostrando a imagem", imagemColor) # Abre a janela com o título dado "Mostrando a imagem"

cv2.waitKey(0) # Aguarda tecla ( 0 = espera infinita)
cv2.destroyAllWindows() # Fecha todas as janelas abertas pelo OpenCV

# Exibição utilizando Matplotlib
img_rgb = cv2.cvtColor(imagemColor, cv2.COLOR_BGR2RGB)

plt.imshow(img_rgb)                 # Exibir a imagem no plot
plt.title("Mostrando a imagem")     # Define o título
plt.axis("off")                     # Remove eixos (mais limpo para imagens)
plt.show()                          # 