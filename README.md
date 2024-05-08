## Objetivo

A detecção de movimento e a exploração da técnica de 'ponto a ponto' com o filtro de limiarização foram o principal objetivo deste projeto. Em prática, o movimento na imagem é reconhecido a partir dos píxeis que assumem um novo valor em relação aos frames anteriores e, para visualizarmos essa diferença, é criado um novo modelo com a limiarização desse resultado.

#### Parte 1 - Importando os dados

Importei as bibliotecas a seguir com o intuito de trabalhar com uma interface gráfica (tkinter), processamento de imagens (OpenCV) e facilitar o gerenciamento de arranjos e matrizes (NumPy).

```python
from tkinter import *
import cv2
import numpy as n
```
#### Parte 2 - Implementação algoritmos 

##### Algoritmos capturar movimento

Função – limiar consiste em separar píxeis de uma imagem em duas categorias distintas, neste caso preto e branco, a partir de um valor limiar.

A limiarização é útil para casos onde precisamos isolar um objeto de interesse na imagem.

```python
#FUNÇÃO LIMIAR
def limiar(img):   
  img_res = np.zeros(img.shape)
  limiar = 30
  
  for x in range(img.shape[0]):
    for y in range(img.shape[1]):
      if img[x,y] > limiar:
        img_res[x,y] = 255
      else:
        img_res[x,y] = 0
        
  return img_res
```

Este trecho é responsável pela captura de três imagens renderizadas pela webcam, após a captação é efetuada a subtração entre elas, com o intuito de identificar e capturar a diferença entre elas, a partir disso formar uma única imagem.
Utilizamos o método absdiff da biblioteca OpenCv para identificar as diferenças, e o método bitwise_and da biblioteca OpenCv para mesclar as imagens.

```python
# CALCULO DE DIFERENÇA ENTRE FRAMES
diferenca1 = cv2.absdiff(terceiroFrame, segundoFrame)
diferenca2 = cv2.absdiff(segundoFrame, primeiroFrame)
diferencaFinal = cv2.bitwise_and(diferenca1,diferenca2)
```

Após identificar e montar a imagem referencial, mandaremos a mesma como parâmetro da função Limiar para conseguirmos apresentar o resultado.
Resolvemos utilizar uma ferramenta de contorno para destacar os pontos que a função de limiarização nos trouxe, para este caso efetuamos a conversão do retorno da limiarização para um array de 8 bits e com isso passamos como parâmetro para o método findContours que faz a busca por alterações para ser utilizado no método drawContours que irá apresentar graficamente.
Por final, apresentemos com o método OpenCV imshow, que irá retornar uma janela com o resultado.

```python
diferencaFinal = limiar(diferencaFinal)
imgDeContorno = diferencaFinal.astype(np.uint8)
achandoContorno,aux = cv2.findContours(image = imgDeContorno, mode = cv2.RETR_TREE, method =cv2.CHAIN_APPROX_SIMPLE)
cv2.drawContours(image = frame, contours = achandoContorno, contourIdx = -1, color = (255,150,0), thickness = 3, lineType = cv2.LINE_AA)

cv2.imshow(janelaComFiltro, diferencaFinal)
cv2.imshow(janelaSemFiltro, frame)
```
### Resultado
![img limiar 2](https://github.com/inhouuu/Limiarizacao/assets/45317498/8807f550-2e66-4b37-b602-f9f371e0815f)
![img limiar 1](https://github.com/inhouuu/Limiarizacao/assets/45317498/e3231082-f5dd-4ec4-a83a-2285068c21b2)

## Conclusão

Por fim, o resultado do projeto resultou com o objetivo inicial, nele foi possível compreender melhor o funcionamento dos filtros em imagens que estão sendo geradas de forma simultânea com o processamento das mesmas.
O conteúdo, em especial a técnica de point processing, foi necessária para diferenciar as partes em movimento das partes estáticas, tais quais o plano de fundo.
