import numpy as np
import pandas as pd

file_list = pd.read_csv("FileList.csv")
volume_file = pd.read_csv("VolumeTracings.csv")
file_names = file_list['FileName'].unique()

# Duplicated values
volume_names = volume_file['FileName']
volume_names_no_extension = np.array([name[:-4] for name in volume_names])

# Unique values
volume_unique_names = np.unique(volume_names_no_extension)


# Check videos with less or more than 42 row in volume tracings file
unique_volume_name, counts = np.unique(volume_names_no_extension, return_counts=True)
elements_counts = dict(zip(unique_volume_name, counts))

l = []
for k,v in elements_counts.items():
    if v!=42:
        l.append(k)
#         print(k + "   " + str(v))
# print(len(l))




intersection = np.intersect1d(volume_unique_names, file_names)
print(len(intersection))

difference = np.setdiff1d(file_names, volume_unique_names)
print(len(difference))
print(difference)

print('*******'*10)

difference = np.setdiff1d(volume_unique_names, file_names)
print(len(difference))
print(difference)
