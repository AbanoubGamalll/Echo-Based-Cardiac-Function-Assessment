import os
import cv2
import matplotlib.pyplot as plt
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import numpy as np
import base64
import copy

import shutil
import uvicorn

from fastapi import FastAPI, File, UploadFile

from Unet import loadUnetModel,predictMask,get_LV_volume,calculate_EF
from Transformer import Detect_ESED_Frame, loadTransformerModel
from Paths import _ED_Model_Path, _ES_Model_Path, _transformerModelPath

app = FastAPI()


print("******************************************************************")
print("Before Looad Model")
print("******************************************************************")
# Load Model
transformerModel = loadTransformerModel(_transformerModelPath)
ED_Model = loadUnetModel(_ED_Model_Path)
ES_Model = loadUnetModel(_ES_Model_Path)

print("******************************************************************")
print("After Looad Model")
print("******************************************************************")

def get_image_encoded(image,name="Frame.jpg"):
  
    # Save the image
    plt.imsave(name, image)

    with open(name, 'rb') as f:
        image_data = f.read()

    encoded_image = base64.b64encode(image_data).decode('utf-8')
    os.remove(name)
    return encoded_image

def showBinaryMask(image, mask):
    image[mask == 1] = [68/255, 138/255, 1]
    return image

@app.post("/")
def predict_EF(video: UploadFile = File(...)):


    # Save the uploaded video to disk
    with open(video.filename, "wb") as buffer:
        shutil.copyfileobj(video.file, buffer)


    print("*****************************************************************")
    print("before Transformer")
    print("*****************************************************************")

    # Predict
    ES_Frame_IMG, ED_Frame_IMG = Detect_ESED_Frame(video.filename, transformerModel)
    if ES_Frame_IMG is None or ED_Frame_IMG is None:
        return {"error": "Unable to open video file"}
    

     # Mask
    ED_pred_mask = predictMask(ED_Model, np.expand_dims(ED_Frame_IMG, axis=0))
    ES_pred_mask = predictMask(ES_Model, np.expand_dims(ES_Frame_IMG, axis=0))

    
    print("*****************************************************************")
    print("before merged images")
    print("*****************************************************************")
    # Merging the mask with the original image
    ES_pred_mask_merged = showBinaryMask(copy.deepcopy(ES_Frame_IMG), ES_pred_mask)
    ED_pred_mask_merged = showBinaryMask(copy.deepcopy(ED_Frame_IMG), ED_pred_mask)

    

    print("*****************************************************************")
    print("before get volumes")
    print("*****************************************************************")
    # Volume
    ED_pred_volume, ED_pred_landmarks = get_LV_volume(ED_pred_mask)
    ES_pred_volume, ES_pred_landmarks = get_LV_volume(ES_pred_mask)

    print("*****************************************************************")
    print("before EF")
    print("*****************************************************************")
    # EF
    ef_pred = calculate_EF(ED_pred_volume, ES_pred_volume)
    
    print("*****************************************************************")
    print("After EF")
    print("*****************************************************************")

    esv = int(ES_pred_volume)
    edv =  int(ED_pred_volume)
    ef = round(ef_pred, 2)

    imgEST = get_image_encoded(ES_Frame_IMG)
    imgEDT = get_image_encoded(ED_Frame_IMG)
    imgESU = get_image_encoded(ES_pred_mask_merged)
    imgEDU = get_image_encoded(ED_pred_mask_merged)
    
    # Remove Video
    os.remove(video.filename)

    return {
            "ESV Value":esv,
            "EDV Value":edv,
            "EF Value":ef,
            "imgEST Value": imgEST,
            "imgEDT Value":imgEDT,
            "imgESU Value":imgESU,
            "imgEDU Value":imgEDU
        }


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
