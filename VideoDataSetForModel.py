import os
import torch
import numpy as np
from HelperFunction import _extractVideoFrames, _mirroringVideo
from Paths import _videosPath


class VideoDataSetForModel(torch.utils.data.Dataset):
    def __init__(self, dataSet=None, fullVideo=False):

        self.dataSet = dataSet
        self.fullVideo = fullVideo
        self.frame_width = self.frame_height = 128

    def __len__(self):
        return len(self.dataSet)

    def __getitem__(self, index):
        obj = self.dataSet[index]

        if self.fullVideo:
            frame_count = obj.numberOfFrames
            path = os.path.join(_videosPath, obj.fileName + '.avi')
            video = _extractVideoFrames(path)
        else:
            frame_count = 128
            video = _mirroringVideo(obj)

        frames = np.zeros((frame_count, 112, 112, 3), np.float32)
        labels = np.zeros(frame_count, np.int8)

        if self.fullVideo:
            frames = video
            labels[obj.ES_frame] = 1
            labels[obj.ED_frame] = 2
        else:
            for i in range(0, frame_count):
                # 0 TR , 1 ES, 2 ED
                label = video[i][1]
                if label == 'ES':
                    label = 1
                elif label == 'ED':
                    label = 2
                else:
                    label = 0

                frames[i] = video[i][0]
                labels[i] = label

        # (F,W,H,C) > F C W H
        frames = frames.transpose((3, 0, 1, 2))

        ########################
        # Load video into np.array
        frames = frames.astype(np.float32)

        # Scale pixel values from 0-255 to 0-1
        frames /= 255.0

        frames = np.moveaxis(frames, 0, 1)
        p = 8
        frames = np.pad(frames, ((0, 0), (0, 0), (p, p), (p, p)), mode='constant', constant_values=0)
        ########################

        return frames, labels
