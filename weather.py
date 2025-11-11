from flask import Flask, jsonify, request

app = Flask(__name__)


# Current weather
@app.route('/api/weather/current')
def current_weather():
    city = request.args.get('city', 'Unknown')
    data = {
        'city': city,
        'temperature': '24°C',
        'condition': 'Sunny',
        'humidity': '60%'
    }
    return jsonify(data)


# Forecast weather
@app.route('/api/weather/forecast')
def weather_forecast():
    city = request.args.get('city', 'Unknown')
    days = int(request.args.get('days', 3))

    forecast_data = []
    for i in range(days):
        forecast_data.append({
            'day': i + 1,
            'temperature': f'{25 + i}°C',
            'condition': 'Partly Cloudy'
        })

    return jsonify({
        'city': city,
        'forecast_days': days,
        'data': forecast_data
    })


if __name__ == '__main__':
    app.run(debug=True, port=5001)
