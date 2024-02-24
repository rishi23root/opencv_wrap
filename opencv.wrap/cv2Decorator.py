# cv2Decorator.py
import cv2
import time
from time import sleep as nap
from functools import wraps
import traceback
from pathlib import Path

class cv2Decorator:
    def TotalTimeTaken(show = False):
        """Calculate the total time taken in executing a function"""
        def inner_wrapper(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                try :
                    start = time.perf_counter()
                    # print(kwargs.keys())
                    kwargs['time_taken'] = start
                    return_data = function(*args, **kwargs)
                    # print(return_data)
                    if show:
                        time_taken = time.perf_counter() - start
                        in_mins = divmod(time_taken,60)
                        nap(1)
                        print("Time taken --> ",
                            ":".join(
                                    map(
                                        lambda x : str(int(x)),
                                        [in_mins[1],*divmod(in_mins[0],60)[::-1]][::-1]
                                    ))
                            ,"Hours")
                    return return_data
                except Exception as e:
                    print(e)
            return wrapper
        return inner_wrapper

    previousTime = 0 # used in calculating   
    def CalculateFps(draw=False,
            org = (5, 25), 
            font = cv2.FONT_HERSHEY_PLAIN,
            fontScale = 2, 
            color = (255, 0, 0),
            thickness = 2):
        """Draw the fps of the frame on the image corner"""
        def inner_wrapper(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                currentTime = time.time()

                # calculate the fps and update it
                try:
                    fps = 1 / (currentTime - __class__.previousTime)
                except ZeroDivisionError:
                    fps = 0
                finally :
                    __class__.previousTime = currentTime
                    kwargs['fps'] = round(fps, 1)

                # print("from fps",kwargs.keys())
                return_kwargs = function(*args, **kwargs)

                if draw and 'frame' in return_kwargs:    
                    # get the image_size and put the text at right top
                    try :
                        # shape = return_kwargs['frame'].shape
                        cv2.putText(
                            return_kwargs['frame'],
                            f'FPS:{str(int(fps)).rjust(3)}', 
                            org =org , 
                            fontFace =font,
                            fontScale = fontScale , 
                            color =color,
                            thickness =thickness )
                    except :
                        pass
                    finally :
                        # show the frames
                        return return_kwargs
                else :
                    return return_kwargs

            return wrapper
        return inner_wrapper

    def MirrorFrame(axis = 1):
        """flip the frame from its y axis take axis as args"""
        """0 means flipping around the x-axis 
        positive value (for example, 1) means flipping around y-axis. (mirror)
        Negative value (for example, -1) means flipping around both axes."""
        def inner_wrapper(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                if 'frame' in kwargs:
                    kwargs['mirror_frame'] = cv2.flip(kwargs['frame'], axis)
                    return function(*args,**kwargs)
                else :
                    raise Exception("Error in reading the Frame, frame not found, try calling the mirror frame after the frame is present")
            return wrapper
        return inner_wrapper
    
    def ConvertCOLOR(converter = cv2.COLOR_RGB2BGR):
        """Convert COLOR of the frame to the converter provided"""
        def inner_wrapper(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                if converter :
                    if 'frame' in kwargs:
                        kwargs['color_converted'] = cv2.cvtColor(kwargs['frame'], converter)
                        return function(*args,**kwargs)
                    else :
                        raise Exception("Error in reading the Frame, frame not found, try calling the mirror frame after the frame is present")
                else :
                    return function(*args,**kwargs)
            return wrapper
        return inner_wrapper


    # simple form
    def ReadCamAndShowFrames(
            idCam = 0,
            wCam = 640, 
            hCam = 480 ,
            frameTitle:str = "Cam feed",
            keysToBreak : list = [81,27]):
        """Decorated funtion will can pass a args['frame'] in defining the function """
        """It makes the use webcam in cv2 easier (super simple form)
        idCam        cam id (default = 0),
        wCam         cam frame width (default = 640), if set to None it will not be update from cam
        hCam         cam frame height (default = 480),  if set to None it will not be update from cam
        frameTitle   show title on the frames 
        keysToBreak  keys to break frames (default = 81,27)
        """
        def inner_wrapper(function):
            @wraps(function)
            def wrapper(*args, **kwargs):       
                try:
                    # open the webcam capture of the 
                    try :
                        cap = cv2.VideoCapture(idCam)
                        # may cause error in reading
                    except :
                        # can cause significant frame drop
                        print("Using cv2.CAP_DSHOW")
                        cap = cv2.VideoCapture(idCam,cv2.CAP_DSHOW)
                        
                    cap.set(3, wCam)
                    cap.set(4, hCam)
                    while True:
                        # read image
                        success, frame = cap.read()
                        if success :
                            # call the function
                            if function :
                                frame = function(frame=frame)

                            # show the frames
                            cv2.imshow(frameTitle, frame)
                            key = cv2.waitKey(1)
                            if key in keysToBreak:
                                cv2.destroyAllWindows()
                                break
                        else:
                            raise Exception("Error in reading the Frame")

                except Exception as e :
                    print(traceback.format_exc())
                    # print(getattr(e, 'message', repr(e)))
                    # print(getattr(e, 'message', str(e)))
                finally:
                    cap.release()
                    cv2.destroyAllWindows()
            return wrapper
        return inner_wrapper

    # with specific detector  # updated 
    def ReadCamAddDetectShowFrames(
                    detector = (None,),
                    idCam = 0,
                    wCam = 640, 
                    hCam = 480 ,
                    frameTitle:str = "Cam feed",
                    keysToBreak : list = [81,27]):
        """Decorated funtion will can pass a args['frame','detector'] in defining the function """
        """It will call the detector class if any with its args if any and initiate the call the return the called function
        detector     detector to use in detection (default = (None,)),
        idCam        cam id (default = 0),
        wCam         cam frame width (default = 640), if set to None it will not be update from cam
        hCam         cam frame height (default = 480),  if set to None it will not be update from cam
        frameTitle   show title on the frames 
        keysToBreak  keys to break frames (default = 81,27)
        """
        def inner_wrapper(function):
            @wraps(function)
            def wrapper(*args, **kwargs):       
                try:
                    # open the webcam capture of the 
                    try :
                        cap = cv2.VideoCapture(idCam)
                        # may cause error in reading
                    except :
                        # can cause significant frame drop
                        print("Using cv2.CAP_DSHOW")
                        cap = cv2.VideoCapture(idCam,cv2.CAP_DSHOW)
                    
                    # use of the detector funtion, whaterver class is provied here if any
                    if detector[0]:
                        detectorFuntion = detector[0](*detector[1:]) # to detect and use different function in the hand detector class
                    else :
                        detectorFuntion = None
                    cap.set(3, wCam)
                    cap.set(4, hCam)
                    while True:
                        # read image
                        success, frame = cap.read()
                        if success :
                            # call the function
                            if function :
                                kwargs['frame'] = frame
                                kwargs['detector'] = detectorFuntion
                                # print("readcam before: ",kwargs.keys())
                                return_kwargs = function(*args, **kwargs)
                            else:
                                return_kwargs = kwargs

                            # show the frames
                            cv2.imshow(frameTitle, frame)
                            key = cv2.waitKey(1)
                            if key in keysToBreak:
                                cv2.destroyAllWindows()
                                return return_kwargs
                        else:
                            raise Exception("Error in reading the Frame")

                except Exception as e :
                    print(traceback.format_exc())
                    # print(getattr(e, 'message', repr(e)))
                    # print(getattr(e, 'message', str(e)))
                finally:
                    cap.release()
                    cv2.destroyAllWindows()
            return wrapper
        return inner_wrapper

    # with specific detector 
    def ReadCamAddDetectShowFrames_video(
                    videoPath: Path = "", 
                    detector = (None,),
                    idCam = 0,
                    frameTitle:str = "Cam feed",
                    keysToBreak : list = [81,27]):
        """Decorated funtion will can pass a args['frame','detector'] in defining the function """
        """It will call the detector class if any with its args if any and initiate the call the return the called function
        videoPath    path to the video
        detector     detector to use in detection (default = (None,)),
        idCam        cam id (default = 0),
        frameTitle   show title on the frames 
        keysToBreak  keys to break frames (default = 81,27)
        """
        def inner_wrapper(function):
            @wraps(function)
            def wrapper(*args, **kwargs):       
                try:
                    # open the webcam capture of the 
                    try :
                        cap = cv2.VideoCapture(videoPath)
                        # may cause error in reading
                    except :
                        # can cause significant frame drop
                        print("Using cv2.CAP_DSHOW")
                        cap = cv2.VideoCapture(videoPath,cv2.CAP_DSHOW)
                    
                    # use of the detector funtion, whaterver class is provied here if any
                    if detector[0]:
                        detectorFuntion = detector[0](*detector[1:]) # to detect and use different function in the hand detector class
                    else :
                        detectorFuntion = None
                    while cap.isOpened():
                        # read image
                        success, frame = cap.read()
                        if success :
                            # call the function
                            if function :
                                frame = function(frame=frame,detector=detectorFuntion)

                            # show the frames
                            cv2.imshow(frameTitle, frame)
                            key = cv2.waitKey(1)
                            if key in keysToBreak:
                                cv2.destroyAllWindows()
                                break
                        else:
                            break

                except Exception as e :
                    print(traceback.format_exc())
                    # print(getattr(e, 'message', repr(e)))
                    # print(getattr(e, 'message', str(e)))
                finally:
                    cap.release()
                    cv2.destroyAllWindows()
            return wrapper
        return inner_wrapper


    # default decorator for more (template)
    # def default_decorator(args1 = 1):
    #     def inner_wrapper(function):
    #         @wraps(function)
    #         def wrapper(*args, **kwargs):
    #             # run the funtion
    #             # return function(*args,**kwargs)
    #         return wrapper
    #     return inner_wrapper

# # call only one funtion to run all the basics things
if __name__ == "__main__":
    # example 1
    # a = 0
    # @cv2Decorator.TotalTimeTaken(show = True)
    # @cv2Decorator.ReadCamAndShowFrames()
    # @cv2Decorator.CalculateFps(draw = True)
    # @cv2Decorator.MirrorFrame()
    # def all_actions(frame):
    #     # update to get all different types of action on the frames 
    #     a += 1
    #     return frame

    # all_actions()

    # example 2 # face detectection
    @cv2Decorator.TotalTimeTaken(show=True)
    @cv2Decorator.ReadCamAddDetectShowFrames(detector=(cv2.CascadeClassifier,cv2.data.haarcascades+"haarcascade_frontalface_default.xml"))
    @cv2Decorator.CalculateFps(draw = True)
    @cv2Decorator.MirrorFrame()
    def all_actions(frame,detector):
        gray_img = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)

        # detect face from trainerd data and detectMultiScale use to deteat every size of face
        face_coordinate = detector.detectMultiScale(gray_img,1.3,5)
        # extracting cordinates (x,y,width,height)
        # (x,y,w,h) = face_coordinate[0]    
        for i in face_coordinate:
            (x,y,w,h) = i
            # drawing rectangle on the image 
            cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

        return frame

    all_actions()
