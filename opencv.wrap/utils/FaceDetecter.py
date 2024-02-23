from typing import overload
import cv2


class Face:
    padding = 10
    image_size = 200
    def __init__(self):
        self.trained_model =cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        self.ksize = (20,20)

    def detectFace(self,frame,draw = False):
        gray_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        self.face_coordinate = self.trained_model.detectMultiScale(gray_img,1.3,5)
        # extracting cordinates (x,y,width,height)
        # (x,y,w,h) = face_coordinate[0]    
        for i in self.face_coordinate:
            (x,y,w,h) = i
            # drawing rectangle on the image 
            if draw :
                cv2.rectangle(frame,(x-self.padding,y-self.padding),(x+w+self.padding,y+h+self.padding),(0,255,0),2)
            # crop 
            roiFrame = frame[y-self.padding:self.padding+h+y,
                             x-self.padding:self.padding+w+x] 
            # put back on 
            frame[y-self.padding:self.padding+h+y,
                  x-self.padding:self.padding+w+x] = self.actionOnImage(roiFrame,action='blur')
        return frame
    
    def actionOnImage(self,roiFrame,action='blur'):
        """make the roiImage - blur or dark"""
        try :
            if action == 'blur':
                # blur the part of the image
                roiFrame =  cv2.blur(roiFrame, self.ksize, cv2.BORDER_DEFAULT) 
            else :
                # make it black
                roiFrame[:,:] = (0,0,0)
        except :
            pass
        finally:
            return roiFrame
    
    def detectFaceAndShow(self,frame,draw = False):
        fh,fw,fc = frame.shape
        gray_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        self.face_coordinate = self.trained_model.detectMultiScale(gray_img,1.3,5)
        for index in range(len(self.face_coordinate)) :
            (x,y,w,h) = self.face_coordinate[index]    
            # drawing rectangle on the image 
            if draw :
                cv2.rectangle(frame,(x-self.padding,y-self.padding),(x+w+self.padding,y+h+self.padding),(0,255,0),2)
            # crop 
            self.padding = 60
            roiFrame = frame[y-self.padding:self.padding+h+y,
                            x-self.padding:self.padding+w+x] 
            # # put back on 

            try :
                frame[fh-self.image_size: fh,
                      fw-self.image_size: fw] = cv2.resize(roiFrame,(self.image_size,self.image_size))
            except :
                pass
        
        return frame     
   
    def detectFaceAndCenter(self,frame,draw = False,padding = 100 ):
        fh,fw,fc = frame.shape
        gray_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
        self.face_coordinate = self.trained_model.detectMultiScale(gray_img,1.3,5)
        if len(self.face_coordinate) >= 1 :
            (x,y,w,h) = self.face_coordinate[0]    
            # drawing rectangle on the image 
            if draw :
                cv2.rectangle(frame,(x-self.padding,y-self.padding),(x+w+self.padding,y+h+self.padding),(0,255,0),2)
            # crop 
            roiFrame = frame[y-padding:padding+h+y,
                            x-padding:padding+w+x] 
            # # put back on 
            try :
                frame[:,:] = cv2.resize(roiFrame,(fw,fh))
            except :
                pass
        return frame     
