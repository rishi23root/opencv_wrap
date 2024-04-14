import numpy as np


class Singleton:
    """Singleton class using __new__ method.
    This class can be used as a base class for other classes for singleton.
    provides a single instance of the class.
    and store the instance in the class variable _instance
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        # save the kwargs for the instance
        cls.verbose = kwargs.get("verbose", False)
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            if cls.verbose:
                print(f"[{cls.__name__}]", "New Singleton Instance Created")
        return cls._instance

    @property
    def isVerbose(self):
        """return the verbose status of the class.

        Returns
        -------
        bool
            verbose status of the class.
        """
        if self.verbose:
            print(f"[{self.__class__.__name__}]", "Verbose Mode is ON")
        return self.verbose


class Detector(Singleton):
    """Detector class using Singleton class.
    This class can be used as a base class for other detector classes.
    handle creation and mangement of the detector instances.
    """

    _detector = None

    def detect(self, image: np.ndarray, *args, **kwargs):
        """process the detection in the images and \
            return the results of the detection.

        Parameters
        ----------
        image : np.ndarray
            image to be detected.

        Returns
        -------
        detection results
        """
        if self._detector is None:
            raise NotImplementedError(
                f"[{self.__class__.__name__}] Detector not implemented."
            )

        if image is None or not isinstance(image, np.ndarray):
            raise ValueError(
                f"[{self.__class__.__name__}] Image \
                    not provided."
            )

        return self._detector(image, *args, **kwargs)

    def __enter__(self):
        return self.__class__._instance

    def __exit__(self, exc_type, exc_val, exc_tb):
        # show error in good way
        if exc_type:
            print(exc_type, exc_val, exc_tb)
            return True
        return False
