import requests

# 配置 API 信息
API_KEY = 'a50b80b50d70a0d26b0f43b6e2f03e4b'  # 替换为您的 API 密钥
BASE_URL = 'http://api.openweathermap.org/data/2.5/weather'

def get_weather(city):
    params = {
        'q': city,           # 城市名称
        'appid': API_KEY,    # API 密钥
        'units': 'metric',   # 摄氏度
        'lang': 'zh'         # 中文描述
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code == 200:
        data = response.json()
        return {
            'temperature': data['main']['temp'],         # 温度
            'wind_speed': data['wind']['speed'],         # 风速
            'wind_direction': data['wind']['deg'],       # 风向
            'humidity': data['main']['humidity'],        # 湿度
            'weather_condition': data['weather'][0]['description'],  # 天气状况
        }
    else:
        return {'error': f"Error {response.status_code}: {response.reason}"}

# 示例调用
if __name__ == "__main__":
    city_name = "Beijing"  # 替换为实际城市名称
    weather = get_weather(city_name)
    if 'error' in weather:
        print(weather['error'])
    else:
        print(f"城市: {city_name}")
        print(f"温度: {weather['temperature']}°C")
        print(f"风速: {weather['wind_speed']} m/s")
        print(f"风向: {weather['wind_direction']}°")
        print(f"湿度: {weather['humidity']}%")
        print(f"天气状况: {weather['weather_condition']}")

