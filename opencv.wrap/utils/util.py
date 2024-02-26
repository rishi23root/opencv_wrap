import os
import cv2

def extract_image(video:str,fps:int,direction):
    # 1. get videos frames 
    if not os.path.exists(direction) : os.mkdir(direction)
    vidcap = cv2.VideoCapture('a.mp4')
    default_fps = round(vidcap.get(cv2.CAP_PROP_FPS))
    print("default fps of video is --> ",default_fps)
    if fps < default_fps : steps = round(default_fps/fps)
    else : steps = 1
    print("new fps of video is --> ",int(default_fps/steps))
    folder_path = os.path.join(direction,'image%s.jpg')
    success = True
    while success:
        count = int(vidcap.get(1))
        success,frame = vidcap.read()
        if count%steps == 0 :
            try : cv2.imwrite(folder_path.replace("%s",str(count)),frame) # save file
            except : pass # last frame is none


def face_finder(img):
    # load pre trained data
    trained_data =cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")

    # using imread read image inn cv2
    img = cv2.imread(img)

    # convert into grayscale take 2 args image and color
    # gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # detect face from trainerd data and detectMultiScale use to deteat every size of face
    # face_coordinate = trained_data.detectMultiScale(cv2.cvtColor(gray_img))
    face_coordinate = trained_data.detectMultiScale(cv2.cvtColor(img,cv2.COLOR_BGR2GRAY))

    # extracting cordinates (x,y,width,height)
    # (x,y,w,h) = face_coordinate[0]
    print('there are min people present :',len(face_coordinate))
    for i in face_coordinate:
        (x,y,w,h) = i
        # drawing rectangle on the image 
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

    # show image in cv2 take 2 arrg =window name , image
    cv2.imshow('image representation',img)
    # wait to close the window to move further program
    cv2.waitKey()



# function to make object detection

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