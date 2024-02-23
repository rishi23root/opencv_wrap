import cv2,os

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

if __name__=='__main__':
    video = 'a.mp4'
    fps = 5
    image_folder = os.path.join(os.getcwd(),'images')
    extract_image(video,fps,image_folder)