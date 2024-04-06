from math import ceil, floor
import os
from pathlib import Path
from tkinter import HORIZONTAL
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
        r = width / (float(w) if w else 1)
        dim = (width, int(h * r))
        
    # return the resized image
    return cv2.resize(image, dim, interpolation=inter)


# either need to ### update this or remove this
# clip image from the given coordinates
def clipImage(image, coordinates):
    """clip the image from the given coordinates

    Parameters
    ----------
    image : image
        image to clip
    coordinates : tuple
        coordinates of the image to clip (x1, y1, x2, y2)

    Returns
    -------
    image
        clipped image
    """
    # unpack the coordinates
    (x,y,w,h) = coordinates
    # clip the image
    return image[ y:y+h, x:x+w]



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
    frame = cv2.copyMakeBorder(frame, 25, 0, 1, 1, cv2.BORDER_CONSTANT, value=(0, 0, 0))
    # showcase the top fps and time taken till yet
    cv2.putText(frame, title, possition, font, font_scale, color, thickness)
    return frame

def combine_images(images, view:str='horizontal',mWidth:int=400, col:int=2):
    """combine the images in the given view

    Parameters
    ----------
    images : array of images or frames
        images to combine
    view : str, optional
        view of combination of image, (vertical or horizaontal), by default 'horizontal'
    mWidth : int, optional
        max width of the window of images, by default 400
    col : int, optional
        number of columns to show row or col respective to view horizontal or vertical, by default 1
    """
    
    if len(images) == 0:
        raise Exception("No images to show, add atleast one image to show the image")

    # first check for no of col to show in a row 
    eachImageWidth = mWidth // (col if col >= 3 else 2)
    
    # then divide the provided space with col and resize images accordingly
    images = [resizeImage(i,eachImageWidth,eachImageWidth) for i in images]
    # add border for the images
    images = [cv2.copyMakeBorder(i, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=(0, 0, 0)) for i in images]
    
    
    # create a window to show the output images
    # heigth, width, _ = images[0].shape
    if view == 'horizontal':
        height = mWidth + (col*2) + 2
        width = (images[0].shape[0] * ceil(len(images) / col)) + (col * 2)
        combined = np.zeros((height, width, 3), dtype=np.uint8)
        
        print(width,height)

        # Loop through each pair of images and combine them horizontally
        row_offset = 0
        for i in range(0, len(images), col):
            col_offset = 0            
            for each in images[i:i+col]:
                # Get the dimensions of the current image
                rows, cols, _ = each.shape
                # print(rows,cols,"col",  col_offset,col_offset+cols)
                # Combine the images horizontally
                combined[row_offset:row_offset+rows, col_offset:col_offset+cols, :] = each
                # Update column offset for the next image
                col_offset += cols
            # Update row offset for the next row
            row_offset += rows

    else:
        height = (images[0].shape[0] * ceil(len(images) / col)) + (col * 2)
        width = mWidth + (col*2) + 2
        combined = np.zeros((height, width, 3),dtype=np.uint8)
        
        # then combine the images
        row_offset = 0
        for index in range(0,len(images),col):
            cols_offset = 0
            for each in images[index:index+col]:
                rows, cols, _ = each.shape
                combined[row_offset:row_offset+rows, cols_offset:cols_offset + cols, :] = each
                cols_offset += cols
            row_offset += rows

        
    return combined


def show_all_frames(dict,keysToShow=['frame','color_converted'],showStats = True, windowName='Showcase Frames'):
    if len(keysToShow) == 0:
        raise Exception("No keys to show, add atleast one key to show the image")
    if len(keysToShow) == 1:
        # show the image
        cv2.imshow(windowName,dict[keysToShow[0]])
        return

    # create a window to show the output images
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
                if i == 'frame':
                    showcase[i] = added_title(dict[i], "Real Image")
                else:
                    showcase[i] = added_title(resizeImage(dict[i],400), i)
            elif type(dict[i]) == type([]):
                if len(dict[i]) > 0 and type(dict[i][0]) == type(np.array([])):
                    # print(f"key {i} is array of length",len(dict[i]))
                    ##### update view according to the space aviailable
                    # calculate the space available in the window after showing the other images
                    # accoring to that show this list of images in HORIZONTAL or VERTICAL
                    showcase[i] = added_title(combine_images(dict[i]), i)
            else:
                print(f"key {i} is not np array or string")
                raise Exception(f"key {i} is not np array or string")


            # colculate the size of the image and resize it if need and then show it
            pass
    else:
        # print(showcase.keys())
        allimagesSize = [i.shape for i in showcase.values()]
        rows_comb = max([i[0] for i in allimagesSize])
        cols_comb = sum([i[1] for i in allimagesSize])
        comb = np.zeros(shape=(rows_comb, cols_comb, 3), dtype=np.uint8)
        
        cols_offset = 0
        # print('without detected',rows_comb,cols_comb)
        for i, image in showcase.items():
            # if i == 'detected': 
            #     print('with detected',rows_comb,cols_comb)
            # Check if the image is grayscale
            if len(image.shape) == 2: 
                image = np.stack((image,) * 3, axis=-1)
            
            rows, cols, _ = image.shape
            comb[:rows, cols_offset:cols_offset + cols, :] = image
            cols_offset += cols
                
    # make all the frames of same size
    # dict['frame'] = added_title(dict['frame'], "Real Image")
    # dict['color_converted'] = added_title(resizeImage(dict['color_converted'],400,400), "Gray Image")
    
    # rows_rgb, cols_rgb, channels = dict['frame'].shape
    # rows_gray, cols_gray = dict['color_converted'].shape[:2]
    
    # # combine grey and color converted image
    # rows_comb = max(rows_rgb, rows_gray)
    # cols_comb = cols_rgb + cols_gray
    # comb = np.zeros(shape=(rows_comb, cols_comb, channels), dtype=np.uint8)

    # comb[:rows_rgb, :cols_rgb] = dict['frame']
    # comb[:rows_gray, cols_rgb:] = dict['color_converted'][:, :, None]


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




# check for keywork 'update' with hashtags in the code to fix from there 