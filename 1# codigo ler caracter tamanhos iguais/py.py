import cv2
import numpy as np

digits = cv2.imread("digits.png", cv2.IMREAD_GRAYSCALE)
test_digits = cv2.imread("test_digits.png", cv2.IMREAD_GRAYSCALE)
rows = np.vsplit(digits, 100)

cv2.imshow("row 0", digits)
cv2.waitKey(0)

cv2.destroyAllWindows()
