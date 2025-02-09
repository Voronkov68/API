from flask import Flask, jsonify

app = Flask(__name__)

weather_data = {
    "Moscow": {"temperature": -3, "condition": "Ясно"},
    "Sankt-Peterburg": {"temperature": -5, "condition": "Облачно с прояснениями"},
    "Rostov": {"temperature": -4, "condition": "Ясно"}
}

@app.route("/weather/<city>", methods=["GET"])
def get_weather(city):
    city = city.capitalize()
    if city in weather_data:
        return jsonify(weather_data[city])
    else:
        return jsonify({"error": "Город не найден"}), 404

if __name__ =="__main__":
    app.run(host="0.0.0.0", port=5000)