import requests



API_KEY = "a50b80b50d70a0d26b0f43b6e2f03e4b"  # 替换为实际的 API 密钥

def fetch_city_list():
    """
    模拟获取城市列表的 API 调用
    """
    try:
        response = requests.get('https://countriesnow.space/api/v0.1/countries/population/cities')
        response.raise_for_status()
        data = response.json()
        return [city['city'] for city in data['data']]
    except Exception as e:
        raise RuntimeError(f"无法获取城市列表: {e}")

def get_weather(city, api_key):
    """
    根据城市名称获取天气信息
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        return {
            'temperature': weather_data['main']['temp'],
            'description': weather_data['weather'][0]['description'],
            'humidity': weather_data['main']['humidity'],
            'wind_speed': weather_data['wind']['speed']
        }
    except Exception as e:
        raise RuntimeError(f"无法获取天气信息: {e}")

def get_location_data():
    """
    获取地理信息并返回字典
    """
    response = requests.get('https://ipinfo.io/json')
    if response.status_code == 200:
        return response.json()
    else:
        return {'error': f"Error {response.status_code}: {response.reason}"}

def get_city(location_data):
    """
    从地理信息中提取城市
    """
    return location_data.get('city', '未知城市')

def get_weather_by_location(api_key):
    """
    根据当前 IP 获取位置并获取天气
    """
    location_data = get_location_data()
    if 'error' in location_data:
        return {'error': "无法获取位置信息"}
    city = get_city(location_data)
    return get_weather(city, api_key)



def get_dynamic_city_list():
    """
    获取城市列表的业务逻辑
    """
    try:
        return fetch_city_list()
    except RuntimeError as e:
        print(f"错误: {e}")
        # 如果 API 请求失败，提供备用城市列表
        return ["北京", "上海", "广州", "深圳"]

def get_weather_for_city(city):
    """
    获取指定城市的天气信息
    """
    try:
        return get_weather(city, API_KEY)
    except RuntimeError as e:
        print(f"错误: {e}")
        return {"error": str(e)}


 