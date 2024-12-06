import requests

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

# 示例调用
if __name__ == "__main__":
    location_data = get_location_data()
    if 'error' not in location_data:
        city = get_city(location_data)
        print(f"城市: {city}")
    else:
        print(location_data['error'])

