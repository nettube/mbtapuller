from flask import Flask, render_template, jsonify
import Database
import Functions
import StatCache
import FleetAnalyzer
from constants import *

from services.stations_service import stations_service
from services.station_details_service import station_details_service
from services.train_service import train_service
from services.route_service import route_service

Database.wait_for_available()
session = Database.connect()

app = Flask(__name__)

# app.register_blueprint(stations_service)
# app.register_blueprint(station_details_service)
# app.register_blueprint(train_service)
# app.register_blueprint(route_service)


# @app.route("/", methods=['GET', 'POST'])
# def home():
#     lines = sorted(Functions.all_routes(session), key=lambda k: k['name'])
#     return render_template('index.html', lines=lines)


@app.route("/puller/movement_average.json")
def movement_average_json():
    all = StatCache.circular_all(Database.connect_redis(), 'movement_average')[::-1]
    return jsonify(all)


@app.route("/puller/orange_movement_average.json")
def movement_average_orange_json():
    all = StatCache.circular_all(Database.connect_redis(), 'orange_movement_average')[::-1]
    return jsonify(all)


# Fleet analysis
@app.route("/puller/fleet/today.json")
def fleet_today_all():
    return jsonify({
        RED_LINE: FleetAnalyzer.model_frequency_for_route(session, RED_LINE),
        ORANGE_LINE: FleetAnalyzer.model_frequency_for_route(session, ORANGE_LINE),
        BLUE_LINE: FleetAnalyzer.model_frequency_for_route(session, BLUE_LINE),
        GREEN_LINE_B: FleetAnalyzer.model_frequency_for_route(session, GREEN_LINE_B),
        GREEN_LINE_C: FleetAnalyzer.model_frequency_for_route(session, GREEN_LINE_C),
        GREEN_LINE_D: FleetAnalyzer.model_frequency_for_route(session, GREEN_LINE_D),
        GREEN_LINE_E: FleetAnalyzer.model_frequency_for_route(session, GREEN_LINE_E),
    })


if __name__ == "__main__":
    app.run(host='0.0.0.0')
