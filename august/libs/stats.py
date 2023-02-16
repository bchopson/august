import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert

from august import model
from august.model import db


def calculate_summary_data():
    year_expr = sa.func.date_part("year", model.WeatherData.date)
    max_expr = sa.func.cast(model.WeatherData.max_temperature, sa.Integer)
    min_expr = sa.func.cast(model.WeatherData.min_temperature, sa.Integer)
    stmt = sa.select(
        model.WeatherData.station_id,
        year_expr.label("year"),
        (sa.func.avg(max_expr) / 10).label("avg_max_temperature"),
        (sa.func.avg(min_expr) / 10).label("avg_min_temperature"),
        (sa.func.sum(model.WeatherData.precipitation) / 100).label(
            "total_precipitation"
        ),
    ).group_by(
        model.WeatherData.station_id,
        year_expr,
    )
    insert_stmt = insert(model.WeatherDataSummary.__table__).from_select(
        [
            "station_id",
            "year",
            "avg_max_temperature",
            "avg_min_temperature",
            "total_precipitation",
        ],
        stmt,
    )
    insert_stmt = insert_stmt.on_conflict_do_update(
        index_elements=model.WeatherDataSummary.__upsert_index_elements__,
        set_=model.WeatherDataSummary.__table__.c,
    )
    with db.session.begin():
        db.session.execute(insert_stmt)
