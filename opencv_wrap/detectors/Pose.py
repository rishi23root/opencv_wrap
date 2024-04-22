# flake8: noqa: E501

import mediapipe as mp
from opencv_wrap.utils import DetectorClass
from opencv_wrap.utils.helper import detectionBox

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_pose = mp.solutions.pose


# tested with multiple people in the frame, not working
# 1. use yolo to detect the person in the frame
# 2. crop the person from the frame
# 3. use pose detection on the cropped frame


class PoseDetector(DetectorClass):

    def __init__(
        self,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        verbose=False,
    ):
        if self._detector is None:
            self.pose = mp_pose.Pose(
                min_detection_confidence=min_detection_confidence,
                min_tracking_confidence=min_tracking_confidence,
            )
            self._detector = self.processFrame

    def processFrame(self, frame):
        """process frame and extract the pose features

        Parameters
        ----------
        frame : np.array
            frame to process

        Returns
        -------
        landmarks
            output of pose.process function
        """
        return self.pose.process(frame)

    def getDetectionBox(self, processedFrame, frame, padding_ratio=0.2, draw=False):
        """return the detected box from the processed frame, here pose

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
        # Implementation for detection box extraction for body pose detection
        pose_box = []
        if processedFrame.pose_landmarks:
            h, w, _ = frame.shape
            cx_min = w
            cy_min = h
            cx_max = cy_max = 0
            for lm in processedFrame.pose_landmarks.landmark:
                # get the bounding box of the body
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

            pose_box.append((cx_min, cy_min, cx_max - cx_min, cy_max - cy_min))

        if draw:
            detectionBox(detectedArr=pose_box, frame=frame)

        return pose_box

    def getLandmarks(self, processedFrame, frame, draw=False):
        """return the detected landmarks from the processed frame, here pose

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
        # Implementation for landmark extraction for body pose detection
        mp_drawing.draw_landmarks(
            frame,
            processedFrame.pose_landmarks,
            mp_pose.POSE_CONNECTIONS,
            landmark_drawing_spec=mp_drawing_styles.get_default_pose_landmarks_style(),
        )

        return processedFrame.pose_landmarks


if __name__ == "__main__":
    PoseDetector()
    pass
