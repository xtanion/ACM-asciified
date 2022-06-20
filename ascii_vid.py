from ascii_text import generate_ascii_image
import cv2
import numpy as np
import os

vid_path = 'data/sasuke-dance.gif'

# Creating a VideoCapture object to read the video
vid = cv2.VideoCapture(vid_path)
pwd = os.getcwd()
flag, frame = vid.read()
resolution = frame.shape[:-1]

# Creating a temp directory to save images
tmp_dir = os.path.join(pwd, 'tmp')
if not os.path.exists(tmp_dir):
    os.mkdir(tmp_dir)

f_count = 0
while (vid.isOpened()):

    flag, frame = vid.read()
    if flag is False:
        break

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    img_path = os.path.join(tmp_dir, f'{f_count}.png')
    generate_ascii_image(frame, img_path)

    # to save all ascii'ed frame increase f_count
    # f_count += 1
    frame = cv2.imread(img_path)
    cv2.startWindowThread()
    cv2.namedWindow("ascii")
    cv2.imshow("ascii", frame)
    if cv2.waitKey(25) & 0xFF == ord('q'):
        break


vid.release()
cv2.destroyAllWindows()

# Deleting the temoporary directory and Frames
for items in os.listdir(tmp_dir):
    os.remove(os.path.join(tmp_dir, items))
