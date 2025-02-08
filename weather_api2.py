import requests
from flask import Flask, jsonify


TOKEN = "Token"
URL = "https://api.weather.yandex.ru/v2/forecast?lat=52.37125&lon=4.89388"


app = Flask(__name__)

def get_coordinates(city_name):
    url = f"https://geocode-maps.yandex.ru/1.x/?format=json&geocode={city_name}"
    response = requests.get(url)
    data = response.json()
    
    if 'response' in data and 'GeoObjectCollection' in data['response']:
        pos = data['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos']
        lon, lat = pos.split()
        return float(lat), float(lon)
    else:
        return None

def get_weather_from_api(lat, lon):
    headers = {
        'X-Yandex-Weather-Key': TOKEN
    }

    url = f"https://api.weather.yandex.ru/v2/forecast?lat={lat}&lon={lon}"

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        weather = data.get("fact", None)
        return weather
    else:
        return None

@app.route("/weather/<city>", methods=["GET"])
def get_weather(city):
    coordinates = get_coordinates(city)
    if coordinates:
        lat, lon = coordinates
        weather = get_weather_from_api(lat, lon)
        if weather:
            return jsonify({
                "temperature": weather["temp"],  # Температура
                "condition": weather["condition"]  # Погодные условия
            })
        else:
            return jsonify({"error": "Не удалось получить данные о погоде"}), 500
    else:
        return jsonify({"error": "Город не найден"}), 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
