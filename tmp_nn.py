# Отключение oneDNN
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.utils import to_categorical
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.datasets import load_iris

# Отключение oneDNN
import os
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# Загрузка данных
data = load_iris()
X = data.data
y = data.target

# Преобразование меток в one-hot encoding
y = to_categorical(y)

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Масштабирование данных
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model = Sequential([
    # Input(shape=(X_train.shape[1],)),
    Dense(64, input_shape=(X_train.shape[1],), activation='relu'),
    Dense(32, activation='relu'),
    Dense(y_train.shape[1], activation='softmax')
])

model.compile(optimizer=Adam(learning_rate=0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train, y_train, epochs=50, batch_size=8, validation_split=0.2)

loss, accuracy = model.evaluate(X_test, y_test)
print(f'Test Accuracy: {accuracy:.4f}')

predictions = model.predict(X_test)

# Установка параметра вывода
np.set_printoptions(suppress=True, precision=4)

# print("Formatted Predictions:\n", predictions)

# Пример вывода вероятностей для первого примера из тестовой выборки
print(predictions[0])
print(predictions)
