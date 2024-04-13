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
                print("New Singleton Instance for Class :", cls.__name__)
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
            print("Verbose Mode is ON for Class :", self.__class__.__name__)
        return self.verbose


class Detector(Singleton):
    """Detector class using Singleton class.
    This class can be used as a base class for other detector classes.
    handle creation and mangement of the detector instances.
    using queue to execute the detector requests."""

    _detector = None

    def __init__(self, *args, **kwargs):
        if self.isVerbose:
            print("genrating Detector instance", self._instance)

        # laod the detector here
        if not hasattr(self, "_detector"):
            self._detector = self.__class__._detector
