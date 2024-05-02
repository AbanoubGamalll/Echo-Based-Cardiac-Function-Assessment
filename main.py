import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import numpy as np

from Transformer import loadTransformerModel, Detect_ESED_Frame
from Unet import loadUnetModel, predictLVForEDESFrames, predictMask
from HelperFunction import load_or_get_data, calculate_EF, get_LV_volume, _createBinaryMask
from Paths import _ED_Model_Path, _ES_Model_Path, _transformerModelPath, _videosPath

# Data
test_dataSet = load_or_get_data('TEST')
print('TEST =', len(test_dataSet))

# Load Model
transformerModel = loadTransformerModel(_transformerModelPath)
ED_Model = loadUnetModel(_ED_Model_Path)
ES_Model = loadUnetModel(_ES_Model_Path)

for obj in test_dataSet[0:1]:
    print(obj.fileName)
    name = obj.fileName + '.avi'
    videoPath = os.path.join(_videosPath, name)

    ES_Frame_IMG, ED_Frame_IMG = Detect_ESED_Frame(videoPath, transformerModel)
    # ES_Frame_IMG, ED_Frame_IMG = obj.ES_Frame_IMG, obj.ED_Frame_IMG

    efPred = predictLVForEDESFrames(ES_Frame_IMG, ED_Frame_IMG, ED_Model, ES_Model)

    print('EF Predicted =', efPred)
    print('EF =', obj.EF_value)
    print('-----------------------')

# listEFTrue = []
# listEFPred = []
# listEDV = []
# listESV = []
# i = 0
# for obj in test_dataSet[0:1]:
#     print(i, obj.fileName)
#     i += 1
#
#     # Mask
#     ED_true_mask = _createBinaryMask(obj.ED_landMark)
#     ES_true_mask = _createBinaryMask(obj.ES_landMark)
#
#     ED_pred_mask = predictMask(ED_Model, np.expand_dims(obj.ED_Frame_IMG, axis=0))
#     ES_pred_mask = predictMask(ES_Model, np.expand_dims(obj.ES_Frame_IMG, axis=0))
#
#     # Volume
#     ED_true_volume, ED_true_landmarks = get_LV_volume(ED_true_mask)
#     ES_true_volume, ES_true_landmarks = get_LV_volume(ES_true_mask)
#
#     ED_pred_volume, ED_pred_landmarks = get_LV_volume(ED_pred_mask)
#     ES_pred_volume, ES_pred_landmarks = get_LV_volume(ES_pred_mask)
#     print(ED_pred_volume)
#     # EF
#     ef_true = calculate_EF(ED_true_volume, ES_true_volume)
#     ef_pred = calculate_EF(ED_pred_volume, ES_pred_volume)
#
#     # Print
#     diffTrue = abs(obj.EF_value - ef_true)
#     diffPred = (abs(obj.EF_value - ef_pred))
#
#     print('ED_volume:', ED_pred_volume, ' ,True:', ED_true_volume)
#     print('ES_volume:', ES_pred_volume, 'True:',   ES_true_volume)
#     print('EF Pred:', ef_pred, 'TRUE', obj.EF_value)
#     print('Diff True: ', diffTrue)
#     print('Diff pred: ', diffPred)
#
#     listEFTrue.append(diffTrue)
#     listEFPred.append(diffPred)
#     listEDV.append(abs(ED_true_volume - ED_pred_volume))
#     listESV.append(abs(ES_true_volume - ES_pred_volume))
#
#     # Show
#     # print('True ED')
#     # img1 = obj.ED_Frame_IMG.copy()
#     # landmark = ED_true_landmarks
#     # for l in range(0, 21):
#     #     plt.plot([landmark.X1[l], landmark.X2[l]], [landmark.Y1[l], landmark.Y2[l]], color='orange')
#     #     plt.plot(landmark.X1[l], landmark.Y1[l], marker='*', color='green')
#     #     plt.plot(landmark.X2[l], landmark.Y2[l], marker='*', color='green')
#     # showBinaryMask(img1, ED_true_mask)
#     # plt.imshow(img1)
#     # plt.axis('off')
#     # plt.show()
#     # plt.imshow(obj.ES_Frame_IMG)
#     # plt.axis('off')
#     # plt.show()
#     #
#     # print('Pred ED')
#     # img2 = obj.ED_Frame_IMG.copy()
#     # showBinaryMask(img2, ED_pred_mask)
#     # landmark = ED_pred_landmarks
#     # for l in range(0, 21):
#     #     plt.plot([landmark.X1[l], landmark.X2[l]], [landmark.Y1[l], landmark.Y2[l]], color='orange')
#     #     plt.plot(landmark.X1[l], landmark.Y1[l], marker='*', color='green')
#     #     plt.plot(landmark.X2[l], landmark.Y2[l], marker='*', color='green')
#     # plt.imshow(img2)
#     # plt.axis('off')
#     # plt.show()
#     #
#     # print('True ES')
#     # img1 = obj.ES_Frame_IMG.copy()
#     # landmark = ES_true_landmarks
#     # for l in range(0, 21):
#     #     plt.plot([landmark.X1[l], landmark.X2[l]], [landmark.Y1[l], landmark.Y2[l]], color='orange')
#     #     plt.plot(landmark.X1[l], landmark.Y1[l], marker='*', color='green')
#     #     plt.plot(landmark.X2[l], landmark.Y2[l], marker='*', color='green')
#     # showBinaryMask(img1, ES_true_mask)
#     # plt.imshow(img1)
#     # plt.axis('off')
#     # plt.show()
#     #
#     # print('Pred ES')
#     # img2 = obj.ES_Frame_IMG.copy()
#     # showBinaryMask(img2, ES_pred_mask)
#     # landmark = ES_pred_landmarks
#     # for l in range(0, 21):
#     #     plt.plot([landmark.X1[l], landmark.X2[l]], [landmark.Y1[l], landmark.Y2[l]], color='orange')
#     #     plt.plot(landmark.X1[l], landmark.Y1[l], marker='*', color='green')
#     #     plt.plot(landmark.X2[l], landmark.Y2[l], marker='*', color='green')
#     # plt.imshow(img2)
#     # plt.axis('off')
#     # plt.show()
#
#     print('------------------------------------------------')
#
# print("Average Error True:", sum(listEFTrue) / len(listEFTrue))
# print("Average Error Pred:", sum(listEFPred) / len(listEFPred))
# print("Average Error ED V:", sum(listEDV) / len(listEDV))
# print("Average Error ES V:", sum(listESV) / len(listESV))
# print(max(listEFPred))
