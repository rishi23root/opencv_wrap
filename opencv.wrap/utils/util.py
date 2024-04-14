# flake8: noqa: E501
import os
from pathlib import Path
import cv2
import numpy as np
import time


def saveFrame(frame: str, count: int, destination: Path):
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
    if not os.path.exists(destination):
        os.mkdir(destination)
    folder_path = os.path.join(destination, "image%s.jpg")
    try:
        cv2.imwrite(folder_path.replace("%s", str(count)), frame)  # save file
    except:
        pass  # last frame is none


# create box for the object detection
def detectionBox(detectedArr, frame, border_color=(0, 255, 0), border_thickness=2):
    """create a border box for the given frame and detected array (x,y,w,h)

    Parameters
    ----------
    detectedArr : array of tuples (x,y,w,h)
        array of all the detected objects
    frame : image or frame
        frame to draw the border box on
    border_color : rbg, optional
        color of the boder to draw boder with, by default (0, 255, 0)
    border_thickness : int, optional
        thickness of the border to draw, by default 2
    """ """"""
    for i in detectedArr:
        (x, y, w, h) = i
        # drawing rectangle on the image
        cv2.rectangle(frame, (x, y), (x + w, y + h), border_color, border_thickness)


# resize the image
def resizeImage(
    image, width=None, height=None, inter=cv2.INTER_AREA, keep_aspect_ratio=False
):
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
    keep_aspect_ratio : bool, optional
        keep the aspect ratio of the image, by default False

    Returns
    -------
    image
        resized image
    """
    # grab the image size
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    if width is None or w == 0 or h == 0:
        # original image
        return image
    elif width is not None and height is None:
        if keep_aspect_ratio:
            # error here
            r = width / float(w)
            dim = (width, int(h * r))
            return cv2.resize(image, dim, interpolation=inter)
        else:
            return cv2.resize(image, (width, width), interpolation=inter)
    else:
        return cv2.resize(image, (width, height), interpolation=inter)

    # calculate the ratio of the height and construct the
    # dimensions
    #     r = height / float(h)
    #     dim = (int(w * r), height)

    # # otherwise, the height is None
    # else:
    #     # calculate the ratio of the width and construct the
    #     # dimensions
    #     r = width / (float(w) if w else 1)
    #     dim = (width, int(h * r))
    # return cv2.resize(image, dim, interpolation=inter)


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
    (x, y, w, h) = coordinates
    # clip the image
    return image[y : y + h, x : x + w]


def added_title(
    frame,
    title: str,
    font=cv2.FONT_HERSHEY_SIMPLEX,
    font_scale=0.7,
    color=(255, 255, 255),
    bcolor=(0, 0, 0),
    thickness=1,
):
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
    frame = cv2.copyMakeBorder(frame, 25, 0, 1, 1, cv2.BORDER_CONSTANT, value=bcolor)
    # showcase the top fps and time taken till yet
    cv2.putText(frame, title, possition, font, font_scale, color, thickness)
    return frame


def combine_images(images, mWidth: int = 400, col: int = 2, compress=True):
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
    compress : bool, optional
        compress the image to fit the space avilable, turns into square, by default True
    """

    # resize all images to the same size
    if len(images) == 0:
        raise Exception("No images to show, add atleast one image to show the image")

    # first check for no of col to show in a row
    eachImageWidth = (mWidth // col) - 2
    if compress:
        images = (
            resizeImage(i, eachImageWidth)
            # resizeImage(i, eachImageWidth, keep_aspect_ratio=False)
            for i in images
        )

        # REMOVE false positive, filter out the images which are None or width or height not equal to eachImageWidth
        images = [
            i
            for i in images
            if i is not None
            and (i.shape[0] == eachImageWidth and i.shape[1] == eachImageWidth)
        ]

    # add border for the images
    images = [
        cv2.copyMakeBorder(i, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=(0, 0, 0))
        for i in images
    ]
    eachImageWidth += 2

    if col == 1:
        return np.vstack(images)
    else:
        # get how many elements are require to comple the grid showcase
        blankImagesToAdd = col - (len(images) % col)
        if blankImagesToAdd < col:
            # add blank images to the images array
            images.extend(
                [
                    np.zeros(
                        shape=(eachImageWidth, eachImageWidth, 3),
                        dtype=np.uint8,
                    )
                ]
                * blankImagesToAdd
            )

        return np.vstack(
            [np.hstack(images[i : i + col]) for i in range(0, len(images), col)]
        )


canvasW = 0
canvasH = 0


def show_all_frames(
    dict,
    keysToShow=["frame", "color_converted"],
    showStats=True,
    windowName="Showcase Frames",
):
    """show all the frames in the dictionary in a single window

    Parameters
    ----------
    dict : dict
        dict of images or frames to show
    keysToShow : list, optional
        keys for only framers to show, by default ["frame", "color_converted"]
    showStats : bool, optional
        stats like fps and time spend, by default True
    windowName : str, optional
        window name which show all frame, by default "Showcase Frames"
    """
    global canvasH, canvasW

    if len(keysToShow) == 0:
        raise Exception("No keys to show, add atleast one key to show the image")
    if len(keysToShow) == 1:
        # show the image
        cv2.imshow(windowName, dict[keysToShow[0]])
        return

    # create a window to show the output images
    showcase = {}
    expectedWidth = 0

    # 1/ first create a combined image of all
    for i in keysToShow:
        if i not in dict.keys():
            print(f"key {i} not found in the dictionary")
            raise Exception(f"key {i} not found in the dictionary")
        else:
            # check what type of data does these keys have
            if type(dict[i]) == type(None):
                raise Exception(f"key {i} is None")
            elif type(dict[i]) == type(np.array([])):
                if len(dict[i].shape) == 2:
                    dict[i] = np.stack((dict[i],) * 3, axis=-1)

                # np array means an individual image || print(f"key {i} is np array",len(dict[i]))
                if i == "frame":
                    showcase[i] = added_title(dict[i], "Real Image")
                    expectedWidth += showcase[i].shape[0]
                else:
                    if showcase.get("conversions") == None:
                        showcase["conversions"] = {}
                        showcase["conversions"][i] = added_title(
                            resizeImage(dict[i], 400, keep_aspect_ratio=True), i
                        )
                        expectedWidth += showcase["conversions"][i].shape[0]
                    else:
                        showcase["conversions"][i] = added_title(
                            resizeImage(dict[i], 400, keep_aspect_ratio=True), i
                        )
                # add width to expected width and pass it to add frames horizontal or vertical of combination
            elif type(dict[i]) == type([]):
                if len(dict[i]) > 0 and type(dict[i][0]) == type(np.array([])):
                    # print(f"key {i} is array of length",len(dict[i]))
                    # calculate the space available in the window after showing the other images
                    # accoring to that show this list of images in HORIZONTAL or VERTICAL
                    if expectedWidth > 400:
                        showcase[i] = added_title(
                            combine_images(dict[i], mWidth=expectedWidth),
                            i,
                            bcolor=(0, 0, 0),
                        )
                    else:
                        showcase[i] = added_title(
                            combine_images(dict[i]), i, bcolor=(0, 0, 0)
                        )
            else:
                print(f"key {i} is not np array or string")
                raise Exception(f"key {i} is not np array or string")

            # colculate the size of the image and resize it if need and then show it
    else:
        if showcase.get("conversions") != None:
            maxWidth = max(
                showcase["conversions"].values(), key=lambda x: x.shape[0]
            ).shape[0]
            showcase["conversions"] = added_title(
                combine_images(
                    list(showcase["conversions"].values()),
                    mWidth=maxWidth,
                    col=1,
                    compress=False,
                ),
                "conversions",
                bcolor=(0, 0, 0),
            )

        allimagesSize = [i.shape for i in showcase.values()]
        rows_comb = max([i[0] for i in allimagesSize])
        cols_comb = sum([i[1] for i in allimagesSize])

        rows_comb = max(rows_comb, canvasW)
        cols_comb = max(cols_comb, canvasH)

        canvasW = rows_comb
        canvasH = cols_comb

        comb = np.zeros(shape=(rows_comb, cols_comb, 3), dtype=np.uint8)

        cols_offset = 0
        # print('without detected',rows_comb,cols_comb)
        for i, image in showcase.items():
            rows, cols, _ = image.shape
            comb[:rows, cols_offset : cols_offset + cols, :] = image
            cols_offset += cols

    if showStats:
        # add a strip of 30 pixels at the top of the image
        comb = cv2.copyMakeBorder(
            comb, 40, 0, 0, 0, cv2.BORDER_CONSTANT, value=(0, 0, 0)
        )
        # showcase the top fps and time taken till yet
        cv2.putText(
            comb,
            f"FPS: {dict['fps']}",
            (10, 30),
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
        )
        time_taken = time.perf_counter() - dict["startsAt"]
        in_mins = divmod(time_taken, 60)
        formatedTime = "Time: " + (
            ":".join(
                map(
                    lambda x: str(int(x)),
                    [in_mins[1], *divmod(in_mins[0], 60)[::-1]][::-1],
                )
            )
        )

        text_width = cv2.getTextSize(formatedTime, cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0][0]
        # put the time to right end of the image
        possition = (comb.shape[1] - text_width, 30)
        cv2.putText(
            comb,
            formatedTime,
            possition,
            cv2.FONT_HERSHEY_SIMPLEX,
            1,
            (255, 255, 255),
            2,
        )

    # show the output image
    cv2.imshow(windowName, comb)
