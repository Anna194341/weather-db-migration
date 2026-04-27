from app.database.db import SessionLocal
from app.models.wind import Wind
from app.models.weather import Weather
from sqlalchemy import func
from sqlalchemy.orm import joinedload

class WeatherService:
    def update_good_to_go_out(self):
        db = SessionLocal()

        try:
            winds = db.query(Wind).all()

            for wind in winds:
                wind.is_good_to_go_out = wind.wind_kph <= 36

            db.commit()

            print(f"Updated {len(winds)} wind records.")

        finally:
            db.close()

    def get_weather_by_country_and_date(self, country: str, date_str: str):
        db = SessionLocal()

        try:
            results = (
                db.query(Weather)
                .options(joinedload(Weather.wind))
                .filter(Weather.country == country)
                .filter(func.date(Weather.last_updated) == date_str)
                .all()
            )

            return results

        finally:
            db.close()


if __name__ == "__main__":
    service = WeatherService()
    service.update_good_to_go_out()