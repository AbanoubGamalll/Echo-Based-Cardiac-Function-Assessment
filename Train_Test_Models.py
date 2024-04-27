import Transformer
import Unet
from HelperFunction import load_or_get_data, CreateAllMasks, getImageAndMasks
from paths import _transformerModelPath, _trueMasksPath, _ED_Model_Path, _ES_Model_Path

train_dataSet = load_or_get_data(spilt_type='TRAIN')
print('TRAIN =', len(train_dataSet))

test_dataSet = load_or_get_data(spilt_type='TEST')
print('TEST =', len(test_dataSet))

val_dataSet = load_or_get_data(spilt_type='VAL')
print('VAL =', len(val_dataSet))

# Transformer Model
Transformer.train(train_dataSet, num_epochs=2, batch_size=2, parallel=True)
Transformer.test(_transformerModelPath, test_dataSet)

# Prepare Data For U-NET
CreateAllMasks(_trueMasksPath)

#  TRAIN & TEST
frameType = 'ED'
unet_dataset_train = getImageAndMasks(frameType=frameType, split='TRAIN', trueMasksPath=_trueMasksPath)
unet_dataset_test = getImageAndMasks(frameType=frameType, split='TEST', trueMasksPath=_trueMasksPath)
unet_dataset_val = getImageAndMasks(frameType=frameType, split='VAL', trueMasksPath=_trueMasksPath)

# ED U-NET Model
Unet.train(unet_dataset_train, epochs=5, batchSize=32, modelPath='', name=f'{frameType}_U_NET_Model')
Unet.test(unet_dataset_test, path=_ED_Model_Path)

frameType = 'ES'
unet_dataset_train = getImageAndMasks(frameType=frameType, split='TRAIN', trueMasksPath=_trueMasksPath)
unet_dataset_test = getImageAndMasks(frameType=frameType, split='TEST', trueMasksPath=_trueMasksPath)
unet_dataset_val = getImageAndMasks(frameType=frameType, split='VAL', trueMasksPath=_trueMasksPath)

# 80,20 %
N = 550
unet_dataset_train = unet_dataset_train.concatenate(unet_dataset_val.take(N))
unet_dataset_val = unet_dataset_val.skip(N)
unet_dataset_test = unet_dataset_test.concatenate(unet_dataset_val)
print(len(unet_dataset_train))
print(len(unet_dataset_test))

# ES U-NET Model
Unet.train(unet_dataset_train, epochs=5, batchSize=32, modelPath='', name=f'{frameType}_U_NET_Model')
Unet.test(unet_dataset_test, path=_ES_Model_Path)