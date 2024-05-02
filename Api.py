import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import shutil
import uvicorn

from fastapi import FastAPI, File, UploadFile

from Unet import loadUnetModel, predictLVForEDESFrames
from Transformer import Detect_ESED_Frame, loadTransformerModel
from Paths import _ED_Model_Path, _ES_Model_Path, _transformerModelPath

app = FastAPI()

# Load Model
transformerModel = loadTransformerModel(_transformerModelPath)
ED_Model = loadUnetModel(_ED_Model_Path)
ES_Model = loadUnetModel(_ES_Model_Path)


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/ef")
def predict_EF(file: UploadFile = File(...)):
    # Copy File
    with open(file.filename, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Predict
    ES_Frame_IMG, ED_Frame_IMG = Detect_ESED_Frame(file.filename, transformerModel)

    if ES_Frame_IMG is None or ED_Frame_IMG is None:
        return {"error": "Unable to open video file"}

    efPred = predictLVForEDESFrames(ES_Frame_IMG, ED_Frame_IMG, ED_Model, ES_Model)

    # Remove Video
    os.remove(file.filename)

    return {
        "filename": file.filename,
        "EF Predicted": efPred
    }


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
