import socket
import sys
import threading
import base64
import pytesseract as ocr
import numpy as np
import cv2
import struct
from PIL import Image

hostname = "redesb.space"
HOST = socket.gethostbyname(hostName)	# Symbolic name meaning all available interfaces
PORT = 9666	# Arbitrary non-privileged port
HOST = socket.gethostbyname(HOST)
print(str(HOST))
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')

#Bind socket to local host and port
try:
	s.bind((HOST, PORT))
except socket.error as msg:
	print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	sys.exit()

print ('Socket bind complete')

# Start listening on socket
s.listen(10)
print ('Socket now listening')


# Receives base64 string and decode to jpg
def decodeImage(baseImage):
	imgData = base64.b64decode(baseImage)
	fileName = 'test_image.jpg'
	with open(fileName, 'wb') as f:
		f.write(imgData)


# Deep Learning to read the image (may be a call to other code file)
def readImage():
	# tipando a leitura para os canais de ordem RGB
	imagem = Image.open('test_image.jpg').convert('RGB')

	# transformando pillow image para cv2 image
	cimg = np.array(imagem)
	cimg = cimg[:, :, ::-1].copy()

	# # Visualizacaoo da imagem
	# cv2.imshow('image',cimg)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

	# convertendo em um array editavel de numpy[x, y, CANALS]
	npimagem = np.asarray(imagem).astype(np.uint8)

	# # Visualizacaoo da imagem
	# cv2.imshow('image',npimagem)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

	# diminuio dos ruidos antes da binarizao
	npimagem[:, :, 0] = 0 # zerando o canal R (RED)
	npimagem[:, :, 2] = 0 # zerando o canal B (BLUE)

	# # Visualizao da imagem
	# cv2.imshow('image',npimagem)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

	# atribuio em escala de cinza
	im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY)

	# # Visualizaaao da imagem
	# cv2.imshow('image',im)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()

	# apla da truncagem binaria para a intensidade
	# pixels de intensidade de cor abaixo de 127 aonvertidos para 0 (PRETO)
	# pixels de intensidade de cor acima de 127 saonvertidos para 255 (BRANCO)
	# A atrubiao do THRESH_OTSU incrementa uma anateligente dos nivels de truncagem
	ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

	# Visualizaao da imagem
	#cv2.imshow('image',thresh)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()

	# reconvertendo o retorno do threshold em um objeto do tipo PIL.Image
	binimagem = Image.fromarray(thresh)

	# chamada ao tesseract OCR por meio de seu wrapper
	phrase = ocr.image_to_string(binimagem, lang='por')

	# imprao do resultado
	return phrase

# Now keep talking with the client
while 1:
    # Wait to accept a connection - blocking call
	conn, addr = s.accept()
	print ('Connected with ' + addr[0] + ':' + str(addr[1]))
	final = ""
	size = ""
	data = conn.recv(1024)
	size += data.decode('utf-8')
	data = conn.recv(1024)
	size += data.decode('utf-8')
	size = int(size)
	print(size)
	# Infinite loop so that function do not terminate
	while True:
		#print("Looking for more")
		dataImg = conn.recv(1024)
		#print(data)
		final += dataImg.decode('utf-8')
		print(dataImg.decode('utf-8'))
		size -= 1024
		if size <= 0 :
			print("Breaking")
			break

	print("Received all")
	#print (final)
	#print(size)
	decodeImage(final)
	reply = readImage()
	print (reply)
	#conn.sendall(str(len(reply.encode())).encode())
	conn.sendall(reply.encode())

	# End of Loop

conn.close()
s.close()
