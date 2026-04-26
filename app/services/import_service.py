import csv
from datetime import datetime

from app.database.db import SessionLocal
from app.models.weather import Weather, WindDirection
from app.repositories.repository import Repository


class ImportService:
    def __init__(self, path: str):
        self.path = path

    def run(self):
        db = SessionLocal()
        repo = Repository(db)

        items = []

        with open(self.path, encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                item = Weather(
                    country=row["country"],
                    location_name=row["location_name"],
                    last_updated=datetime.strptime(row["last_updated"], "%Y-%m-%d %H:%M"),
                    temperature_celsius=float(row["temperature_celsius"]),
                    sunrise=datetime.strptime(row["sunrise"], "%I:%M %p").time(),

                    wind_mph=float(row["wind_mph"]),
                    wind_kph=float(row["wind_kph"]),
                    wind_degree=int(row["wind_degree"]),
                    wind_direction=WindDirection(row["wind_direction"]),

                    gust_mph=float(row["gust_mph"]),
                    gust_kph=float(row["gust_kph"]),
                )

                items.append(item)

        repo.save_all(items)
        db.close()


if __name__ == "__main__":
    ImportService("data/GlobalWeatherRepository.csv").run()
    