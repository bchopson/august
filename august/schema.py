from apiflask import Schema
from marshmallow import fields

MAX_PER_PAGE = 100


class PaginationSchema(Schema):
    page = fields.Int()
    per_page = fields.Int(max=MAX_PER_PAGE)


class WeatherDataSchema(Schema):
    id = fields.Int(required=True)
    station_id = fields.Str(required=True)
    date = fields.Date(required=True)
    max_temperature = fields.Int()
    min_temperature = fields.Int()
    precipitation = fields.Int()


class WeatherDataQuerySchema(PaginationSchema):
    station_id = fields.Str()
    date = fields.Date()


class WeatherDataSummarySchema(Schema):
    id = fields.Int(required=True)
    station_id = fields.Str(required=True)
    year = fields.Int(required=True)
    avg_max_temperature = fields.Decimal(as_string=True)
    avg_min_temperature = fields.Decimal(as_string=True)
    total_precipitation = fields.Decimal(as_string=True)


class WeatherDataSummaryQuerySchema(PaginationSchema):
    station_id = fields.Str()
    year = fields.Int()
