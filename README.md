# Echo-Based Cardiac Function Assessment <br> `Graduation Project 2024`

- `The goal of this project is to create a sophisticated Deep Learning system that can quickly and accurately evaluate Left Ventricle Ejection Fraction (LVEF), enhancing the diagnosis and management of cardiovascular diseases.` 
- `Precise LVEF assessment is vital for forecasting the prognosis in conditions such as congestive heart failure, yet existing techniques are often slow and lack precision.`

# System Architecture <br>
![alt results](https://github.com/AbanoubGamalll/Echo-Based-Cardiac-Function-Assessment/blob/main/Media/SystemArchitecture.png)


# Before using this repo
> you can use Kaggle Notebook directly from <a href="https://www.kaggle.com/code/abanoubgamal/gp-notebook"> HERE </a>.

You will need to request access to the 
<a href = 'https://echonet.github.io/dynamic'>EchoNet-Dynamic</a>
dataset from Stanford University. </br>
Once you have access to the data, download it and write the path of the "EchoNet-Dynamic" folder in the _dataRootPath variable in
<a href = "https://github.com/AbanoubGamalll/Echo-Based-Cardiac-Function-Assessment/blob/main/Model/Paths.py">Paths</a>.

<pre>
EchoNet-Dynamic Dataset
├── FileList.csv
├── VolumeTracings.csv
└── Videos
    ├── 0X1A0A263B22CCD966.avi
    ├── 0X1A2A76BDB5B98BED.avi
    ├── 0X1A2C60147AF9FDAE.avi
    └── etc.
</pre>

# Train Models
- train this model from 
 <a href = "https://github.com/AbanoubGamalll/Echo-Based-Cardiac-Function-Assessment/blob/main/Model/Main.py">Main</a>
and choose one model to train each time.

1) HyperModel:
- Detecting (ES-ED) Frames <br><br>
![alt results](https://github.com/AbanoubGamalll/Echo-Based-Cardiac-Function-Assessment/blob/main/Media/HeartCycle.png)

2) U-Net Model:
- Detecting Left Ventricle <br><br>
![alt results](https://github.com/AbanoubGamalll/Echo-Based-Cardiac-Function-Assessment/blob/main/Media/DetectingLV.png)


# Test Models
- Add the Model Pathts in <a href = "https://github.com/AbanoubGamalll/Echo-Based-Cardiac-Function-Assessment/blob/main/Model/Paths.py">Paths</a> <br>
Can find All Models here: <br>
        - <a href = https://www.kaggle.com/models/abanoubgamal/u-net/Keras/transformer/1> HyperModel </a> Download best.pt <br> 
        - <a href = https://www.kaggle.com/models/abanoubgamal/u-net/Keras/ed/1> U-Net ED </a> <br>
        - <a href = https://www.kaggle.com/models/abanoubgamal/u-net/Keras/es/1>  U-Net ES </a> <br>

- Run
<a href = "https://github.com/AbanoubGamalll/Echo-Based-Cardiac-Function-Assessment/blob/main/Model/Api.py"> API </a>
to open the local server using FastAPI.
- Run the <a href = "https://github.com/AbanoubGamalll/Echo-Based-Cardiac-Function-Assessment/blob/main/GUI"> GUI </a>
file using flutter.

# Team Members
- Abanoub Gamal
- Kerolos Nabil
- Kerolos Helal
- Kerolos Waheed
- Yassa Kamille
- Ganna Muhammed

# Supervisors
- Dr. Manal Mohsen Tantawi
- T.A. Radwa Reda Hossieny
