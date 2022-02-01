import cv2

img_file = "test.png"
img = cv2.imread(img_file, cv2.IMREAD_COLOR)
gray = cv2.imread(img_file, cv2.IMREAD_GRAYSCALE)
unchange = cv2.imread(img_file, cv2.IMREAD_UNCHANGED)

cv2.imshow('original', img)
cv2.imshow('Gray', gray)
cv2.imshow('Unchange', unchange)

cv2.waitKey(0)
cv2.destroyAllWindows()