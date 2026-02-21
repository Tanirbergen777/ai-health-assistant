from sklearn.tree import DecisionTreeClassifier
import pandas as pd

# 1. Готовим "обучающие" данные (для диплома это пример)
# Признаки: [Возраст, ИМТ, Уровень активности]
X = [
    [20, 18.5, 5], # Молодой, худой, активный -> Легкая программа
    [45, 30.0, 1], # Старше, лишний вес, сидячий образ -> Начальная
    [25, 24.0, 3], # Средние параметры -> Средняя
    [30, 22.0, 5]  # Спортсмен -> Интенсивная
]
# Метки: 0 - Начальный, 1 - Средний, 2 - Продвинутый
y = [2, 0, 1, 2]

# 2. Обучаем модель
model = DecisionTreeClassifier()
model.fit(X, y)

def predict_difficulty(age, bmi, activity_level):
    """
    Функция принимает данные пользователя и возвращает уровень сложности
    """
    prediction = model.predict([[age, bmi, activity_level]])
    levels = {0: "Начальный (Beginner)", 1: "Средний (Intermediate)", 2: "Продвинутый (Advanced)"}
    return levels[prediction[0]]