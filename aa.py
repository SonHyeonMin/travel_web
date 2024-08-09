import requests

# API 키 설정
API_KEY = 'your_kakao_api_key'  # 카카오 개발자 센터에서 발급받은 API 키
headers = {
    "Authorization": f"KakaoAK {API_KEY}"
}

# 장소 검색 예제: "카페" 검색
query = "카페"
url = "https://dapi.kakao.com/v2/local/search/keyword.json"
params = {
    "query": query,
    "size": 5  # 검색 결과의 개수를 지정할 수 있습니다.
}

response = requests.get(url, headers=headers, params=params)

# JSON 응답을 파싱
if response.status_code == 200:
    places = response.json()
    for place in places['documents']:
        print(f"Place Name: {place['place_name']}")
        print(f"Address: {place['address_name']}")
        print(f"Phone: {place['phone']}")
        print(f"URL: {place['place_url']}")
        print("----------")
else:
    print("Error:", response.status_code)

