import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
import pandas as pd

# Загрузка данных
data = load_iris()
X = data.data
y = data.target

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Заполнение пропущенных значений
imputer = SimpleImputer(strategy='mean')
X_train = imputer.fit_transform(X_train)
X_test = imputer.transform(X_test)

# Масштабирование данных
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Кодирование целевой переменной
encoder = OneHotEncoder()  # sparse=False
y_train = encoder.fit_transform(y_train.reshape(-1, 1))
y_test = encoder.transform(y_test.reshape(-1, 1))

# Удаление высоко коррелированных признаков (если применимо)
X_train_df = pd.DataFrame(X_train)
X_test_df = pd.DataFrame(X_test)
corr_matrix = X_train_df.corr().abs()
upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
to_drop = [column for column in upper.columns if any(upper[column] > 0.95)]
X_train_df = X_train_df.drop(columns=to_drop)
X_test_df = X_test_df.drop(columns=to_drop)

# Преобразование обратно в numpy массивы
X_train = X_train_df.values
X_test = X_test_df.values
