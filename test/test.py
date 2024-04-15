# flake8: noqa: E501
from opencv_wrap import cv2Decorator
import cv2
from opencv_wrap.detectors import Face
from opencv_wrap.utils.helper import saveFrame, detectionBox, show_all_frames, clipImage


# reading a single frame from the directory

# @cv2Decorator.TotalTimeTaken(show=True)
# @cv2Decorator.DetectInEachFrame(detector=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml"),name='face')
# @cv2Decorator.CalculateFps(draw = True)
# @cv2Decorator.MirrorFrame()
# @cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_BGR2GRAY)
# def all_actions(**kwargs):
#     frame = kwargs['frame']
#     # detect face from trainerd data and detectMultiScale use to deteat every size of face
#     face_coordinate = kwargs['face'].detectMultiScale(kwargs['color_converted'],1.3,5)
#     detectionBox(detectedArr=face_coordinate, frame=frame)
#     return kwargs

# frame = cv2.imread('./testMedia/test.jpg')

# kwargs = all_actions(frame=frame)
# cv2.imshow('frame',kwargs['frame'])
# key = cv2.waitKey(0)


# reading a video from the directory


# @cv2Decorator.DetectInEachFrame(
#     detector=cv2.CascadeClassifier(
#         cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
#     ),
#     name="face",
# )
@cv2Decorator.DetectInEachFrame(
    detector=Face(verbose=True),
    name="face",
)
@cv2Decorator.TotalTimeTaken(show=True)
# @cv2Decorator.AccessCamOrVideo(show=False, videoPath="./testMedia/test.mp4", fps=12)
@cv2Decorator.AccessCamOrVideo(show=False, fps=12)
@cv2Decorator.CalculateFps(draw=True)
@cv2Decorator.MirrorFrame()
@cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_BGR2GRAY)
@cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_RGB2BGR, frameName="bgr_frame")
def all_actions(**kwargs):
    # detect face from trainerd data and detectMultiScale use to deteat every size of face
    # face_coordinate = kwargs["face"].detectMultiScale(kwargs["greyScale"], 1.3, 5)
    mainFrameCopy = kwargs["frame"].copy()
    processed = kwargs["face"].detect(kwargs["bgr_frame"])
    face_coordinate = kwargs["face"].getDetectionBox(
        processed, kwargs["frame"], draw=True
    )
    kwargs["face"].drawLandmarks(processed, kwargs["frame"])
    # print(len(face_coordinate))

    kwargs["detected"] = [clipImage(mainFrameCopy, i) for i in face_coordinate]
    # saveFrame(frame=frame,count=kwargs['frame_count'],destination='./test2')

    # detectionBox(detectedArr=face_coordinate, frame=kwargs["frame"])
    # show_all_frames(kwargs,keysToShow=['frame','greyScale','mirror_frame','detected'])
    # show_all_frames(kwargs,keysToShow=['frame','greyScale','mirror_frame'])
    show_all_frames(kwargs, keysToShow=["frame", "detected"])
    return kwargs


kwargs = all_actions()


# reading the cam feed
# @cv2Decorator.TotalTimeTaken(show=True)
# @cv2Decorator.DetectInEachFrame(detector=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml"),name='face')
# @cv2Decorator.AccessCamOrVideo(show=True)
# @cv2Decorator.CalculateFps(draw = True)
# @cv2Decorator.MirrorFrame()
# @cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_BGR2GRAY)
# def all_actions(**kwargs):
#     frame = kwargs['frame']
#     # detect face from trainerd data and detectMultiScale use to deteat every size of face
#     face_coordinate = kwargs['face'].detectMultiScale(kwargs['color_converted'],1.3,5)
#     # saveFrame(frame=frame,count=kwargs['frame_count'],destination='./test2')
#     detectionBox(detectedArr=face_coordinate, frame=frame)
#     return kwargs

# kwargs = all_actions()

# print("last ",all_actions().keys())
# print("last ",all_actions().keys())
