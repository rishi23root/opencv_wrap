import cv2
from utils.base import Detector


class Face(Detector):
    def __init__(self, *args, **kwargs):

        if self._detector is None:
            detectorModule = cv2.CascadeClassifier(
                cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            )
            # laod the detector here
            self._detector = lambda x: detectorModule.detectMultiScale(x, 1.3, 5)
        # print(self._detector)


if __name__ == "__main__":
    d1 = Face(verbose=True)
    d2 = Face()

    image = cv2.imread("./test/test.jpg")
    print(d1.detect(image))
    print("isinstance of face :", isinstance(d1, Face), end=" ")
    print("is i1 == i2 :", d1 == d2)
