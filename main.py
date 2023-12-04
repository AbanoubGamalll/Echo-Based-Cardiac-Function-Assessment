import cv2
import os
import pandas as pd
import matplotlib.pyplot as plt

def read_video_frames(video_name):
    video_folder = video_name[0:-4]
    os.makedirs(video_folder, exist_ok=True)
    video = cv2.VideoCapture(video_name)
    success, image = video.read()
    count = 0
    while success:
        cv2.imwrite(f"{video_folder}/frame%d.jpg" % count, image)  # save frame as JPEG file
        success, image = video.read()
        count += 1

def draw_vertical_line(img, x1, y1, x2, y2):
    color = (0, 0, 255)  # BGR format, so (0, 0, 255) is red
    thickness = 1
    cv2.line(img, (x1, y1), (x2, y2), color, thickness)


# draw lines on a test frame
img = cv2.imread("video1/frame45.jpg")
data = pd.read_csv('VolumeTracings.csv').iloc[:21, 1:5]

for i in range(len(data)):
    x1 = data.iloc[i][0]
    y1 = data.iloc[i][1]
    x2 = data.iloc[i][2]
    y2 = data.iloc[i][3]
    draw_vertical_line(img, int(x1), int(y1), int(x2), int(y2))

plt.imshow(img)
plt.show()
