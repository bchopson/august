import arrow
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy_utils.types import ArrowType

from august.app import db


class UpsertMixin:
    @classmethod
    def upsert(cls, **kwargs):
        stmt = insert(cls.__table__).values(**kwargs)
        stmt = stmt.on_conflict_do_update(
            index_elements=cls.__upsert_index_elements__, set_=kwargs
        )
        db.session.execute(stmt)


class WeatherData(UpsertMixin, db.Model):
    __upsert_index_elements__ = ["station_id", "date"]

    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    max_temperature = db.Column(db.Integer)
    min_temperature = db.Column(db.Integer)
    precipitation = db.Column(db.Integer)

    __table_args__ = (
        sa.UniqueConstraint(station_id, date, name="uq_weather_data_station_id_date"),
    )


class WeatherDataSummary(UpsertMixin, db.Model):
    __upsert_index_elements__ = ["station_id", "year"]

    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    avg_max_temperature = db.Column(db.Numeric)
    avg_min_temperature = db.Column(db.Numeric)
    total_precipitation = db.Column(db.Numeric)

    __table_args__ = (
        sa.UniqueConstraint(
            station_id, year, name="uq_weather_data_summary_station_id_year"
        ),
    )


class ImportRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    count = db.Column(db.Integer)
    start_utc = db.Column(ArrowType)
    end_utc = db.Column(ArrowType)

    @classmethod
    def start(cls):
        run = cls(start_utc=arrow.utcnow())
        db.session.add(run)
        return run

    def end(self, count):
        self.count = count
        self.end_utc = arrow.utcnow()
