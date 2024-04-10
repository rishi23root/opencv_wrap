

class baseDetector:
    def __init__(self):
        # implement singletons for the detectors sub classes
        # if self.__class__._detector
        #     self._detector = self.__class__._detector
        # else:
        #     self.__class__._detector
        self._detector = None

    def detect(self, image):
        return self._detector.detect(image)