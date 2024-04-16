import mediapipe as mp
from opencv_wrap.utils import DetectorClass
from opencv_wrap.utils.helper import detectionBox


mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils


class HandDetector(DetectorClass):

    def __init__(
        self,
        max_num_hands=2,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        verbose=False,
    ):
        if self._detector is None:
            self.hands = mp_hands.Hands(
                max_num_hands=max_num_hands,
                min_detection_confidence=min_detection_confidence,
                min_tracking_confidence=min_tracking_confidence,
            )
            self._detector = self.processFrame

    def processFrame(self, frame):
        """process frame and extract the hand features

        Parameters
        ----------
        frame : np.array
            frame to process

        Returns
        -------
        landmarks
            output of hands.process function
        """
        return self.hands.process(frame)
    

    def getDetectionBox(self, processedFrame, frame, padding_ratio=0.2, draw=False):
        """return the detected box from the processed frame, here face

        Parameters
        ----------
        processedFrame : 
            output of processFrame function
        frame : np.array
            frame to draw the box on
        padding_ratio : float, optional
            padding ratio for the box, by default 0.2
        draw : bool, optional
            draw the box on the frame, by default False

        Returns
        -------
        list
            list of boxes
        """
        hand_boxes = []
        if processedFrame.multi_hand_landmarks:
            for hand_landmarks in processedFrame.multi_hand_landmarks:
                h, w, _ = frame.shape
                cx_min = w
                cy_min = h
                cx_max = cy_max = 0
                for lm in hand_landmarks.landmark:
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    if cx < cx_min:
                        cx_min = cx
                    if cy < cy_min:
                        cy_min = cy
                    if cx > cx_max:
                        cx_max = cx
                    if cy > cy_max:
                        cy_max = cy

                # if there is some space around the detected face then give some padding to the face box
                padding_x = int((cx_max - cx_min) * padding_ratio)
                padding_y = int((cy_max - cy_min) * padding_ratio)

                # Apply padding to the face box
                cx_min -= padding_x
                cy_min -= padding_y
                cx_max += padding_x
                cy_max += padding_y

                # check if the box is within the frame from the given coordinates
                cx_min = max(0, cx_min)
                cy_min = max(0, cy_min)
                cx_max = min(w, cx_max)
                cy_max = min(h, cy_max)
                

                hand_boxes.append((cx_min, cy_min, cx_max - cx_min, cy_max - cy_min))

        if draw:
            detectionBox(detectedArr=hand_boxes, frame=frame)

        return hand_boxes

    def getLandmarks(self, processedFrame, frame, draw=False):
        """return the detected landmarks from the processed frame, here face

        Parameters
        ----------
        processedFrame : 
            output of processFrame function
        frame : np.array
            frame to draw the landmarks on
        draw : bool, optional
            draw the landmarks on the frame, by default False

        Returns
        -------
        list
            list of landmarks
        """
        if processedFrame.multi_hand_landmarks and draw:
            for hand_landmarks in processedFrame.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        frame,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS)

        return processedFrame.multi_hand_landmarks

if __name__ == "__main__":
    HandDetector()
    pass