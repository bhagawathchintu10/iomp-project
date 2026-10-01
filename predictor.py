import numpy as np
import pickle
from keras.models import load_model

model = load_model("models/lstm_model.h5")

scaler = pickle.load(open("models/scaler.pkl","rb"))

def predict_future(data):

    arr=np.array(data).reshape(1,5,7)

    pred=model.predict(arr)

    pred=scaler.inverse_transform(pred)

    return pred[0]