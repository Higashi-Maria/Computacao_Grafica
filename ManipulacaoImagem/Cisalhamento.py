from PIL import Image
import numpy as np

# 1. Carregar a imagem e transformar em array Numpy
caminho_entrada = r"C:\Users\Maria\Desktop\CG\tensor.jpeg"
imagem = Image.open(caminho_entrada)
arr = np.array(imagem)
# shape: (altura, largura, canais)

altura, largura = arr.shape[:2]  # altura e largura originais da imagem
print(f"Original: shape Numpy: {arr.shape} (altura, largura, canais)")

# 2. Definir o fator de cisalhamento horizontal. shx = 0.3 significa: cada linha e desloca
# 0.3 vezes a altura da imagem para a direita (ou esquerda se negativo)
# A linha do topo (y=0) fica parada; a de baixo (y=altura-1) e a mais deslocada.
shx = 0.3  # fator de cisalhamento horizontal

# 3. Calcular a nova largura para que a imagem cisalhada caiba na tela.
deslocamento_max = int(np.ceil(shx * (altura - 1)))  # deslocamento máximo em pixels
nova_largura = largura + deslocamento_max  # nova largura da imagem cisalhada

# 4. Cisalhamento em Numpy usando MAPEAMENTO INVERSO:
# Para cada pixel de SAIDA(x_out, y_out), calcula de qual pixel da ENTRADA ele veio,
# aplicando a inversa da transformação: x_in = x_out - shx * y_out.
# Isso evita "buracos" caso fizessemos o mapeamento direto.
y_out, x_out = np.indices((altura, nova_largura))  # malhas de coordenadas de saída
x_in = (x_out - shx * y_out).astype(int)  # vizinho mais próximo (nearest neighbor)

# 5. Máscara: pixels cuja coordenada de origem cai dentro da imagem original.
# Os que ficam fora viram fundo (preto por padrão, pois o canvas começa zerado).
valido = (x_in >= 0) & (x_in < largura)  # True se o pixel de saída tem origem válida

# 6. Montar a imagem de saída usando indexação avançada do Numpy (sem loops).
arr_cisalhado = np.zeros(shape=(altura, nova_largura, 3), dtype=arr.dtype) 
arr_cisalhado[valido] = arr[y_out[valido], x_in[valido]]


print(f"Cisalhado: shape Numpy: {arr_cisalhado.shape} (altura aumenta em {deslocamento_max} px)")

# 7. Voltar para PIL só para salvar em disco
caminho_saida = r"C:\Users\Maria\Desktop\CG\tensor_cisalhado.jpeg"
Image.fromarray(arr_cisalhado).save(caminho_saida)

print(f"Imagem cisalhada salva com sucesso!")