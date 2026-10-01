import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense
from sklearn.preprocessing import MinMaxScaler
import pickle

data = pd.read_csv("data/telemetry.csv")

features = data[['fuel','temp','voltage','battery','deviation','radiation','oxygen']]

scaler = MinMaxScaler()
scaled = scaler.fit_transform(features)

seq_len = 5

X=[]
y=[]

for i in range(len(scaled)-seq_len):
    X.append(scaled[i:i+seq_len])
    y.append(scaled[i+seq_len])

X=np.array(X)
y=np.array(y)

model=Sequential()

model.add(LSTM(64,input_shape=(X.shape[1],X.shape[2])))
model.add(Dense(7))

model.compile(loss="mse",optimizer="adam")

model.fit(X,y,epochs=25)

model.save("models/lstm_model.h5")

pickle.dump(scaler,open("models/scaler.pkl","wb"))

print("Model trained successfully")