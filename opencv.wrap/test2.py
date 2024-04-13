""" this is the way """

from utils.base import Detector


class Face(Detector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # laod the detector here

        if not hasattr(self, "_detector"):
            self._detector = self.__class__._detector
            print("genrating Face instance", self._instance)

    def detect(self, image):
        return self._detector.detect(image)


class Hand(Detector):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # laod the detector here

        if not hasattr(self, "_detector"):
            self._detector = self.__class__._detector
            print("genrating Face instance", self._instance)

    def detect(self, image):
        return self._detector.detect(image)


if __name__ == "__main__":
    d1 = Face(verbose=True)
    d2 = Face()
    print(d1._detector)
    d1 = Hand(verbose=True)
    d2 = Hand()
    print(d1._detector)
