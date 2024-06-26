# flake8: noqa: E501
from opencv_wrap import cv2Decorator
import cv2
from opencv_wrap.detectors import Face, Hand, Pose
from opencv_wrap.utils.helper import saveFrame, detectionBox, show_all_frames, clipImage


# reading a single frame from the directory

# @cv2Decorator.DetectInEachFrame(detector=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml"),name='face')
# @cv2Decorator.MirrorFrame()
# @cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_BGR2GRAY)
# def all_actions(**kwargs):
#     frame = kwargs['frame']
#     # detect face from trainerd data and detectMultiScale use to deteat every size of face
#     face_coordinate = kwargs['face'].detectMultiScale(kwargs['greyScale'],1.3,5)
#     detectionBox(detectedArr=face_coordinate, frame=frame)
#     return kwargs

# frame = cv2.imread('./opencv_wrap/testMedia/test.jpg')

# kwargs = all_actions(frame=frame)
# cv2.imshow('frame',kwargs['frame'])
# key = cv2.waitKey(0)


# reading a video from the directory


# face detection
# @cv2Decorator.DetectInEachFrame(
#     detector=Face(verbose=True),
#     name="face",
# )
# @cv2Decorator.TotalTimeTaken(show=True)
# # @cv2Decorator.AccessCamOrVideo(show=False, videoPath="./opencv_wrap/testMedia/test.mp4", fps=12)
# @cv2Decorator.AccessCamOrVideo(show=False)
# @cv2Decorator.CalculateFps(draw=True)
# @cv2Decorator.MirrorFrame()
# @cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_BGR2GRAY)
# @cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_RGB2BGR, frameName="bgr_frame")
# def all_actions(**kwargs):
#     # detect face from trainerd data and detectMultiScale use to deteat every size of face
#     # face_coordinate = kwargs["face"].detectMultiScale(kwargs["greyScale"], 1.3, 5)
#     mainFrameCopy = kwargs["frame"].copy()
#     processed = kwargs["face"].detect(kwargs["bgr_frame"])
#     face_coordinate = kwargs["face"].getDetectionBox(
#         processed, kwargs["frame"], draw=True
#     )
#     kwargs["face"].getLandmarks(processed, kwargs["frame"])
#     # print(len(face_coordinate))

#     kwargs["detected"] = [clipImage(mainFrameCopy, i) for i in face_coordinate]
#     # saveFrame(frame=frame,count=kwargs['frame_count'],destination='./test2')

#     # detectionBox(detectedArr=face_coordinate, frame=kwargs["frame"])
#     # show_all_frames(kwargs,keysToShow=['frame','greyScale','mirror_frame','detected'])
#     # show_all_frames(kwargs,keysToShow=['frame','greyScale','mirror_frame'])
#     show_all_frames(kwargs, keysToShow=["frame", "detected"])
#     return kwargs


# kwargs = all_actions()


# Hand
@cv2Decorator.DetectInEachFrame(
    detector=Hand(verbose=True),
    name="hand",
)
@cv2Decorator.TotalTimeTaken(show=True)
# @cv2Decorator.AccessCamOrVideo(show=False, videoPath="./opencv_wrap/testMedia/test.mp4", fps=12)
@cv2Decorator.AccessCamOrVideo(show=False, fps=12)
@cv2Decorator.CalculateFps(draw=True)
@cv2Decorator.MirrorFrame()
@cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_BGR2GRAY)
@cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_RGB2BGR, frameName="bgr_frame")
def all_actions(**kwargs):
    # detect hand from trainerd data and detectMultiScale use to deteat every size of hand
    # face_coordinate = kwargs["hand"].detectMultiScale(kwargs["greyScale"], 1.3, 5)
    mainFrameCopy = kwargs["frame"].copy()
    processed = kwargs["hand"].detect(kwargs["bgr_frame"])
    face_coordinate = kwargs["hand"].getDetectionBox(
        processed, kwargs["frame"], draw=True
    )
    kwargs["hand"].getLandmarks(processed, kwargs["frame"], draw=True)
    # print(len(face_coordinate))

    kwargs["detected"] = [clipImage(mainFrameCopy, i) for i in face_coordinate]
    # saveFrame(frame=frame,count=kwargs['frame_count'],destination='./test2')

    # detectionBox(detectedArr=face_coordinate, frame=kwargs["frame"])
    # show_all_frames(kwargs,keysToShow=['frame','greyScale','mirror_frame','detected'])
    # show_all_frames(kwargs,keysToShow=['frame','greyScale','mirror_frame'])
    show_all_frames(kwargs, keysToShow=["frame", "detected"])
    return kwargs


kwargs = all_actions()


# pose detection


# @cv2Decorator.DetectInEachFrame(
#     detector=Pose(verbose=True),
#     name="pose",
# )
# @cv2Decorator.TotalTimeTaken(show=True)
# @cv2Decorator.AccessCamOrVideo(show=False, videoPath="./opencv_wrap/testMedia/test.mp4", fps=12)
# # @cv2Decorator.AccessCamOrVideo(show=False, fps=12)
# @cv2Decorator.CalculateFps(draw=True)
# @cv2Decorator.MirrorFrame()
# @cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_BGR2GRAY)
# @cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_RGB2BGR, frameName="bgr_frame")
# def all_actions(**kwargs):
#     # detect pose from trainerd data and detectMultiScale use to deteat every size of pose
#     # face_coordinate = kwargs["pose"].detectMultiScale(kwargs["greyScale"], 1.3, 5)
#     mainFrameCopy = kwargs["frame"].copy()
#     processed = kwargs["pose"].detect(kwargs["bgr_frame"])
#     face_coordinate = kwargs["pose"].getDetectionBox(
#         processed, kwargs["frame"], draw=True
#     )
#     kwargs["pose"].getLandmarks(processed, kwargs["frame"], draw=True)
#     # print(len(face_coordinate))

#     kwargs["detected"] = [clipImage(mainFrameCopy, i) for i in face_coordinate]
#     # saveFrame(frame=frame,count=kwargs['frame_count'],destination='./test2')

#     # detectionBox(detectedArr=face_coordinate, frame=kwargs["frame"])
#     # show_all_frames(kwargs,keysToShow=['frame','greyScale','mirror_frame','detected'])
#     # show_all_frames(kwargs,keysToShow=['frame','greyScale','mirror_frame'])
#     show_all_frames(kwargs, keysToShow=["frame", "detected"])
#     return kwargs


# all_actions()


# reading the cam feed
# @cv2Decorator.TotalTimeTaken(show=True)
# @cv2Decorator.DetectInEachFrame(detector=cv2.CascadeClassifier(cv2.data.haarcascades+"haarcascade_frontalface_default.xml"),name='face')
# @cv2Decorator.AccessCamOrVideo(show=True, videoPath="./opencv_wrap/testMedia/test.mp4", )
# @cv2Decorator.CalculateFps(draw = True)
# @cv2Decorator.MirrorFrame()
# @cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_BGR2GRAY)
# def all_actions(**kwargs):
#     frame = kwargs['frame']
#     # detect face from trainerd data and detectMultiScale use to deteat every size of face
#     face_coordinate = kwargs['face'].detectMultiScale(kwargs['greyScale'],1.3,5)
#     # saveFrame(frame=frame,count=kwargs['frame_count'],destination='./test2')
#     detectionBox(detectedArr=face_coordinate, frame=frame)
#     return kwargs

# a = all_actions()
# print(a['frame_count'])


# show converted frames in smart view
# @cv2Decorator.TotalTimeTaken(show=True)
# @cv2Decorator.AccessCamOrVideo(show=False, videoPath="./opencv_wrap/testMedia/test.mp4", fps=12)
# @cv2Decorator.CalculateFps(draw=True)
# @cv2Decorator.MirrorFrame()
# @cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_BGR2GRAY)
# def all_actions(**kwargs):
#     show_all_frames(kwargs,keysToShow=['frame','greyScale','mirror_frame'])
#     return kwargs

# all_actions()
