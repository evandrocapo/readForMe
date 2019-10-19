import socket
import sys
import threading
import base64
import cv2
import os
import pytesseract as ocr
import numpy as np
from PIL import Image
from gtts import gTTS


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

	# convertendo em um array editavel de numpy[x, y, CANALS]
	npimagem = np.asarray(imagem).astype(np.uint8)

	# diminuio dos ruidos antes da binarizao
	npimagem[:, :, 0] = 0 # zerando o canal R (RED)
	npimagem[:, :, 2] = 0 # zerando o canal B (BLUE)

	# atribuio em escala de cinza
	im = cv2.cvtColor(npimagem, cv2.COLOR_RGB2GRAY)

	ret, thresh = cv2.threshold(im, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)

	# reconvertendo o retorno do threshold em um objeto do tipo PIL.Image
	binimagem = Image.fromarray(thresh)

	# chamada ao tesseract OCR por meio de seu wrapper
	phrase = ocr.image_to_string(binimagem, lang='por')

	# imprao do resultado
	return phrase


def main():

	# "192.168.42.85"
	HOST = "192.168.42.193"	# Symbolic name meaning all available interfaces
	PORT = 8888	# Arbitrary non-privileged port
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

	# Now keep talking with the client
	while 1:
	    # Wait to accept a connection - blocking call
		conn, addr = s.accept()
		print ('Connected with ' + addr[0] + ':' + str(addr[1]))
		final = ""
		size = 0
		# data = conn.recv(4)
		# print("Received size: " + str(size.from_bytes(data,'big')))
		# size = size.from_bytes(data,'big')

		# Infinite loop so that function do not terminate
		while True:
			# print("Looking for more")
			# Receiving from client
			data = conn.recv(1024)
			final += data.decode("utf-8")
			# size -= 1024
			#  print(size)
			# if size <= 0:
			if not data:
				print("Breaking")
				break

		# print("Received all")
		decodeImage(final)
		reply = readImage()
		# 	#reply = readImage()
		print(reply)
		if reply == "":
			reply= "Não consegui ler"
		myobj = gTTS(text=reply, lang='pt', slow=False)
		myobj.save("speech.mp3")
		os.system("mpg321 speech.mp3")


		# conn.sendall(reply.encode())
		# # End of Loop

	conn.close()
	s.close()

if __name__ == "__main__":
	main()
