import os
from pathlib import Path
import cv2
import numpy as np
import time

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

# resize the image 
def resizeImage(image, width=None, height=None, inter=cv2.INTER_AREA):
    """resize the image to the given width and height

    Parameters
    ----------
    image : image
        image to resize
    width : int
        width of the image
    height : int
        height of the image
    inter : cv2.INTER_AREA
        interpolation method

    Returns
    -------
    image
        resized image
    """
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))

    # return the resized image
    return cv2.resize(image, dim, interpolation=inter)

# clip image from the given coordinates
def clipImage(image, coordinates):
    """clip the image from the given coordinates

    Parameters
    ----------
    image : image
        image to clip
    coordinates : tuple
        coordinates of the image to clip

    Returns
    -------
    image
        clipped image
    """
    # unpack the coordinates
    x1, y1, x2, y2 = coordinates

    # clip the image
    return image[y1:y2, x1:x2]



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


def added_title(frame, title:str, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=.7, color=(255,255,255), thickness=1):
    """take the frame and add the title to the top of the image

    Parameters
    ----------
    frame : image 
    title : str
        title to add to the image
    font : cv2 fonts, optional
        font to use in the title, by default cv2.FONT_HERSHEY_SIMPLEX
    font_scale : float, optional
        font scale, by default .7
    color : tuple, optional
        color of the font, by default (255,255,255)
    thickness : int, optional
        thickness of the font, by default 1

    Returns
    -------
    frame
        frame with title added to the top
    """
    # set the position of the text in the middle of the image width
    frame_width = frame.shape[1]
    text_width = cv2.getTextSize(title, font, font_scale, thickness)[0][0]
    possition = (int((frame_width - text_width) / 2), 15)

    # add a strip of 30 pixels at the top of the image
    frame = cv2.copyMakeBorder(frame, 25, 0, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    # showcase the top fps and time taken till yet
    cv2.putText(frame, title, possition, font, font_scale, color, thickness)
    return frame

def combine_images(images, view='horizontal'):
    """combine the images in the given view

    Parameters
    ----------
    images : array of images or frames
        images to combine
    view : str, optional
        view of combination of image, (vertical or horizaontal), by default 'horizontal'
    """
    
    if view == 'horizontal':
        # get the height of the first image
        height = images[0].shape[0]
        # get the width of all the images
        width = sum([i.shape[1] for i in images])

        # create a blank image of the size of the combined images
        combined = np.zeros((height, width, 3), dtype=np.uint8)

        # add the images to the combined image
        for i, image in enumerate(images):
            combined[:, i * image.shape[1]:(i + 1) * image.shape[1]] = image
    else:
        # get the width of the first image
        width = images[0].shape[1]
        # get the height of all the images
        height = sum([i.shape[0] for i in images])

        # create a blank image of the size of the combined images
        combined = np.zeros((height, width, 3), dtype=np.uint8)

        # add the images to the combined image
        for i, image in enumerate(images):
            combined[i * image.shape[0]:(i + 1) * image.shape[0], :] = image
    
    return combined


def show_all_frames(dict,keysToShow=['frame','color_converted'],showStats = True, windowName='Showcase Frames'):
    if len(keysToShow) == 0:
        raise Exception("No keys to show, add atleast one key to show the image")
    if len(keysToShow) == 1:
        # show the image
        cv2.imshow(window_name,dict[keysToShow[0]])
        return

    # create a window to show the output images
    width = 0
    height = 0
    showcase = {}
        
    # 1/ first create a combined image of all 
    for i in keysToShow:
        if i not in dict.keys():
            print(f"key {i} not found in the dictionary")
            raise Exception(f"key {i} not found in the dictionary")
        else:
            # check what type of data does these keys have
            if type(dict[i]) == type(None): raise Exception(f"key {i} is None")
            elif type(dict[i]) == type(np.array([])):
                # np array means an individual image || print(f"key {i} is np array",len(dict[i]))
                showcase[i] = dict[i]
            elif type(dict[i]) == type([]):
                print(f"key {i} is np array",len(dict[i]))
                pass
            else:
                print(f"key {i} is not np array or string")
                raise Exception(f"key {i} is not np array or string")


            # colculate the size of the image and resize it if need and then show it
            pass
    else:
        # print("all keys found")
        pass
    
    # make all the frames of same size
    dict['frame'] = added_title(dict['frame'], "Real Image")
    dict['color_converted'] = added_title(resizeImage(dict['color_converted'],400,400), "Gray Image")
    
    rows_rgb, cols_rgb, channels = dict['frame'].shape
    rows_gray, cols_gray = dict['color_converted'].shape[:2]
    
    # combine grey and color converted image
    rows_comb = max(rows_rgb, rows_gray)
    cols_comb = cols_rgb + cols_gray
    comb = np.zeros(shape=(rows_comb, cols_comb, channels), dtype=np.uint8)

    comb[:rows_rgb, :cols_rgb] = dict['frame']
    comb[:rows_gray, cols_rgb:] = dict['color_converted'][:, :, None]


    if showStats:
        # add a strip of 30 pixels at the top of the image
        comb = cv2.copyMakeBorder(comb, 40, 0, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        # showcase the top fps and time taken till yet
        cv2.putText(comb, f"FPS: {dict['fps']}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
        time_taken = time.perf_counter() - dict['startsAt']
        in_mins = divmod(time_taken,60)
        formatedTime = "Time: " + (":".join(
            map(
                lambda x : str(int(x)),
                [in_mins[1],*divmod(in_mins[0],60)[::-1]][::-1]
            )))
        
        text_width = cv2.getTextSize(formatedTime, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0][0]
        # put the time to right end of the image
        possition = (comb.shape[1] - text_width, 30)        
        cv2.putText(comb, formatedTime, possition, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # show the output image 
    cv2.imshow(windowName, comb)
    
    
# showcase top fps and time taken till yet 
# then show the images 