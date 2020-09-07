import cv2
import sys
# run python face.py {image name} to get results

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

if __name__ == '__main__':
    face_finder(sys.argv[1])