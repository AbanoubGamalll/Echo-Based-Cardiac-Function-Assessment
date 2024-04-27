# DataSet
# - EchoNet-Dynamic
# ----- FileList.csv
# ----- VolumeTracings.csv
# ----- Videos
# ---------- 0X1A0A263B22CCD966.avi
# ---------- 0X1A2A76BDB5B98BED.avi
# ---------- 0X1A2C60147AF9FDAE.avi
# ---------- etc.

_dataRootPath = "E:/Fcis Material/Graduation Project/DataSet (EchoNet-Dynamic)/"
_videosPath = _dataRootPath + 'Videos'
_fileNamesPath = _dataRootPath + 'FileList.csv'
_volumeTracingPath = _dataRootPath + 'VolumeTracings.csv'

# Loaded Videos
_loadedVideosPath = './Loaded Videos'

# Transformer
_transformerModelPath = './Models/TransformerModel.pt'

# U-NET
_trueMasksPath = './True Masks'
_ED_Model_Path = 'Models/ED_U_NET_Model.weights.h5'
_ES_Model_Path = './Models/ES_U_NET_Model.weights.h5'
