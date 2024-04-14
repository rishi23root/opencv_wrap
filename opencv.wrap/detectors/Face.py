# flake8: noqa: E501
import cv2
from utils.base import Detector
from utils.util import detectionBox

import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh


# functionalities
# 1/ get face detection
# 2/ get face landmarks ractangle
# 3/ get face landmarks points
# 4/ save faces and save them them in a folder
# 5/ compare faces from folder and current face


class Face(Detector):

    def __init__(
        self,
        max_num_faces=5,
        refine_landmarks=True,
        min_detection_confidence=0.4,
        min_tracking_confidence=0.5,
        verbose=False,
    ):
        if self._detector is None:
            self.face_mesh = mp_face_mesh.FaceMesh(
                max_num_faces=max_num_faces,
                refine_landmarks=refine_landmarks,
                min_detection_confidence=min_detection_confidence,
                min_tracking_confidence=min_tracking_confidence,
            )
            # detectorModule = cv2.CascadeClassifier(
            #     cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            # )
            # laod the detector here
            # self._detector = lambda x: detectorModule.detectMultiScale(x, 1.3, 5)
            # self._detector = self.faceDetectionModule
            self._detector = self.processFrame
        # print(self._detector)

    def processFrame(self, frame):
        """process frame and extract the face features

        Parameters
        ----------
        frame : np.array
            frame to process

        Returns
        -------
        landmarks
            output of face_mesh.process function
        """
        return self.face_mesh.process(frame)
        # print(processedFrame.multi_face_landmarks)

    def getDetectionBox(self, processedFrame, frame, padding_ratio=0.2, draw=False):
        """return the detected box from the processed frame, here face

        Parameters
        ----------
        processedFrame : landmarks
            landmarks from the processed frame
        frame : nd.array
            frame to down on
        padding_ratio : float, optional
            padding to the face detected, by default 0.2
        draw : bool, optional
            draw the face box on the frame, by default False

        Returns
        -------
        list
            return list of face box cordiantes (x,y,w,h)
        """
        # get the face box
        face_boxes = []
        # Adjust this value to control the amount of padding (e.g., 0.1 for 10% padding)

        if processedFrame.multi_face_landmarks:
            for face_landmarks in processedFrame.multi_face_landmarks:
                h, w, _ = frame.shape
                cx_min = w
                cy_min = h
                cx_max = cy_max = 0
                for lm in face_landmarks.landmark:
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

                face_boxes.append((cx_min, cy_min, cx_max - cx_min, cy_max - cy_min))

        if draw:
            detectionBox(detectedArr=face_boxes, frame=frame)

        return face_boxes

    def drawLandmarks(self, processedFrame, frame):
        """draw the landmarks on the frame

        Parameters
        ----------
        processedFrame : landmarks
            processed frame to get the landmarks from
        frame : np.array
            frame to draw on
        """
        if processedFrame.multi_face_landmarks:
            for face_landmarks in processedFrame.multi_face_landmarks:
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_TESSELATION,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style(),
                )
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style(),
                )
                mp_drawing.draw_landmarks(
                    image=frame,
                    landmark_list=face_landmarks,
                    connections=mp_face_mesh.FACEMESH_IRISES,
                    landmark_drawing_spec=None,
                    connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style(),
                )


if __name__ == "__main__":
    d1 = Face(verbose=True)
    d2 = Face()

    image = cv2.imread("./test/test.jpg")
    print(d1.detect(image))
    print("isinstance of face :", isinstance(d1, Face), end=" ")
    print("is i1 == i2 :", d1 == d2)
