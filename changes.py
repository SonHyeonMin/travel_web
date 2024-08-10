from geopy.geocoders import Nominatim

def get_lat_lon(address):
    # Nominatim 지오코더 객체 생성
    geolocator = Nominatim(user_agent="geoapiExercises")
    
    # 주소를 위도와 경도로 변환
    location = geolocator.geocode(address)
    
    # 위도와 경도 반환
    if location:
        return location.latitude, location.longitude
    else:
        return None

# 예시 주소
address = "동구 망양로 659-2"
coordinates = get_lat_lon(address)

if coordinates:
    print(f"Latitude: {coordinates[0]}, Longitude: {coordinates[1]}")
else:
    print("Location not found.")
