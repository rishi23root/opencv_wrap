from typing import overload
import cv2
import pprint
import mediapipe as mp
import time
import traceback
from cv2Decorator import cv2Decorator

class handDetector():
    imgPadding= 30
    def __init__(self, mode=False, maxHands=2, detectionCon=0.5, trackCon=0.5):
        """initialization"""
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        
        # 'initialization the mp hands'
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
                            self.mode,
                            self.maxHands,
                            self.detectionCon,
                            self.trackCon)
        self.mpDraw = mp.solutions.drawing_utils
        self.overlap_shape = (200,200)

    def findHands(self, frame, draw=False):
        """Detect the hand form the images and return the HandCount and frame"""
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        frameRGB.flags.writeable = False
        self.results = self.hands.process(frameRGB)
        # print(self.results.multi_hand_landmarks)
        if self.results.multi_hand_landmarks:
            for handLms in self.results.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(
                        frame,
                        handLms,
                        self.mpHands.HAND_CONNECTIONS)
            else :
                return len(self.results.multi_hand_landmarks), frame
        else :
            return 0, frame

    def findHandsAndPosture(self, frame, handNo=0, draw=False):
        """detect the hand ,posture and then return a int and the frame
           0: rock 
           1: paper 
           2: scissor 
           3: None 
        """
        # extract the hands form the image
        frameRGB = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        frameRGB.flags.writeable = False
        self.results = self.hands.process(frameRGB)
        # print(self.results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            try :
                # get the frame shape and size for future calculation
                h, w, c = frame.shape
                # if hand in list
                handLms = self.results.multi_hand_landmarks[handNo] 
                # for testing draw the landmarks
                if draw:
                    # print(f"{draw=} Hand Founded    ")
                    self.mpDraw.draw_landmarks(
                        frame,
                        handLms,
                        self.mpHands.HAND_CONNECTIONS)

                end_frame = [0,0]
                start_frame = [w,h]
                lmList = []
                for id,lm in enumerate(handLms.landmark):
                    # convert landmark to pixle possitions
                    entry = (id, int(lm.x * w), int(lm.y * h))
                    # for find the small hand frame 
                    if entry[1] > end_frame[0]:
                        end_frame[0] = entry[1] 
                    if entry[2] > end_frame[1]:
                        end_frame[1] = entry[2] 
                    if entry[1] < start_frame[0]:
                        start_frame[0] = entry[1] 
                    if entry[2] < start_frame[1]:
                        start_frame[1] = entry[2] 
                    lmList.append(entry)

                if draw:
                    cv2.rectangle(
                        frame,
                        (end_frame[0] + self.imgPadding,end_frame[1] + self.imgPadding),
                        (start_frame[0] - self.imgPadding,start_frame[1] - self.imgPadding),
                        (0,255,0),
                        2)

                # draw on the frame 
                at = [0,0]
                try :
                    roiImage = cv2.resize(
                            frame[
                                start_frame[1] - self.imgPadding : end_frame[1] + self.imgPadding,
                                start_frame[0] - self.imgPadding : end_frame[0] + self.imgPadding
                            ],
                            self.overlap_shape)
                    # strainght the image and detect the posture
                    postureInt, roiImage = self.findPosture(roiImage)
                    frame[at[1]:self.overlap_shape[0],at[0]:self.overlap_shape[1]] = roiImage
                except:
                    # print(traceback.format_exc())
                    postureInt = 0 

            except IndexError:
                print(f"{handNo=} Hand not Found")
            except Exception as e :
                print(traceback.format_exc())
                # print(getattr(e, 'message', repr(e)))
                # print(getattr(e, 'message', str(e)))
        else :
            # no hand posture detected
            postureInt = 0
        
        return postureInt, frame

    def findPosture(self,frame):
        """find the fingurs """
        h,w,c = frame.shape
        count, roiImg = self.findHands(frame,draw=False)


        
        # convert landmark to pixle possitions

        # possitions = [(id, int(lm.x * w), int(lm.y * h)) for id,lm in enumerate(self.results.multi_hand_landmarks[0].landmark)]

        # pointing the figers up
        # WRIST


        # print(possitions)
        # print(possitions)
        # [(0, 103, 186), (1, 68, 173), (2, 47, 146), (3, 35, 122), (4, 22, 103), (5, 79, 105), (6, 76, 69), (7, 76, 47), (8, 76, 28), (9, 103, 105), (10, 108, 67), (11, 112, 44), (12, 117, 24), (13, 124, 113), (14, 134, 79), (15, 141, 57), (16, 146, 39), (17, 142, 127), (18, 159, 105), (19, 169, 90), (20, 177, 77)]

        # img = cv2.rotate(roiImage, cv2.ROTATE_90_COUNTERCLOCKWISE)


        # detect the postureInt and update the value of the variable
        # 1. detect all the figers open  ==> paper
        # else :
        # 2. detect middle and index figers 
        # else :
        # detect if hand all figure close   


        # print(dir(self.mpHands.HandLandmark) ) --> ['INDEX_FINGER_DIP', 'INDEX_FINGER_MCP', 'INDEX_FINGER_PIP', 'INDEX_FINGER_TIP', 'MIDDLE_FINGER_DIP', 'MIDDLE_FINGER_MCP', 'MIDDLE_FINGER_PIP', 'MIDDLE_FINGER_TIP', 'PINKY_DIP', 'PINKY_MCP', 'PINKY_PIP', 'PINKY_TIP', 'RING_FINGER_DIP', 'RING_FINGER_MCP', 'RING_FINGER_PIP', 'RING_FINGER_TIP', 'THUMB_CMC', 'THUMB_IP', 'THUMB_MCP', 'THUMB_TIP', 'WRIST', '__class__', '__doc__', '__members__', '__module__']
        
        # hand detection first get all the extreams points
        # to cut the frame and use it for detection 
        # 1. algo to get all the extream  

         # sides of the figure
                # edges = [
                #     [end_frame[0],-end_frame[1]],
                #     [end_frame[0],-start_frame[1]],
                #     [-end_frame[1],start_frame[0]],
                #     [start_frame[0],-start_frame[1]]
                #     ]

                # # make the side butoom to flaten the hand is the shortest distance from the base line 
                # # print(f"{lmList[self.mpHands.HandLandmark.WRIST]=}")
                # for i in range(len(edges)):
                #     if i < 2:
                #         a = Cordinate(
                #             edges[i],
                #             edges[i+1]).perpendicular_distance(*lmList[self.mpHands.HandLandmark.WRIST][1:])
                #     else :
                #         a = Cordinate(
                #             edges[i],
                #             edges[0]).perpendicular_distance(*lmList[self.mpHands.HandLandmark.WRIST][1:])
                #     print(a)

        return 0,roiImg


if __name__ == "__main__":
    # handDetector()
    pass