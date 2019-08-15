import cv2
import numpy as np

digits = cv2.imread("digits.png", cv2.IMREAD_GRAYSCALE)
test_digits = cv2.imread("test_digits2.png", cv2.IMREAD_GRAYSCALE)

rows = np.vsplit(digits, 50)  # separa em linhas
cells = []
for row in rows:
    row_cells = np.hsplit(row, 50)  # separa em colunas 
    for cell in row_cells:
        cell = cell.flatten() # cell = vetor(cada linha) -> flatten = retirar vetor ( deixar apenas um vetor )
        cells.append(cell) # salvar o unico vetor(sequencia de numeros da imagem) em um vetor
cells = np.array(cells, dtype=np.float32)

k = np.arange(10) # configurando o label do dataset
cells_labels = np.repeat(k, 250) # label do dataset

test_digits = np.vsplit(test_digits, 4)
test_cells = []
for d in test_digits:
    d = d.flatten()
    test_cells.append(d)
test_cells = np.array(test_cells, dtype=np.float32)


#cv2.imshow("hm", test_cells[0])
#cv2.imshow("hm2", test_cells)
#cv2.waitKey(0)
#cv2.destroyAllWindows()


# Cells = Foto de cada celular
# Cells_labels = labels da foto

# KNN
knn = cv2.ml.KNearest_create() # Criar o algoritmo KNN
knn.train(cells, cv2.ml.ROW_SAMPLE, cells_labels) # Treina o dataset
ret, result, neighbours, dist = knn.findNearest(test_cells, k=1) # Roda o algoritmo

print(result)