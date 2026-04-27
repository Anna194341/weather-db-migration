from app.services.weather_service import WeatherService


def main():
    service = WeatherService()

    country = input("Enter country: ").strip()
    date = input("Enter date (YYYY-MM-DD): ").strip()

    results = service.get_weather_by_country_and_date(country, date)

    if not results:
        print("No data found.")
        return

    for w in results:
        print("\n--- Weather Record ---")
        print(f"Country: {w.country}")
        print(f"Location: {w.location_name}")
        print(f"Last Updated: {w.last_updated}")
        print(f"Temperature (C): {w.temperature_celsius}")
        print(f"Sunrise: {w.sunrise}")

        if w.wind:
            print(f"Wind kph: {w.wind.wind_kph}")
            print(f"Wind direction: {w.wind.wind_direction.value}")
            print(f"Gust kph: {w.wind.gust_kph}")
            print(f"Good to go out: {w.wind.is_good_to_go_out}")


if __name__ == "__main__":
    main()