import math
import os
import cv2
import pickle
import numpy as np
import pandas as pd
import tensorflow as tf

from VideoData import VideoData, LandMarks
from Paths import _fileNamesPath, _volumeTracingPath, _videosPath, _loadedVideosPath


def _FilterNot_42rows(VolumeTracings, FileList):
    VolumeTracings.dropna(inplace=True)
    FileList.dropna(inplace=True)
    VolumeTracings_names = VolumeTracings['FileName']
    # VolumeTracings_names_no_extension = np.array([name[:-4] for name in VolumeTracings_names])

    VolumeUniqueName, frame_counter = np.unique(VolumeTracings_names, return_counts=True)
    Video_counts = dict(zip(VolumeUniqueName, frame_counter))

    no_rows = 0
    not_42_Rows_video_names = []
    for vName, count in Video_counts.items():
        if count != 42:
            no_rows += count
            not_42_Rows_video_names.append(vName)

    VolumeTracings = VolumeTracings[~VolumeTracings['FileName'].isin(not_42_Rows_video_names)]
    FileList = FileList[(FileList['FileName'] + ".avi").isin(VolumeTracings['FileName'])]

    # Delete rows where 'FileName' column has value '0X4F8859C8AB4DA9CB.avi'
    VolumeTracings = VolumeTracings[VolumeTracings['FileName'] != '0X4F8859C8AB4DA9CB.avi']

    return VolumeTracings, FileList


def _loadAlldata(split_type):
    FileList = pd.read_csv(_fileNamesPath)
    VolumeTracings = pd.read_csv(_volumeTracingPath)

    VolumeTracings, FileList = _FilterNot_42rows(VolumeTracings, FileList)

    leftVentricle_list = []

    VolumeTracings.dropna(inplace=True)
    FileList.dropna(inplace=True)

    for i in range(FileList.iloc[:, 0].size):

        Split = FileList.iloc[i, 8]
        if split_type != "ALL":
            if split_type != Split:
                continue
        fileName = FileList.iloc[i, 0]

        VT = VolumeTracings[VolumeTracings['FileName'] == fileName + '.avi']
        unique_Frames = VT['Frame'].unique()

        if len(unique_Frames) == 0:
            continue

        ED_Frame = unique_Frames[0]

        ES_Frame = unique_Frames[1]
        ED_tmp = VT[VT['Frame'] == ED_Frame]
        ES_tmp = VT[VT['Frame'] == ES_Frame]

        if len(ED_tmp) != 21 or len(ES_tmp) != 21:
            continue
        ED_landMark = LandMarks([], [], [], [])
        ES_landMark = LandMarks([], [], [], [])

        for k in range(21):
            ED_landMark.X1.append(ED_tmp.iloc[k, 1])
            ED_landMark.Y1.append(ED_tmp.iloc[k, 2])
            ED_landMark.X2.append(ED_tmp.iloc[k, 3])
            ED_landMark.Y2.append(ED_tmp.iloc[k, 4])

            ES_landMark.X1.append(ES_tmp.iloc[k, 1])
            ES_landMark.Y1.append(ES_tmp.iloc[k, 2])
            ES_landMark.X2.append(ES_tmp.iloc[k, 3])
            ES_landMark.Y2.append(ES_tmp.iloc[k, 4])

        EF_value = FileList.iloc[i, 1]
        ED_value = FileList.iloc[i, 2]
        ES_value = FileList.iloc[i, 3]
        numberOfFrames = FileList.iloc[i, 7]

        video_path = os.path.join(_videosPath, fileName + '.avi')

        cap = cv2.VideoCapture(video_path)

        if not cap.isOpened():
            print("Error opening video file")

        cap.set(cv2.CAP_PROP_POS_FRAMES, ED_Frame - 1)
        _, ED_Frame_IMG = cap.read()

        cap.set(cv2.CAP_PROP_POS_FRAMES, ES_Frame - 1)
        _, ES_Frame_IMG = cap.read()

        cap.release()

        obj = VideoData(fileName, EF_value, ED_value, ES_value, ED_Frame, ES_Frame, Split, ED_landMark,
                        ES_landMark, numberOfFrames, ED_Frame_IMG, ES_Frame_IMG)

        leftVentricle_list.append(obj)
    return leftVentricle_list


def load_or_get_data(spilt_type="ALL"):
    if spilt_type not in ['TRAIN', 'TEST', 'VAL', 'ALL']:
        print('Error not valid split type')
        return None

    if not os.path.exists(_loadedVideosPath):
        os.makedirs(_loadedVideosPath)
        print(f'{_loadedVideosPath} created')

    file_path = f'{_loadedVideosPath}/Loaded_Videos_Objects_{spilt_type}.pkl'
    # If file exists, load the data from the file
    if os.path.exists(file_path):
        with open(file_path, 'rb') as f:
            data = pickle.load(f)
    # If file doesn't exist, execute loadAlldata() to get the data
    else:
        data = _loadAlldata(spilt_type)
        with open(file_path, 'wb') as f:
            pickle.dump(data, f)

    return data


def _extractVideoFrames(path):
    capture = cv2.VideoCapture(str(path))
    if not capture.isOpened():
        return None
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    frame_width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frames = np.zeros((frame_count, frame_width, frame_height, 3), np.uint8)

    for count in range(frame_count):
        ret, frame = capture.read()
        if not ret:
            raise ValueError("Failed to load frame #{} of {}.".format(count, path))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frames[count] = frame
    capture.release()

    return frames


# Transformer Data
def _mirroringVideo(video_obj):
    original_tuple = []
    desired_length = 128

    path = os.path.join(_videosPath, video_obj.fileName + '.avi')

    if not os.path.exists(path):
        raise FileNotFoundError(path)

    v = _extractVideoFrames(path)

    # Mirror
    start = min(video_obj.ED_frame, video_obj.ES_frame)
    end = max(video_obj.ED_frame, video_obj.ES_frame) + 1

    for i in range(start, end):
        img = v[i]
        if video_obj.ED_frame == i:
            original_tuple.append((img, "ED"))
        elif video_obj.ES_frame == i:
            original_tuple.append((img, "ES"))
        else:
            original_tuple.append((img, "Transition"))

    while len(original_tuple) < desired_length:

        # Create a mirrored dictionary by reversing keys and values
        mirrored_tuple = list(reversed(original_tuple))[1:]

        # Append the mirrored list
        original_tuple.extend(mirrored_tuple)

        # If the list length exceeds desired_length, break the loop
        if len(original_tuple) >= desired_length:
            break

        # Append the original list again
        original_tuple.extend(original_tuple[1:])

    # Trim the dictionary to desired_length if it exceeds it
    original_tuple = original_tuple[:desired_length]

    return original_tuple


# U-Net Data
def _prepareDataToPolygon(landmark):
    data = []
    for i in range(21):
        data.append((landmark.X1[i], landmark.Y1[i]))

    for i in range(21):
        data.append((landmark.X2[i], landmark.Y2[i]))

    if data[0][1] > data[21][1]:
        tmp = data[0]
        data[0] = data[21]
        data[21] = tmp

    if data[21][0] < data[20][0]:
        tmp = data[21]
        data[21] = data[20]
        data[20] = tmp

    tmp = data[22:]
    data[22:] = tmp[::-1]

    return data


def _createBinaryMask(landmark):
    vertices = _prepareDataToPolygon(landmark)

    # Create an empty black image
    mask = np.zeros((112, 112)).astype(float)

    vertices = np.array(vertices)
    vertices = np.round(vertices)
    pts = vertices.astype(int)

    cv2.fillPoly(mask, [pts], color=(255, 255, 255))

    mask[mask == 255] = 1

    return mask


def _createImageAndMaskFolders(frameType, split, path):
    image_path = path + f'/Frames_{frameType}/'
    mask_path = path + f'/Masks_{frameType}/'

    try:
        os.makedirs(image_path)
        print(f'Frames_{frameType} create')
    except OSError:
        print(f'Frames_{frameType} is exist')

    try:
        os.makedirs(mask_path)
        print(f'Masks_{frameType} create')
    except OSError:
        print(f'Masks_{frameType} is exist')

    image_path += f'{split}/'
    mask_path += f'{split}/'

    try:
        os.makedirs(image_path)
        print(f'Frames_{frameType}/{split} create')

    except OSError:
        print(f'Frames_{frameType}/{split} is exist')

    try:
        os.makedirs(mask_path)
        print(f'Masks_{frameType}/{split} create')

    except OSError:
        print(f'Masks_{frameType}/{split} is exist')
    return image_path, mask_path


def _saveImageAndMask(frameType, split, trueMasksPath='', ):
    data_set = load_or_get_data(split)
    if data_set is None:
        return

    image_path, mask_path = _createImageAndMaskFolders(frameType, split, trueMasksPath)
    img = None
    landmarks = None
    for obj in data_set:
        if frameType == 'ES':
            img = obj.ES_Frame_IMG
            landmarks = obj.ES_landMark
        elif frameType == 'ED':
            img = obj.ED_Frame_IMG
            landmarks = obj.ED_landMark

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        mask = _createBinaryMask(landmarks)

        cv2.imwrite(mask_path + f'{obj.fileName}.png', mask)
        cv2.imwrite(image_path + f'{obj.fileName}.png', img)


def CreateAllMasks(trueMasksPath):
    try:
        os.makedirs(trueMasksPath)
        print(f'Dir_{trueMasksPath} create')
    except OSError:
        print(f'Dir_{trueMasksPath} is exist')

    _saveImageAndMask(frameType='ES', split='TRAIN', trueMasksPath=trueMasksPath)
    _saveImageAndMask(frameType='ES', split='TEST', trueMasksPath=trueMasksPath)
    _saveImageAndMask(frameType='ES', split='VAL', trueMasksPath=trueMasksPath)

    _saveImageAndMask(frameType='ED', split='TRAIN', trueMasksPath=trueMasksPath)
    _saveImageAndMask(frameType='ED', split='TEST', trueMasksPath=trueMasksPath)
    _saveImageAndMask(frameType='ED', split='VAL', trueMasksPath=trueMasksPath)


# Read Data
def _process_path(image_path, mask_path):
    img = tf.io.read_file(image_path)
    img = tf.image.decode_png(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    mask = tf.io.read_file(mask_path)
    mask = tf.image.decode_png(mask, channels=3)
    mask = tf.math.reduce_max(mask, axis=-1, keepdims=True)
    return img, mask


def getImageAndMasks(frameType='', split='', trueMasksPath=''):
    if not os.path.exists(trueMasksPath):
        os.makedirs(trueMasksPath)
        print(f'{trueMasksPath} created')
    image_path = os.path.join(trueMasksPath, f"Frames_{frameType}/{split}/")
    mask_path = os.path.join(trueMasksPath, f"Masks_{frameType}/{split}/")
    image_list = os.listdir(image_path)
    mask_list = os.listdir(mask_path)
    image_list = [image_path + i for i in image_list]
    mask_list = [mask_path + i for i in mask_list]

    image_filenames = tf.constant(image_list)
    masks_filenames = tf.constant(mask_list)

    dataset = tf.data.Dataset.from_tensor_slices((image_filenames, masks_filenames))
    print(split, len(mask_list))

    image_ds = dataset.map(_process_path)

    return image_ds


# Predict LandMask From Mask
def _getHorizontalLabel(mask):
    upXY = (112, 0)

    downXY_right = (0, 0)

    downXY_left = (0, 112)

    for x in range(112):
        for y in range(112):
            if mask[x][y] == 0:
                continue

            if upXY[0] > x and upXY[1] < y:
                upXY = (x, y)
            elif downXY_right[0] <= x and downXY_right[1] <= y:
                downXY_right = (x, y)
            elif downXY_left[0] < x or downXY_left[1] > y:
                downXY_left = (x, y)

    midpoint = ((downXY_left[0] + downXY_right[0]) // 2, (downXY_left[1] + downXY_right[1]) // 2)
    for x in range(112):
        for y in range(112):
            midpoint = (midpoint[0] + 1, midpoint[1])

            if midpoint[0] == 112 or mask[midpoint[0]][midpoint[1]] == 0:
                midpoint = (midpoint[0] - 1, midpoint[1])
                break

    #     for i in range(112):
    #         for j in range(112):
    #             if mask[i][j] == 1:
    #                 img[i][j] = (250, 250, 250)

    # plt.scatter(upXY[1], upXY[0], color='orange', marker='o')
    #
    # plt.scatter(downXY_right[1], downXY_right[0], color='orange', marker='o')
    #
    # plt.scatter(downXY_left[1], downXY_left[0], color='orange', marker='o')
    # plt.scatter(midpoint[1], midpoint[0], color='orange', marker='X')

    if midpoint[1] == upXY[1]:
        midpoint = (midpoint[0], midpoint[1] + 0.1)

    return (midpoint[1], midpoint[0]), (upXY[1], upXY[0])


def _perpendicular_points(x1, y1, x2, y2, distance):
    # Calculate slope of the original line
    if x2 - x1 != 0:  # Avoid division by zero
        slope_original = (y2 - y1) / (x2 - x1)
        # Calculate negative reciprocal to get slope of perpendicular line
        slope_perpendicular = -1 / slope_original
    else:
        slope_perpendicular = float('inf')  # Handle vertical lines

    # Find midpoint of the original line

    # Calculate unit vector along the original line
    magnitude = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    unit_vector_x = (x2 - x1) / magnitude
    unit_vector_y = (y2 - y1) / magnitude

    # Calculate displacement vector based on distance
    displacement_x = unit_vector_x * distance
    displacement_y = unit_vector_y * distance

    # New midpoint for the perpendicular line
    new_mid_x = x1 + displacement_x
    new_mid_y = y1 + displacement_y

    # Find points for the perpendicular line
    dx = 1 / (1 + slope_perpendicular ** 2) ** 0.5
    dy = slope_perpendicular * dx

    # Two points for the perpendicular line
    perpendicular_point1 = (new_mid_x + dx, new_mid_y + dy)
    perpendicular_point2 = (new_mid_x - dx, new_mid_y - dy)

    return perpendicular_point1, perpendicular_point2


def _find_previous_or_next_points(point1=None, point2=None, t='n'):
    # Extract coordinates of the two points
    x1, y1 = point1
    x2, y2 = point2
    x, y = 0, 0
    # Calculate the distance between point1 and point2
    distance = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

    # Calculate the slope of the line
    if x2 - x1 != 0:  # Avoid division by zero
        slope = (y2 - y1) / (x2 - x1)
    else:
        slope = None  # Line is vertical

    if t == 'n':
        # Calculate the next point
        if slope is not None:
            # If the line is not vertical, find next x and y
            x = x2 + (x2 - x1) / distance
            y = y2 + (y2 - y1) / distance
        else:
            # If the line is vertical, next point has the same x-coordinate
            x = x2
            y = y2 - distance
    if t == 'p':
        # Calculate the previous point
        if slope is not None:
            # If the line is not vertical, find previous x and y
            x = x1 - (x2 - x1) / distance
            y = y1 - (y2 - y1) / distance
        else:
            # If the line is vertical, previous point has the same x-coordinate
            x = x1
            y = y1 - distance

    return x, y


def _getPointsInMask(point1, point2, mask):
    # plt.plot([point1[0], point2[0]], [point1[1], point2[1]], marker='o', label='Points and Line')

    pn = point2
    lpn = None
    for i in range(112):
        if i == 0:
            pn = _find_previous_or_next_points(point1, point2, t='n')
            lpn = pn
        x = int(np.round(pn[1]))
        y = int(np.round(pn[0]))
        if x == 112 or mask[x][y] == 0:
            break
        else:
            lpn = pn
            pn = _find_previous_or_next_points(point1, pn, t='n')
        # plt.plot(pn[0], pn[1], marker='o', color='red', label='Next Point')

    pn = lpn

    pp = None
    lpp = point1
    for i in range(112):
        if i == 0:
            pp = _find_previous_or_next_points(point1, point2, t='p')
        if int(np.round(pp[1])) == 112 or int(np.round(pp[0])) == 112 \
                or mask[int(np.round(pp[1]))][int(np.round(pp[0]))] == 0:
            break
        else:
            lpp = pp
            pp = _find_previous_or_next_points(pp, point2, t='p')
        # plt.plot(pp[0], pp[1], marker='o', color='red')

    pp = lpp

    # plt.plot([pp[0], pn[0]], [pp[1], pn[1]], color='blue')

    return pn, pp


def _GetPointOfSegmentMask(mask=None):
    labels = [_getHorizontalLabel(mask)]

    x1, y1 = labels[0][0]
    x2, y2 = labels[0][1]

    numOfLines = 20
    distance = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2) / numOfLines

    point = []
    for i in range(numOfLines):
        point1, point2 = _perpendicular_points(x1, y1, x2, y2, distance * i)
        point.append((point1, point2))

        # plt.plot([x1, x2], [y1, y2], label="Original Line")
        # plt.plot([point1[0], point2[0]], [point1[1], point2[1]], label="Perpendicular Line")
        # plt.scatter([x1, x2], [y1, y2], color='red')
        # plt.scatter([point1[0], point2[0]], [point1[1], point2[1]], color='blue')

    for i in range(numOfLines):
        labels.append(_getPointsInMask(point[i][0], point[i][1], mask))

    #     for i in range(112):
    #         for j in range(112):
    #             if mask[i][j] == 1:
    #                 img[i][j] = (250, 250, 250)

    #     x = 'x'
    #     for p1, p2 in labels:
    #         plt.plot(p1[0], p1[1], marker=x, color='red', label='Next Point')
    #         plt.plot(p2[0], p2[1], marker=x, color='red', label='Next Point')
    #         plt.plot([p1[0], p2[0]], [p1[1], p2[1]], color='blue')
    #         x = 'o'

    landmarks_pred = LandMarks([], [], [], [])

    for i in range(21):
        (x1, y1), (x2, y2) = labels[i]
        landmarks_pred.X1.append(x1)
        landmarks_pred.Y1.append(y1)

        landmarks_pred.X2.append(x2)
        landmarks_pred.Y2.append(y2)

    # Arrange landmarks like Dataset
    landmarks_pred.X1[0], landmarks_pred.X2[0] = landmarks_pred.X2[0], landmarks_pred.X1[0]
    landmarks_pred.Y1[0], landmarks_pred.Y2[0] = landmarks_pred.Y2[0], landmarks_pred.Y1[0]

    landmarks_pred.X1[1:21] = landmarks_pred.X1[1:21][::-1]
    landmarks_pred.Y1[1:21] = landmarks_pred.Y1[1:21][::-1]

    landmarks_pred.X2[1:21] = landmarks_pred.X2[1:21][::-1]
    landmarks_pred.Y2[1:21] = landmarks_pred.Y2[1:21][::-1]

    return landmarks_pred


# Calc Volume and EF
def _calculate_volume(landmarks):
    X1 = landmarks.X1
    Y1 = landmarks.Y1
    X2 = landmarks.X2
    Y2 = landmarks.Y2
    verticalLine_distance = math.sqrt((X2[0] - X1[0]) ** 2 + (Y2[0] - Y1[0]) ** 2)
    dx = verticalLine_distance / 20

    volume = 0
    for i in range(1, 21):
        volume += (math.pi * ((X2[i] - X1[i]) ** 2 + (Y2[i] - Y1[i]) ** 2) * dx) / 4.0

    return volume


def calculate_EF(ED_volume, ES_volume):
    return (abs(abs(ED_volume) - abs(ES_volume)) / ED_volume) * 100


def get_LV_volume(mask):
    landmarks = _GetPointOfSegmentMask(mask)
    volume = _calculate_volume(landmarks)
    return volume, landmarks
