import pickle
import numpy as np
from sklearn.ensemble import IsolationForest

def train_anomaly_model(data):

    model = IsolationForest(contamination=0.05)

    model.fit(data)

    pickle.dump(model, open("models/anomaly_model.pkl","wb"))

def detect_anomaly(values):

    model = pickle.load(open("models/anomaly_model.pkl","rb"))

    result = model.predict([values])

    if result[0] == -1:
        return "ANOMALY"

    if values[1] > 38 or values[5] > 6:
        return "THRESHOLD"

    return "NORMAL"