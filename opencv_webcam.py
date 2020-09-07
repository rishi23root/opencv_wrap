import cv2
    
def main(camera_number):
    # load pre trained data
    trained_data =cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    # using-webcam
    webcam = cv2.VideoCapture(camera_number)
    print('press esc for exit')

    while True:
        # extracting-live-data-from-web-cam
        boolen,img = webcam.read()
        # convert into grayscale take 2 args image and color
        gray_img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        # detect face from trainerd data and detectMultiScale use to deteat every size of face
        face_coordinate = trained_data.detectMultiScale(gray_img,1.3,5)
        # extracting cordinates (x,y,width,height)
        # (x,y,w,h) = face_coordinate[0]    
        for i in face_coordinate:
            (x,y,w,h) = i
            # drawing rectangle on the image 
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)

        # show image in cv2 take 2 arrg =window name , image
        cv2.imshow('image representation',img)
        # wait to close the window to move further program
        key = cv2.waitKey(1)
        if key == 81 or key == 27 :
            cv2.destroyAllWindows()
            break
            



if __name__ == '__main__':
    main(0)