"""
Kisan Web Project - Weather Service Routes
Integrates live Open-Meteo meteorological data, 7-day agricultural forecasts, and database caching.
"""
from flask import Blueprint, request, jsonify
from datetime import datetime, timezone, timedelta
import requests
from extensions import db
from models import WeatherCache

weather_bp = Blueprint('weather', __name__, url_prefix='/api/weather')

# Mapping WMO Weather interpretation codes to conditions and icons
WMO_CODES = {
    0: ("Clear Sky", "sun", "Optimal for all farming operations, spraying and harvesting."),
    1: ("Mainly Clear", "sun", "Good sunlight for crop photosynthesis. Ideal field day."),
    2: ("Partly Cloudy", "cloud-sun", "Favorable conditions for vegetative growth."),
    3: ("Overcast", "cloud", "Reduced evaporation. Monitor for early signs of fungal rust."),
    45: ("Foggy", "cloud-fog", "High humidity. Delay pesticide spraying until dew clears."),
    48: ("Depositing Rime Fog", "cloud-fog", "Keep sensitive seedlings sheltered."),
    51: ("Light Drizzle", "cloud-drizzle", "Mild moisture benefit. Postpone chemical sprays."),
    53: ("Moderate Drizzle", "cloud-drizzle", "Beneficial for standing rabi crops."),
    55: ("Dense Drizzle", "cloud-rain", "Ensure soil does not get over-saturated."),
    61: ("Slight Rain", "cloud-rain", "Natural irrigation boost. Hold off artificial watering."),
    63: ("Moderate Rain", "cloud-rain", "Good soil recharge. Check runoff in low-lying beds."),
    65: ("Heavy Rain", "cloud-rain-heavy", "Risk of waterlogging! Clear field drainage channels."),
    80: ("Rain Showers", "cloud-rain", "Intermittent showers. Keep harvested crops in dry sheds."),
    81: ("Moderate Showers", "cloud-rain", "Protect nursery beds from direct soil erosion."),
    82: ("Violent Showers", "cloud-lightning-rain", "Caution: High runoff. Secure irrigation pumps."),
    95: ("Thunderstorm", "cloud-lightning", "Cease all field operations. Secure outdoor machinery."),
    96: ("Thunderstorm with Hail", "cloud-hail", "High alert: Severe risk of lodging and crop damage.")
}

@weather_bp.route('/current', methods=['GET'])
def get_current_weather():
    """Retrieve current weather and 7-day forecast for given coordinates."""
    lat = float(request.args.get('lat', 28.6139))  # Default: New Delhi / Gangetic plains
    lon = float(request.args.get('lon', 77.2090))
    location_name = request.args.get('location', 'Agricultural Zone')

    # Check cache first (within 30 mins)
    cached = WeatherCache.query.filter(
        db.func.abs(WeatherCache.latitude - lat) < 0.05,
        db.func.abs(WeatherCache.longitude - lon) < 0.05
    ).order_by(WeatherCache.fetched_at.desc()).first()

    now_utc = datetime.now(timezone.utc)
    if cached and cached.fetched_at and (now_utc - cached.fetched_at.replace(tzinfo=timezone.utc)).total_seconds() < 1800:
        return jsonify({
            'source': 'cache',
            'data': cached.to_dict()
        }), 200

    # Fetch live data from Open-Meteo
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,relative_humidity_2m,precipitation_probability,weather_code,wind_speed_10m"
            "&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,wind_speed_10m_max"
            "&timezone=auto"
        )
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            raw = resp.json()
            curr = raw.get('current', {})
            daily = raw.get('daily', {})

            temp = curr.get('temperature_2m', 26.5)
            humidity = curr.get('relative_humidity_2m', 65.0)
            rain_prob = curr.get('precipitation_probability', 15.0)
            code = curr.get('weather_code', 0)
            wind = curr.get('wind_speed_10m', 12.0)

            condition_label, icon_name, advisory = WMO_CODES.get(code, ("Pleasant", "sun", "Favorable farming conditions."))

            # Build 7-day forecast array
            forecast_list = []
            dates = daily.get('time', [])
            max_temps = daily.get('temperature_2m_max', [])
            min_temps = daily.get('temperature_2m_min', [])
            rain_probs = daily.get('precipitation_probability_max', [])
            codes = daily.get('weather_code', [])

            for i in range(min(7, len(dates))):
                dt_obj = datetime.strptime(dates[i], "%Y-%m-%d")
                day_name = dt_obj.strftime("%a")
                c_code = codes[i] if i < len(codes) else 0
                c_label, c_icon, c_adv = WMO_CODES.get(c_code, ("Sunny", "sun", "Normal conditions."))
                forecast_list.append({
                    'date': dates[i],
                    'day': day_name,
                    'max_temp': max_temps[i] if i < len(max_temps) else temp + 2,
                    'min_temp': min_temps[i] if i < len(min_temps) else temp - 6,
                    'rain_prob': rain_probs[i] if i < len(rain_probs) else 10,
                    'condition': c_label,
                    'icon': c_icon,
                    'advisory': c_adv
                })

            # Store / update cache
            cache_entry = WeatherCache(
                latitude=lat,
                longitude=lon,
                location_name=location_name,
                temperature=temp,
                humidity=humidity,
                rainfall_probability=rain_prob,
                weather_condition=condition_label,
                wind_speed_kmh=wind,
                fetched_at=now_utc
            )
            cache_entry.forecast = forecast_list
            db.session.add(cache_entry)
            db.session.commit()

            return jsonify({
                'source': 'live_api',
                'data': cache_entry.to_dict()
            }), 200

    except Exception as e:
        pass

    # Fallback realistic agricultural weather data if internet or external API is offline
    today = datetime.now()
    fallback_forecast = []
    conditions = [
        ("Partly Cloudy", "cloud-sun", 28, 18, 15, "Good day for fertilizer application."),
        ("Sunny & Clear", "sun", 30, 19, 5, "Optimal for field drying and threshing."),
        ("Light Rain", "cloud-rain", 25, 17, 65, "Rain forecast: Pause irrigation pumps."),
        ("Overcast", "cloud", 26, 17, 30, "Monitor for pest activity in humid leaf canopies."),
        ("Clear Sky", "sun", 29, 18, 10, "Ideal conditions for sowing seedlings."),
        ("Pleasant Breeze", "sun", 27, 16, 20, "Favorable for pollination in blooming crops."),
        ("Scattered Showers", "cloud-drizzle", 26, 17, 45, "Keep harvested grain bags covered.")
    ]
    for i in range(7):
        day_date = today + timedelta(days=i)
        cond = conditions[i % len(conditions)]
        fallback_forecast.append({
            'date': day_date.strftime("%Y-%m-%d"),
            'day': day_date.strftime("%a"),
            'max_temp': cond[2],
            'min_temp': cond[3],
            'rain_prob': cond[4],
            'condition': cond[0],
            'icon': cond[1],
            'advisory': cond[5]
        })

    fallback_data = {
        'location_name': location_name,
        'latitude': lat,
        'longitude': lon,
        'temperature': 28.5,
        'humidity': 58.0,
        'rainfall_probability': 20.0,
        'weather_condition': 'Partly Cloudy',
        'wind_speed_kmh': 11.5,
        'forecast': fallback_forecast,
        'fetched_at': now_utc.isoformat()
    }
    return jsonify({
        'source': 'fallback',
        'data': fallback_data
    }), 200
