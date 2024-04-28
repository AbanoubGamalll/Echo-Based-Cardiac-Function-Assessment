import numpy as np
from keras.src.losses import SparseCategoricalCrossentropy
from sklearn.metrics import mean_squared_error
import tensorflow as tf
from UnetModel import unetModel
from HelperFunction import get_LV_volume, calculate_EF


def predictLVForEDESFrames(ES_Frame_IMG, ED_Frame_IMG, ED_model, ES_model):
    # Mask
    ED_pred_mask = predictMask(ED_model, np.expand_dims(ED_Frame_IMG, axis=0))
    ES_pred_mask = predictMask(ES_model, np.expand_dims(ES_Frame_IMG, axis=0))

    # Volume
    ED_pred_volume, ED_pred_landmarks = get_LV_volume(ED_pred_mask)
    ES_pred_volume, ES_pred_landmarks = get_LV_volume(ES_pred_mask)

    # EF
    ef_pred = calculate_EF(ED_pred_volume, ES_pred_volume)

    return ef_pred


def calculate_mean_mse(ground_truth_masks, predicted_masks):
    num_masks = len(predicted_masks)
    mse_values = []

    for i in range(num_masks):
        mse = mean_squared_error(ground_truth_masks[i].flatten(), predicted_masks[i].flatten())
        mse_values.append(mse)

    mean_mse = np.mean(mse_values)
    print(f"Mean MSE: {mean_mse * 100}")
    # return mean_mse


def _createPredictedMask(pred_mask):
    pred_mask = tf.argmax(pred_mask, axis=-1)
    pred_mask = pred_mask[..., tf.newaxis]
    return pred_mask[0]


def predictMask(model, image):
    mask = _createPredictedMask(model.predict(image))
    mask = mask.numpy()
    mask = np.squeeze(mask)
    return mask


def loadUnetModel(path):
    loaded_model = unetModel(input_size=(112, 112, 3), n_filters=32, n_classes=2)
    loaded_model.load_weights(path)
    loaded_model.compile(optimizer='adam', loss=SparseCategoricalCrossentropy(from_logits=True), metrics=['accuracy'])

    # print(loaded_model.get_weights()[0][0][0][0])

    return loaded_model


def trainUnet(dataSet, epochs=5, batchSize=32, modelPath='', name=''):
    unet = unetModel(input_size=(112, 112, 3), n_filters=32, n_classes=2)
    unet.compile(optimizer='adam', loss=SparseCategoricalCrossentropy(from_logits=True),
                 metrics=['accuracy'])
    # unet.summary()

    BUFFER_SIZE = 500
    dataSet.batch(batchSize)
    dataSet = dataSet.cache().shuffle(BUFFER_SIZE).batch(batchSize)

    unet.fit(dataSet, epochs=epochs)

    unet.save_weights(f'{modelPath}/{name}.weights.h5')


def testUnet(dataSet, path=''):
    dataSet.batch(1)
    dataSet = dataSet.cache().batch(1)

    loaded_model = loadUnetModel(path)

    evaluation_result = loaded_model.evaluate(dataSet)
    print("Test Accuracy:", evaluation_result[1])
