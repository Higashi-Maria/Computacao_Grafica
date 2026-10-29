from PIL import Image
import numpy as np

# 1. Carregar a imagem e transformar em array Numpy
caminho_entrada = (r"C:\Users\Maria\Desktop\CG\tensor.jpeg")
imagem = Image.open(caminho_entrada)
arr = np.array(imagem)
# shape: (altura, largura, canais)

print(f"Original: shape Numpy: {arr.shape} (altura, largura, canais)")

# 2. Rotacionar 90 graus no sentido horário usando Numpy.np.rot90(arr, k) gira k*90 graus 
# no sentido anti-horário, então para girar 90 graus no sentido horário, usamos k=-1
#Rotação de 90 graus é só permutação de eixos + espelhamento (não precisa interpolar)
arr_rotacionado = np.rot90(arr, k=-7)  # shape: (largura, altura, canais)

print(f"Rotacionado: shape Numpy: {arr_rotacionado.shape} (altura, largura, canais)")

# 3. Voltar para PIL só para salvar em disco
caminho_saida = r"C:\Users\Maria\Desktop\CG\tensor_rotacionado_k=-7.jpeg"
Image.fromarray(arr_rotacionado).save(caminho_saida)

print(f"Imagem rotacionada salva com sucesso!")