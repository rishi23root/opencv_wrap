import os
from pathlib import Path
import cv2

def saveFrame(frame:str,count:int,destination: Path):
    """save frame to destination folder with count as name of the file

    Parameters
    ----------
    frame : str
        frame to save
    count : int
        count of the frame
    destination : Path
        destination folder to save the frame into
    """
    # 1. get videos frames 
    if not os.path.exists(destination) : os.mkdir(destination)
    folder_path = os.path.join(destination,'image%s.jpg')
    try : cv2.imwrite(folder_path.replace("%s",str(count)),frame) # save file
    except : pass # last frame is none

# create box for the object detection
def detectionBox(detectedArr, frame, border_color=(0,255,0),border_thickness=2):
    for i in detectedArr:
        (x,y,w,h) = i
        # drawing rectangle on the image 
        cv2.rectangle(frame,(x,y),(x+w,y+h),border_color,border_thickness)


# function to showcase the all the processed frames
# user will provide different types of frames like real with fps , mirror , gray , face detection
# join them and show them in a single window side by side
# it will also took screen size into consideratioin when showing images if images are more then spaces aviailable then it will show one more window or make image smaller
# window
# section name 
# frame + frame + frame + frame
# frame + frame + frame + frame
# section name
# frame + frame + frame + frame
# frame + frame + frame + frame


# def show_all_frames():
#     pass