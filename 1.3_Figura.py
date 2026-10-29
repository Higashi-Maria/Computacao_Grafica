import cv2
import matplotlib.pyplot as plt

imageColor = cv2.imread("img/bernie-almanzar.png")
img_rgb = cv2.cvtColor(imageColor, cv2.COLOR_BGR2RGB)

linhas = 2
colunas = 3

# Criar a figura com a grade do subplots
fig, axes = plt.subplots(linhas, colunas, figsize=(15, 10))
# 5, 5 -> X, Y

# [linhas, colunas]
axes [0, 0].imshow(img_rgb)
axes [0, 0].set_title('Fig 1 - LOC-0')

axes [0, 1].imshow(img_rgb)
axes [0, 1].set_title('Fig 2 - LOC-1')
axes [0, 1].axis('off')

imageColor = cv2.imread("img/connor-ward.png")
img_rgb = cv2.cvtColor(imageColor, cv2.COLOR_BGR2RGB)

# [linhas, colunas]
axes [1, 1].imshow(img_rgb)
axes [1, 1].set_title('Fig 3 - L1C1')

axes [1, 2].imshow(img_rgb)
axes [1, 2].set_title('Fig 4 - L1C2')
axes [1, 2].axis('off')

plt.figure(figsize=(10, 5))
#plt.figure()

# 2 linhs, 1 coluna
ax1 = plt.subplot(2, 1, 1)
ax1.imshow(img_rgb)
ax1.set_title(f'Original - {img_rgb.shape}')
ax1.axis('off')

ax1 = plt.subplot(2, 1, 2)
ax1.imshow(img_rgb)
ax1.set_title(f'Original - {img_rgb.shape}')


plt.tight_layout()
plt.show()