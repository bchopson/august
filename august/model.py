import datetime as dt
from dataclasses import dataclass
from decimal import Decimal

import arrow
import sqlalchemy as sa
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy_utils.types import ArrowType

db = SQLAlchemy()


class UpsertMixin:
    @classmethod
    def upsert(cls, **kwargs):
        stmt = insert(cls.__table__).values(**kwargs)
        stmt = stmt.on_conflict_do_update(
            index_elements=cls.__upsert_index_elements__, set_=kwargs
        )
        db.session.execute(stmt)


@dataclass
class WeatherData(UpsertMixin, db.Model):
    __upsert_index_elements__ = ["station_id", "date"]

    id: int = db.Column(db.Integer, primary_key=True)
    station_id: str = db.Column(db.String, nullable=False)
    date: dt.date = db.Column(db.Date, nullable=False)
    max_temperature: int = db.Column(db.Integer)
    min_temperature: int = db.Column(db.Integer)
    precipitation: int = db.Column(db.Integer)

    __table_args__ = (
        sa.UniqueConstraint(station_id, date, name="uq_weather_data_station_id_date"),
    )


@dataclass
class WeatherDataSummary(UpsertMixin, db.Model):
    __upsert_index_elements__ = ["station_id", "year"]

    id: int = db.Column(db.Integer, primary_key=True)
    station_id: str = db.Column(db.String, nullable=False)
    year: int = db.Column(db.Integer, nullable=False)
    avg_max_temperature: Decimal = db.Column(db.Numeric)
    avg_min_temperature: Decimal = db.Column(db.Numeric)
    total_precipitation: Decimal = db.Column(db.Numeric)

    __table_args__ = (
        sa.UniqueConstraint(
            station_id, year, name="uq_weather_data_summary_station_id_year"
        ),
    )


@dataclass
class ImportRun(db.Model):
    id: int = db.Column(db.Integer, primary_key=True)
    count: int = db.Column(db.Integer)
    start_utc: arrow.Arrow = db.Column(ArrowType)
    end_utc: arrow.Arrow = db.Column(ArrowType)

    @classmethod
    def start(cls):
        run = cls(start_utc=arrow.utcnow())
        db.session.add(run)
        return run

    def end(self, count):
        self.count = count
        self.end_utc = arrow.utcnow()
