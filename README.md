# Computação Gráfica

Exercícios e experimentos desenvolvidos para a disciplina de Computação Gráfica.

## Conteúdo

- Arquivos Python na raiz: leitura, exibição, representação de cores, contraste e gravação de imagens e vídeos.
- `01-10/`: filtros, binarização, detecção de bordas, linhas e círculos, segmentação e detecção por cor.
- `ManipulacaoImagem/`: transformações geométricas, filtros, redução de ruído e transformada de Fourier.
- `DisseminacaoCultura.py`: simulação visual de disseminação cultural com Tkinter.
- `img/` e `videos/`: imagens e vídeos usados pelos exercícios, além de resultados de processamento.

## Requisitos

Os exemplos usam Python 3 e, conforme o arquivo, OpenCV, NumPy, Matplotlib e Pillow. No Windows, instale as dependências com:

```powershell
py -m pip install opencv-python numpy matplotlib pillow
```

O Tkinter usado pela simulação de disseminação cultural costuma estar incluído na instalação padrão do Python para Windows.

## Como executar

Execute cada exercício a partir da pasta que contém o arquivo. Por exemplo:

```powershell
py .\DisseminacaoCultura.py
py .\01-10\2.0-DetecBordas.py
```

Alguns exercícios abrem imagens ou vídeos locais; mantenha os arquivos de dados nas pastas do projeto para que os caminhos usados pelos scripts sejam encontrados.
