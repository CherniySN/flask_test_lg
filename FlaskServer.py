from flask import Flask, request, jsonify
import pickle
import datetime
import os  # Импортируем модуль os

print(f'1-print {datetime.datetime.now()}')
def pred_client(client, dv, model):
    X = dv.transform([client])
    y_pred = model.predict_proba(X)[:, 1]
    return y_pred[0]

print(f'2-print {datetime.datetime.now()}')
with open ("scoring.bin", 'rb') as f_in:
    dv, model = pickle.load(f_in)

print(f'3-print {datetime.datetime.now()}')
app = Flask('scoring')  # создаем прилоложение Flask (центральный обьект для регистрации)

print(f'4-print {datetime.datetime.now()}')

@app.route('/scoring', methods=['POST'])  # Определяем маршрут /ping
def pred():
    client = request.get_json()  # получаем содержимое запросов

    prediction = pred_client(client, dv, model)  # оцениваем клиента

    pred_result = prediction >= 0.5

    result = {'probability of default': float(prediction),
              'default': bool(pred_result)}
    print(f'5-print {datetime.datetime.now()}')
    print(result)
    return jsonify(result)  # преобразуем в json


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 9697))  # Получаем порт из переменной окружения или используем 9697 по умолчанию
    app.run(debug=False, host='0.0.0.0', port=port)  # Запускаем приложение