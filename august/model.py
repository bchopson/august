from august.app import db


class WeatherData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    station_id = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)
    max_temperature = db.Column(db.Integer)
    min_temperature = db.Column(db.Integer)
    precipitation = db.Column(db.Integer)


class ImportRun(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    start_utc = db.Column()
