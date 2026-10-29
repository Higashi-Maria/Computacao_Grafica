from PIL import Image
import numpy as np

img = Image.open(r"C:\Users\Maria\Desktop\CG\tensor.jpeg") # Converte para RGB, descartando o canal alfa se houver
#img = Image.open(r"C:\Users\Maria\Desktop\Nova pasta (4)\tensor.png")
#arr = np.array(img)[:, :, :3]  # mantém só R, G, B; descarta o canal alfa no Numpy
arr = np.array(img)

print(arr.shape)  # ex.: (height, width, channels) se for RGB