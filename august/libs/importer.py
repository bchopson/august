import csv
import datetime as dt
import logging
from pathlib import Path
from typing import Optional

from august import model
from august.model import db

log = logging.getLogger(__name__)


class WeatherDataImporter:
    def __init__(self, source_dir: Path):
        self.source_dir = source_dir

    def run(self) -> int:
        log.info("Beginning weather data import")
        with db.session.begin():
            run = model.ImportRun.start()
        count = 0
        for path in self.source_dir.glob("*.txt"):
            count += self.import_file(path)
        with db.session.begin():
            run.end(count)
            log.info(
                "Weather data import complete. % records imported or updated", count
            )
        return count

    def import_file(self, path: Path) -> int:
        count = 0
        with db.session.begin():
            with open(path, newline="") as data_file:
                reader = csv.reader(data_file, delimiter="\t")
                for row in reader:
                    model.WeatherData.upsert(
                        station_id=path.stem,
                        date=dt.date.fromisoformat(row[0]),
                        max_temperature=self.read_int_column(row[1]),
                        min_temperature=self.read_int_column(row[2]),
                        precipitation=self.read_int_column(row[3]),
                    )
                    count += 1
        return count

    def read_int_column(self, value: str) -> Optional[int]:
        n = int(value)
        if n == -9999:
            return None
        return n
