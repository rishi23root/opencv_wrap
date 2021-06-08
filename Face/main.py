from time import sleep as nap
from typing import ValuesView
import cv2
from cv2Decorator import cv2Decorator
from FaceDetecter import Face

needToDraw = False

@cv2Decorator.TotalTimeTaken(show = True)
@cv2Decorator.ReadCamAddDetectShowFrames_video(videoPath='test.mp4',detector = (Face,))
@cv2Decorator.CalculateFps(draw = needToDraw)
@cv2Decorator.MirrorFrame()
@cv2Decorator.ConvertCOLOR(converter = None)
def all_actions(frame,detector):
    # all the action on the frames 
    frame = detector.detectFaceAndCenter(frame,draw = needToDraw)
    # frame = detector.detectFaceAndShow(frame,draw = needToDraw)
    # frame = detector.detectFace(frame,draw = needToDraw)
    return frame

# @cv2Decorator.TotalTimeTaken(show = True)
# @cv2Decorator.ReadCamAddDetectShowFrames(detector = (Face,))
# @cv2Decorator.CalculateFps(draw = needToDraw)
# @cv2Decorator.MirrorFrame()
# @cv2Decorator.ConvertCOLOR(converter = None)
# def all_actions(frame,detector):
#     # all the action on the frames 
#     frame = detector.detectFace(frame,draw = needToDraw)
#     return frame

all_actions()


# updates
# 1. add this to the open cv2 project 
# 2. and update to use these in hand detection and 
# 3. rock, paper and scissor game 