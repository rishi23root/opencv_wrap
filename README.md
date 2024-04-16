# opencv_wrap

A collection of decorators for opencv and helper functions for multiple opencv tasks.

Working with opencv can be quite a hussel, a lot of boiler code, nested functions for specific use cases, this package is designed to make it easier to work with opencv, while focusing on the main task in hand. best for prototyping and quick testing. second part is speed and performance, this package is designed to be fast and efficient.

---

Built with ☕ by [@rishi23root](https://github.com/rishi23root/)

[rishi23root/opencv_wrap/](https://github.com/rishi23root/opencv_wrap/)

[![GitHub stars](https://img.shields.io/github/stars/rishi23root/opencv_wrap.svg)](https://github.com/rishi23root/opencv_wrap/stargazers)
[![PyPI](https://img.shields.io/pypi/v/opencv_wrap.svg)](https://pypi.org/project/opencv_wrap/)
[![GitHub](https://img.shields.io/github/license/rishi23root/opencv_wrap.svg)](https://github.com/rishi23root/opencv_wrap/blob/master/LICENSE) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg) [![Say Thanks!](https://img.shields.io/badge/Say%20Thanks-:D-1EAEDB.svg)](https://saythanks.io/to/rishi23root)

# Installation

```bash
pip install opencv-wrap
```

> **Very basic example of reading camera feed and displaying it. with just 5 lines of code. 😎**

```python
from opencv_wrap import cv2Decorator

@cv2Decorator.TotalTimeTaken(show=True)
@cv2Decorator.AccessCamOrVideo(show=True)
@cv2Decorator.CalculateFps(draw=True)
def all_actions(**kwargs):
    return kwargs

all_actions()
```

> **Advance example of face detection and smart viewer. with just 23 lines of code. 😊**

```python
from opencv_wrap import cv2Decorator
import cv2
from opencv_wrap.detectors import Face
from opencv_wrap.utils.helper import show_all_frames, clipImage

@cv2Decorator.DetectInEachFrame(detector=Face(verbose=True),name="face")
@cv2Decorator.TotalTimeTaken(show=True)
@cv2Decorator.AccessCamOrVideo(show=False,videoPath="./opencv_wrap/testMedia/test.mp4")  # path to video
@cv2Decorator.CalculateFps(draw=False)
@cv2Decorator.MirrorFrame()
@cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_RGB2BGR, frameName="bgr_frame")
def all_actions(**kwargs):
    mainFrameCopy = kwargs["frame"].copy()
    processed = kwargs["face"].detect(kwargs["bgr_frame"])
    face_coordinate = kwargs["face"].getDetectionBox(
        processed, kwargs["frame"], draw=True
    )
    kwargs["face"].getLandmarks(processed, kwargs["frame"], draw=True)
    kwargs["detected"] = [clipImage(mainFrameCopy, i) for i in face_coordinate]
    show_all_frames(kwargs, keysToShow=["frame", "detected"])
    return kwargs

all_actions()
```

![image](https://rishi23root.github.io/opencv_wrap/static/Screenshot%20from%202024-04-16%2005-21-50.png)

---

## Features with decorators

```python
from opencv_wrap import cv2Decorator

@cv2Decorator.TotalTimeTaken(show=True)
...
```

- TotalTimeTaken
- CalculateFps
- MirrorFrame
- ConvertCOLOR
- AccessCamOrVideo
- DetectInEachFrame

## Utils to help you with opencv tasks

```python
from opencv_wrap.utils import DetectorClass
from opencv_wrap.utils.helper import detectionBox
```

#### Detector Parent

DetectorClass is a base class for all the detectors. provide some basic functions like Singleton and isVerbose.

#### Helper functions

- `saveFrames`
- `detectionBox`
- `detectionBox`
- `resizeImage`
- `clipImage`
- `added_title`
- `combine_images`

## Detection Classes

```python
from opencv_wrap.detectors import Face , Hand, Pose
```

- Face detection
- Hand detection
- Pose detection
- eye detection (yet to be added)

> you can reconstruct the `detector` classes as per your need. 😊

like extend the class and add more functions to it. like action of certain detections.

> **example**, blur everything but face. can be useful when you want to hide the background and just fucus on the object, here Face.

```python
import cv2
from opencv_wrap import cv2Decorator
from opencv_wrap.detectors import Face

class FaceExtented(Face):
    def blurEverytingButFace(self, frame, face_coordinate):
        # make a copy of the frame
        frameCopy = frame.copy()
        frame = cv2.blur(frame, (50,50))
        for (x, y, w, h) in face_coordinate:
            frame[y : y + h, x : x + w] = frameCopy[y : y + h, x : x + w]
        return frame

@cv2Decorator.DetectInEachFrame(detector=FaceExtented(verbose=True),name="face")
@cv2Decorator.AccessCamOrVideo(show=True,videoPath="./opencv_wrap/testMedia/test.mp4")
@cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_RGB2BGR, frameName="bgr_frame")
def all_actions(\*\*kwargs):
    processed = kwargs["face"].detect(kwargs["bgr_frame"])
    face_coordinate = kwargs["face"].getDetectionBox(
    processed, kwargs["frame"], draw=False,padding_ratio=0.4)
    kwargs["frame"] = kwargs["face"].blurEverytingButFace(kwargs["frame"], face_coordinate)
    return kwargs

all_actions()
```

![image](https://rishi23root.github.io/opencv_wrap/static/Screenshot%20from%202024-04-16%2006-06-26.png)

---

> ## OPEN FOR CONTRIBUTIONS 🤝

#### Steps to start contributing

0. Star the repo 🌟
1. Fork the repo 👨‍💻
2. Clone the repo 📂
3. Create a new issue 🔖
4. Make changes 📜
5. Push the changes 🚀
6. Create a pull request 🌐

---

## More Usage Examples

> **Example 1** : Reading a single frame from the directory

```python
@cv2Decorator.DetectInEachFrame(
    detector=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml"),
    name='face')
@cv2Decorator.MirrorFrame()
@cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_BGR2GRAY)
def all_actions(**kwargs):
    frame = kwargs['frame']
    # detect face from trainerd data and detectMultiScale use to deteat every size of face
    face_coordinate = kwargs['face'].detectMultiScale(kwargs['greyScale'],1.3,5)
    detectionBox(detectedArr=face_coordinate, frame=frame)
    return kwargs

frame = cv2.imread('./opencv_wrap/testMedia/test.jpg')

kwargs = all_actions(frame=frame)
cv2.imshow('frame',kwargs['frame'])
key = cv2.waitKey(0)
```

> **Example 2** : Reading cam and detecting Hand in each frame

```python
@cv2Decorator.DetectInEachFrame(
    detector=Hand(verbose=True),
    name="hand",
)
@cv2Decorator.TotalTimeTaken(show=True)
@cv2Decorator.AccessCamOrVideo(show=False, fps=12)
@cv2Decorator.CalculateFps(draw=True)
@cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_RGB2BGR, frameName="bgr_frame")
def all_actions(**kwargs):
    mainFrameCopy = kwargs["frame"].copy()
    processed = kwargs["hand"].detect(kwargs["bgr_frame"])
    face_coordinate = kwargs["hand"].getDetectionBox(
        processed, kwargs["frame"], draw=True
    )
    kwargs["hand"].getLandmarks(processed, kwargs["frame"],draw=True)
    # print(len(face_coordinate))
    kwargs["detected"] = [clipImage(mainFrameCopy, i) for i in face_coordinate]
    show_all_frames(kwargs, keysToShow=["frame", "detected"])
    return kwargs


kwargs = all_actions()
```

> **Example 3** : Reading video and detecting Pose in each frame

```python
@cv2Decorator.DetectInEachFrame(
    detector=Pose(verbose=True),
    name="pose",
)
@cv2Decorator.TotalTimeTaken(show=True)
@cv2Decorator.AccessCamOrVideo(show=False, videoPath="./opencv_wrap/testMedia/test.mp4", fps=12)
@cv2Decorator.CalculateFps(draw=True)
@cv2Decorator.MirrorFrame()
@cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_BGR2GRAY)
@cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_RGB2BGR, frameName="bgr_frame")
def all_actions(**kwargs):
    mainFrameCopy = kwargs["frame"].copy()
    processed = kwargs["pose"].detect(kwargs["bgr_frame"])
    face_coordinate = kwargs["pose"].getDetectionBox(
        processed, kwargs["frame"], draw=True
    )
    kwargs["pose"].getLandmarks(processed, kwargs["frame"],draw=True)

    kwargs["detected"] = [clipImage(mainFrameCopy, i) for i in face_coordinate]
    show_all_frames(kwargs, keysToShow=["frame", "detected"])
    return kwargs


all_actions()
```

> **Example 4** : Reading video and saving each frame in a folder

```python
from opencv_wrap import cv2Decorator
from opencv_wrap.utils.helper import saveFrame

@cv2Decorator.AccessCamOrVideo(show=True, videoPath="./opencv_wrap/testMedia/test.mp4", )
def all_actions(**kwargs):
    saveFrame(kwargs['frame'],kwargs['frame_count'],destination='./output')
    return kwargs

all_actions()
```

![image](https://rishi23root.github.io/opencv_wrap/static/Screenshot-20240416071523-780x68.png)

> **Example 5** : Reading video and show converted frame in smart view

```python
@cv2Decorator.TotalTimeTaken(show=True)
@cv2Decorator.AccessCamOrVideo(show=False, videoPath="./opencv_wrap/testMedia/test.mp4", fps=12)
@cv2Decorator.CalculateFps(draw=True)
@cv2Decorator.MirrorFrame()
@cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_BGR2GRAY)
def all_actions(**kwargs):
    show_all_frames(kwargs,keysToShow=['frame','greyScale','mirror_frame'])
    return kwargs

all_actions()
```

![image](https://rishi23root.github.io/opencv_wrap/static/Screenshot-20240416071956-1175x661.png)
---

# Future Updates

- [ ] Face recognition
- [ ] Eye detection
- [ ] Object detection
- [ ] Image classification
- [ ] segmentation (decorator)
- [ ] making whole program faster by atleast 10x using cython
