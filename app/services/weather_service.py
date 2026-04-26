from app.database.db import SessionLocal
from app.models.wind import Wind


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


if __name__ == "__main__":
    service = WeatherService()
    service.update_good_to_go_out()