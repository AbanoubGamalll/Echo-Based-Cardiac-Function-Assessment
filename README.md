> # Echo-Based Cardiac Function Assessment `Graduation Project 2024`



# Before using this repo
You will need to request access to the 
<a href = 'https://echonet.github.io/dynamic'>EchoNet-Dynamic</a>
dataset from Stanford University. </br>
Once you have access to the data, download it and write the path of the "EchoNet-Dynamic" folder in the _dataRootPath variable in
<a href = "https://github.com/AbanoubGamalll/Echo-Based-Cardiac-Function-Assessment/blob/main/Model/Paths.py">Paths</a>..

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

Note: you can use Kaggle directly from 
<a href="https://www.kaggle.com/code/abanoubgamal/notebook"> HERE </a>.



# Train Models
- train this model from 
 <a href = "https://github.com/AbanoubGamalll/Echo-Based-Cardiac-Function-Assessment/blob/main/Model/Main.py">Main</a>
and choose one model to train each time.

1) HyperModel:
> Detecting (ES-ED) Frames 
![alt results](https://github.com/AbanoubGamalll/Echo-Based-Cardiac-Function-Assessment/Media/HeartCycle.png)

2) U-Net Model:
> Detecting Left Ventricle 
![alt results](https://github.com/AbanoubGamalll/Echo-Based-Cardiac-Function-Assessment/Media/DetectingLV.png)


# Test Models
> Add the path of model in this file
 <a href = "https://github.com/AbanoubGamalll/Echo-Based-Cardiac-Function-Assessment/blob/main/Model/Paths.py">Paths</a>.

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