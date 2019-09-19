import pytesseract as ocr
import numpy as np
import cv2
from PIL import Image


# tipando a leitura para os canais de ordem RGB
imagem = Image.open('./imagem/recortes/recortes_nivel_dois/recortes_nivel_tres/bacon2.jpg').convert('RGB')

# transformando pillow image para cv2 image
cimg = np.array(imagem)
cimg = cimg[:, :, ::-1].copy() 

# # Visualização da imagem
# cv2.imshow('image',cimg)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# convertendo em um array editável de numpy[x, y, CANALS]
npimagem = np.asarray(imagem).astype(np.uint8)  

# # Visualização da imagem
# cv2.imshow('image',npimagem)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# diminuição dos ruidos antes da binarização
npimagem[:, :, 0] = 0 # zerando o canal R (RED)
npimagem[:, :, 2] = 0 # zerando o canal B (BLUE)

# # Visualização da imagem
# cv2.imshow('image',npimagem)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# atribuição em escala de cinza
im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY) 

# # Visualização da imagem
# cv2.imshow('image',im)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# aplicação da truncagem binária para a intensidade
# pixels de intensidade de cor abaixo de 127 serão convertidos para 0 (PRETO)
# pixels de intensidade de cor acima de 127 serão convertidos para 255 (BRANCO)
# A atrubição do THRESH_OTSU incrementa uma análise inteligente dos nivels de truncagem
ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU) 

# Visualização da imagem
cv2.imshow('image',thresh)
cv2.waitKey(0)
cv2.destroyAllWindows()

# reconvertendo o retorno do threshold em um objeto do tipo PIL.Image
binimagem = Image.fromarray(thresh) 

# chamada ao tesseract OCR por meio de seu wrapper
phrase = ocr.image_to_string(binimagem, lang='por')

# impressão do resultado
print(phrase) 