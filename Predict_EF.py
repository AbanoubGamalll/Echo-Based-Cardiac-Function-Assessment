import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

from Transformer import loadTransformerModel, Detect_ESED_Frame
from Unet import loadUnetModel, predictLVForEDESFrames
from HelperFunction import load_or_get_data
from Paths import _ED_Model_Path, _ES_Model_Path, _transformerModelPath, _videosPath

# Data
test_dataSet = load_or_get_data('TEST')
print('TEST =', len(test_dataSet))

# Load Model
transformerModel = loadTransformerModel(_transformerModelPath)
ED_Model = loadUnetModel(_ED_Model_Path)
ES_Model = loadUnetModel(_ES_Model_Path)

for obj in test_dataSet:
    print(obj.fileName)
    name = obj.fileName + '.avi'
    videoPath = os.path.join(_videosPath, name)

    ES_Frame_IMG, ED_Frame_IMG = Detect_ESED_Frame(videoPath, transformerModel)

    efPred = predictLVForEDESFrames(ES_Frame_IMG, ED_Frame_IMG, ED_Model, ES_Model)

    print('EF Predicted =', efPred)
    print('EF =', obj.EF_value)
    print('-----------------------')
