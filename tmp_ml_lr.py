from sklearn.linear_model import LogisticRegression
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Загрузка данных
data = load_iris()
X_train, X_test, y_train, y_test = train_test_split(data.data, data.target, test_size=0.3, random_state=42)

# Проверка формы y_train и y_test
print(f'y_train shape: {y_train.shape}')
print(f'y_test shape: {y_test.shape}')
print(y_test)

# Обучение модели
model = LogisticRegression(max_iter=200)
model.fit(X_train, y_train)

# Вывод вероятностей
probabilities = model.predict_proba(X_test)
print(probabilities)
