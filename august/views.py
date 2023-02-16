import datetime as dt

import flask

from august import model
from august.model import db

api = flask.Blueprint("api", __name__, url_prefix="/api")

MAX_PER_PAGE = 100


@api.route("/weather")
def weather_data():
    stmt = db.select(model.WeatherData).order_by(
        model.WeatherData.date, model.WeatherData.station_id
    )
    if station_id := flask.request.args.get("station_id"):
        stmt = stmt.where(model.WeatherData.station_id == station_id)
    if date_str := flask.request.args.get("date"):
        try:
            date = dt.date.fromisoformat(date_str)
            stmt = stmt.where(model.WeatherData.date == date)
        except ValueError:
            flask.abort(400)
    page = db.paginate(stmt, max_per_page=MAX_PER_PAGE)
    return flask.jsonify(page.items)


@api.route("/weather/stats")
def weather_data_summary():
    stmt = db.select(model.WeatherDataSummary).order_by(
        model.WeatherDataSummary.year, model.WeatherDataSummary.station_id
    )
    if station_id := flask.request.args.get("station_id"):
        stmt = stmt.where(model.WeatherDataSummary.station_id == station_id)
    if year_str := flask.request.args.get("year"):
        try:
            year = int(year_str)
            stmt = stmt.where(model.WeatherDataSummary.year == year)
        except ValueError:
            flask.abort(400)
    page = db.paginate(stmt, max_per_page=MAX_PER_PAGE)
    return flask.jsonify(page.items)
