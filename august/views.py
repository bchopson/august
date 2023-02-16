from apiflask import APIBlueprint

from august import model
from august.model import db
from august.schema import (
    MAX_PER_PAGE,
    WeatherDataQuerySchema,
    WeatherDataSchema,
    WeatherDataSummaryQuerySchema,
    WeatherDataSummarySchema,
)

api = APIBlueprint("api", __name__, url_prefix="/api")


@api.route("/weather")
@api.input(WeatherDataQuerySchema, location="query")
@api.output(WeatherDataSchema(many=True))
def weather_data(query_params: dict):
    """Historical weather data."""
    stmt = db.select(model.WeatherData).order_by(
        model.WeatherData.date, model.WeatherData.station_id
    )
    if station_id := query_params.get("station_id"):
        stmt = stmt.where(model.WeatherData.station_id == station_id)
    if date := query_params.get("date"):
        stmt = stmt.where(model.WeatherData.date == date)
    paged = db.paginate(stmt, max_per_page=MAX_PER_PAGE)
    return paged.items


@api.route("/weather/stats")
@api.input(WeatherDataSummaryQuerySchema, location="query")
@api.output(WeatherDataSummarySchema(many=True))
def weather_data_summary(query_params: dict):
    """Historical weather data aggregated by year."""
    stmt = db.select(model.WeatherDataSummary).order_by(
        model.WeatherDataSummary.year, model.WeatherDataSummary.station_id
    )
    if station_id := query_params.get("station_id"):
        stmt = stmt.where(model.WeatherDataSummary.station_id == station_id)
    if year := query_params.get("year"):
        stmt = stmt.where(model.WeatherDataSummary.year == year)
    paged = db.paginate(stmt, max_per_page=MAX_PER_PAGE)
    return paged.items
