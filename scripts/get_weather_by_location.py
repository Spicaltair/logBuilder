from get_location import get_location
from get_weather import get_weather

# 获取天气信息
def get_weather_by_location():
    location = get_location()
    if 'error' in location:
        print(location['error'])
        return
    city = location['city']
    weather = get_weather(city)
    if 'error' not in weather:
        print(f"城市: {city}")
        print(f"温度: {weather['temperature']}°C")
        print(f"风速: {weather['wind_speed']} m/s")
        print(f"风向: {weather['wind_direction']}°")
        print(f"湿度: {weather['humidity']}%")
        print(f"天气状况: {weather['weather_condition']}")
    else:
        print(weather['error'])

# 示例调用
if __name__ == "__main__":
    get_weather_by_location()
