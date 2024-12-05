import requests

# 获取地理信息
def get_location():
    response = requests.get('https://ipinfo.io/json')
    if response.status_code == 200:
        data = response.json()
        return {
            'city': data.get('city'),
            'region': data.get('region'),
            'country': data.get('country'),
            'loc': data.get('loc')  # 经纬度，格式为 "纬度,经度"
        }
    else:
        return {'error': f"Error {response.status_code}: {response.reason}"}

def get_city():
    response = requests.get('https://ipinfo.io/json')
    if response.status_code == 200:
        data = response.json()
        return data.get('city'),
        
        
    else:
        return {'error': f"Error {response.status_code}: {response.reason}"}
# 示例调用
if __name__ == "__main__":
    location = get_location()
    if 'error' not in location:
        print(f"城市: {location['city']}")
        print(f"地区: {location['region']}")
        print(f"国家: {location['country']}")
        print(f"经纬度: {location['loc']}")
    else:
        print(location['error'])
