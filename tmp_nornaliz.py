import pandas as pd

# Создание DataFrame
data = {'col1': ['value: 10', 'value: 20', 'value: 30']}
df = pd.DataFrame(data)

# Извлечение числовых данных, нормализация и вставка обратно
df['numeric_value'] = df['col1'].str.extract(r'(\d+)').astype(int)  # Использование необработанной строки r'(\d+)'
df['numeric_value'] = (
    df['numeric_value'] - df['numeric_value'].min()) / (df['numeric_value'].max() - df['numeric_value'].min()
)
df['col1'] = 'value: ' + df['numeric_value'].astype(str)

# Удаление временной колонки
df = df.drop(columns=['numeric_value'])

print(df)
