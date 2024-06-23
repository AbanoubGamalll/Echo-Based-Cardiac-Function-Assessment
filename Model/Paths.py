# DataSet
""" Dataset Files
EchoNet-Dynamic Dataset
├── FileList.csv
├── VolumeTracings.csv
└── Videos
    ├── 0X1A0A263B22CCD966.avi
    ├── 0X1A2A76BDB5B98BED.avi
    ├── 0X1A2C60147AF9FDAE.avi
    └── etc.
"""

# TODO ADD Your _dataRootPath for Dataset
_dataRootPath = ''
_videosPath = _dataRootPath + '/Videos'
_fileNamesPath = _dataRootPath + '/FileList.csv'
_volumeTracingPath = _dataRootPath + '/VolumeTracings.csv'

# Loaded Videos
_loadedVideosPath = ''

# Transformer
# TODO ADD Your Transformer Model
_transformerModelPath = 'TransformerModel.pt'

# U-NET
_trueMasksPath = './True Masks'
# TODO ADD Your ED_Unet Model
_ED_Model_Path = 'ED_Unet.weights.h5'
# TODO ADD Your ES_Unet Model
_ES_Model_Path = 'ES_Unet.weights.h5'
