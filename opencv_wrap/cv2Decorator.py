import cv2
import time
from functools import wraps
import traceback
from pathlib import Path


class cv2Decorator:
    def TotalTimeTaken(show=False):
        """Decorator to calculate the total time taken in executing \
        of provided function and return the \
        'time_taken' in the return data dict

        Parameters
        ----------
        show : bool, optional
            show will print the time taken in human readable format, 
            by default False
        """

        def inner_wrapper(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                start = time.perf_counter()
                kwargs["startsAt"] = start
                return_data = function(*args, **kwargs)
                time_taken = time.perf_counter() - start
                in_mins = divmod(time_taken, 60)
                formatedTime = (
                    ":".join(
                        map(
                            lambda x: str(int(x)),
                            [in_mins[1], *divmod(in_mins[0], 60)[::-1]][::-1],
                        )
                    )
                ) + " Hours"
                return_data["time_taken"] = time_taken

                if show:
                    print("Time taken --> ", formatedTime)

                return return_data

            return wrapper

        return inner_wrapper

    previousTime = 0  # used in calculating

    def CalculateFps(
        draw: bool = False,
        org=(5, 25),
        font=cv2.FONT_HERSHEY_PLAIN,
        fontScale=2,
        color=(255, 0, 0),
        thickness=2,
    ):
        """Decorator to calculate the fps of frames and return the 'fps'\
            in the return data dict

        Parameters
        ----------
        draw : bool, optional
            draw the fps on the frame, by default False
        org : tuple, optional
            org: Point from where the text should start, by default (5, 25)
        font : int, optional
            font: Font type (int), by default cv2.FONT_HERSHEY_PLAIN
        fontScale : int, optional
            fontScale : Font scale factor that is multiplied by the  \
                font-specific base size, by default 2
        color : tuple, optional
            color : Text color, by default (255, 0, 0)
        thickness : int, optional
            thickness : Thickness of the lines used to draw a text, \
                by default 2
        """

        def inner_wrapper(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                currentTime = time.time()

                # calculate the fps and update it
                try:
                    fps = 1 / (currentTime - __class__.previousTime)
                except ZeroDivisionError:
                    fps = 0
                finally:
                    __class__.previousTime = currentTime
                    kwargs["fps"] = round(fps, 1)

                # print("from fps",kwargs.keys())
                return_kwargs = function(*args, **kwargs)

                if draw and "frame" in return_kwargs:
                    # get the image_size and put the text at right top
                    try:
                        # shape = return_kwargs['frame'].shape
                        cv2.putText(
                            return_kwargs["frame"],
                            f"FPS:{str(int(fps)).rjust(3)}",
                            org=org,
                            fontFace=font,
                            fontScale=fontScale,
                            color=color,
                            thickness=thickness,
                        )
                    except:
                        pass
                    finally:
                        # show the frames
                        return return_kwargs
                else:
                    return return_kwargs

            return wrapper

        return inner_wrapper

    def MirrorFrame(axis=1, inputFrameName="mirror_frame"):
        """flip the frame from its axis and update the 'frame'\
              in the return data dict

        Parameters
        ----------
        axis : int, optional
            (0 - x) or (1 - y), by default 1
        inputFrameName : string, optional
            name of the frame to be updated if not present it will \
                creat a new one, by default 'mirror_frame'
        """

        def inner_wrapper(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                if "frame" in kwargs:
                    kwargs[inputFrameName] = cv2.flip(kwargs["frame"], axis)
                    return function(*args, **kwargs)
                else:
                    raise Exception(
                        "Error in reading the Frame, frame not found, try calling the mirror frame after the frame is present"
                    )

            return wrapper

        return inner_wrapper

    def ConvertCOLOR(converter=cv2.COLOR_RGB2BGR, frameName="greyScale"):
        """Convert COLOR of the frame to the converter provided and return \
            the 'color_converted' or the provided name in the return data dict

        Parameters
        ----------
        converter : int, optional
            cv2.COLOR_RGB2BGR or any other cv2.COLOR_*, 
            by default cv2.COLOR_RGB2BGR
        frameName : string, optional
            name of the frame to be updated if not provided \
                then it will update dict with key 'color_converted',
             by default "greyScale'
        """

        def inner_wrapper(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                if converter:
                    if "frame" in kwargs:
                        kwargs[frameName] = cv2.cvtColor(kwargs["frame"], converter)
                        return function(*args, **kwargs)
                    else:
                        raise Exception(
                            "Error in reading the Frame, frame not found, \
                                try calling the mirror frame after \
                                the frame is present"
                        )
                else:
                    return function(*args, **kwargs)

            return wrapper

        return inner_wrapper

    # access cam and video
    def AccessCamOrVideo(
        show=False,
        idCam=0,
        videoPath: Path = "",
        fps=30,
        wCam=640,
        hCam=480,
        frameTitle: str = "feed from",
        keysToBreak: list = [81, 27],
    ):
        """Decorated funtion to access the cam or video and return the 'frame'\
            in the return data dict


        Parameters
        ----------
        show : bool, optional
            show the frames, by default False
        idCam : int, optional
            Camera id, by default 0
        videoPath : Path, optional
            path to the video, by default ""
        fps : int, optional
            fps of the video, by default 30
        wCam : int, optional
            width of the frame if cam, by default 640
        hCam : int, optional
            height of the frame if cam, by default 480
        frameTitle : str, optional
            initial title of the frame it will update according source \
                provided, by default "feed from"
        keysToBreak : list, optional
            keys to break the frames, by default [81,27]
        """

        def inner_wrapper(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                return_kwargs = kwargs
                steps = 1
                try:
                    # open the webcam capture of the
                    if videoPath:
                        cap = cv2.VideoCapture(videoPath)
                        default_fps = round(cap.get(cv2.CAP_PROP_FPS))
                        if fps < default_fps:
                            steps = round(default_fps / fps)

                        print(
                            "default fps of video is :",
                            default_fps,
                            " moving with steps of :",
                            steps,
                        )

                    else:
                        try:
                            cap = cv2.VideoCapture(idCam)
                            # may cause error in reading
                        except Exception:
                            # can cause significant frame drop
                            print("Using cv2.CAP_DSHOW")
                            cap = cv2.VideoCapture(idCam, cv2.CAP_DSHOW)

                        cap.set(3, wCam)
                        cap.set(4, hCam)

                    try:
                        while cap.isOpened():
                            count = int(cap.get(1))
                            kwargs["frame_count"] = count
                            # read image
                            success, frame = cap.read()

                            if (
                                videoPath
                                and count % steps != 0
                                and success
                                and frame is not None
                            ):
                                continue

                            if success and frame is not None:
                                # call the function
                                if function:
                                    kwargs["frame"] = frame
                                    # print("readcam before: ",kwargs.keys())
                                    return_kwargs = function(*args, **kwargs)

                                # show the frames
                                if show:
                                    Title = frameTitle + (
                                        " video" if videoPath else " Cam"
                                    )
                                    cv2.imshow(Title, return_kwargs["frame"])
                                key = cv2.waitKey(1)
                                if key in keysToBreak:
                                    cv2.destroyAllWindows()
                                    break
                            else:
                                if not success and not videoPath:
                                    raise Exception("Error in reading the Frame")
                                else:
                                    break

                    # expect for keyboard interrupt
                    except KeyboardInterrupt:
                        print("Keyboard Interrupt, closing cam")
                        return return_kwargs
                except Exception:
                    print("[error]", traceback.format_exc())
                    # print(getattr(e, 'message', repr(e)))
                    # print(getattr(e, 'message', str(e)))
                finally:
                    cv2.destroyAllWindows()
                    cap.release()

                return return_kwargs

            return wrapper

        return inner_wrapper

    # detect in each frame
    def DetectInEachFrame(
        detector=None,
        name="detector",
    ):
        """
        detect in each frame and return the 'detector' in the return data dict

        Parameters
        ----------
        detector : _type_, optional
            detector to detect in each frame, by default None
        name : str, optional
            name of the detector, this paramerter will be usefull when defining multiple detectors, by default "detecter"
        """

        def inner_wrapper(function):
            @wraps(function)
            def wrapper(*args, **kwargs):
                # run the funtion
                if detector:
                    kwargs[name] = detector

                return function(*args, **kwargs)

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

    @cv2Decorator.TotalTimeTaken(show=True)
    @cv2Decorator.DetectInEachFrame(
        detector=cv2.CascadeClassifier(
            cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
        )
    )
    @cv2Decorator.AccessCamOrVideo(show=True)
    @cv2Decorator.CalculateFps(draw=True)
    @cv2Decorator.MirrorFrame()
    @cv2Decorator.ConvertCOLOR(converter=cv2.COLOR_BGR2GRAY)
    def all_actions(**kwargs):
        frame = kwargs["frame"]
        # mirrored = kwargs['mirror_frame']

        # detect face from trainerd data and detectMultiScale use to deteat every size of face
        face_coordinate = kwargs["detector"].detectMultiScale(
            kwargs["color_converted"], 1.3, 5
        )

        for i in face_coordinate:
            (x, y, w, h) = i
            # drawing rectangle on the image
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        return kwargs
