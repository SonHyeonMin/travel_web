import requests
import json
import random

# Kakao API 키 설정
API_KEY = "33f096a2efdfcbf38c71025a4926325c"

def get_lat_lon(address):
    url = "https://dapi.kakao.com/v2/local/search/address.json"
    headers = {"Authorization": f"KakaoAK {API_KEY}"}
    params = {"query": address}

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
        result = response.json()

        if result['documents']:
            # 결과 중 첫 번째 항목의 경도 및 위도 반환
            document = result['documents'][0]
            lon = document['x']  # 경도
            lat = document['y']  # 위도
            return lon, lat
        else:
            print("해당 주소에 대한 좌표를 찾을 수 없습니다.")
            return None, None

    except requests.exceptions.RequestException as e:
        print(f"API 요청 중 오류가 발생했습니다: {e}")
        return None, None

# JSON 파일 열기
with open("response_1723079876538.json", "r", encoding="utf-8") as file:
    data = json.load(file)

try:
    items = data.get("response", {}).get("body", {}).get("items", {}).get("item", [])
    
    # 조건에 맞는 항목들만 필터링하여 리스트 생성
    filtered_items = [
        item for item in items 
        if item.get("dw_wheelchair_YN") == "Y" 
        and item.get("out_parking_YN") == "Y" 
        and item.get("dw_act_space_YN") == "Y"
    ]
    
    if filtered_items:
        # 랜덤하게 하나 선택
        selected_item = random.choice(filtered_items)
        b_store_name = selected_item.get("b_store_name")
        b_store_address = selected_item.get("b_store_address")
        print(f"Store Name: {b_store_name}")
        print(f"Store Address: {b_store_address}")

        # 주소를 경도와 위도로 변환
        lon, lat = get_lat_lon(b_store_address)
        if lon and lat:
            print(f"Latitude: {lat}, Longitude: {lon}")
    else:
        print("조건에 맞는 항목이 없습니다.")

except (AttributeError, TypeError, KeyError) as e:
    print("데이터를 처리하는 동안 오류가 발생했습니다.")
    print(f"오류: {e}")
