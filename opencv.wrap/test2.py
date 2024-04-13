import cv2
from detectors.Face import Face

if __name__ == "__main__":
    d1 = Face(verbose=True)
    d2 = Face()

    image = cv2.imread("./test/test.jpg")
    print(d1.detect(image))
    print("isinstance of face :", isinstance(d1, Face), end=" ")
    print("is i1 == i2 :", d1 == d2)
