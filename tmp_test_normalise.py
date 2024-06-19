import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# Пример данных с положительными и отрицательными значениями
# X = np.array([[1, -1, 2],
#               [2, 0, 0],
#               [0, 1, -1],
#               [1, 1, 1],
#               [1, -1, 0]])

X = np.array([[1000, -500, 200],
              [200, 300, -800],
              [900, 100, -100],
              [100, 1000, 100],
              [100, -100, 1000]])

y = np.array([0, 1, 0, 1, 0])

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Стандартизация данных
standard_scaler = StandardScaler()
X_train_standardized = standard_scaler.fit_transform(X_train)
X_test_standardized = standard_scaler.transform(X_test)

# Масштабирование данных с Min-Max Scaler
minmax_scaler = MinMaxScaler(feature_range=(-1, 1))
X_train_minmax_scaled = minmax_scaler.fit_transform(X_train)
X_test_minmax_scaled = minmax_scaler.transform(X_test)

print("Original X_train:\n", X_train)
print("Standardized X_train:\n", X_train_standardized)
print("Min-Max Scaled X_train:\n", X_train_minmax_scaled)
