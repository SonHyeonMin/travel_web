import requests
import json
import random
import streamlit as st
import streamlit.components.v1 as components

# Kakao API 키 설정
API_KEY = "33f096a2efdfcbf38c71025a4926325c"  # 본인의 Kakao API 키로 변경

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
            lon = float(document['x'])  # 경도
            lat = float(document['y'])  # 위도
            return lon, lat
        else:
            st.error("해당 주소에 대한 좌표를 찾을 수 없습니다.")
            return None, None

    except requests.exceptions.RequestException as e:
        st.error(f"API 요청 중 오류가 발생했습니다: {e}")
        return None, None

# Streamlit 애플리케이션 시작
st.title('여행 코스 지도')

# 사용자로부터 여행지를 입력받음
destination = st.text_input('여행지를 입력하세요 (예: 대구)')

# 사용자가 '대구'를 입력했을 때만 JSON 파일에서 데이터를 필터링하고 지도를 표시
if destination.strip() == "대구":
    # JSON 파일 열기
    try:
        with open("response_1723079876538.json", "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        st.error("JSON 파일을 찾을 수 없습니다.")
        data = {}

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
            st.write(f"Store Name: {b_store_name}")
            st.write(f"Store Address: {b_store_address}")

            # 주소를 경도와 위도로 변환
            lon, lat = get_lat_lon(b_store_address)
            if lon and lat:
                st.write(f"Latitude: {lat}, Longitude: {lon}")
            else:
                st.stop()  # 좌표를 찾지 못하면 이후 코드 실행 중지
        else:
            st.error("조건에 맞는 항목이 없습니다.")
            st.stop()

    except (AttributeError, TypeError, KeyError) as e:
        st.error("데이터를 처리하는 동안 오류가 발생했습니다.")
        st.error(f"오류: {e}")
        st.stop()

    # Streamlit의 세션 상태를 이용해 지도 중심좌표를 저장합니다.
    if "center" not in st.session_state:
        st.session_state["center"] = (lat, lon)  # 추출한 초기 좌표 설정

    # 중심 좌표를 설정하는 함수
    def set_center(new_lat, new_lon):
        st.session_state["center"] = (new_lat, new_lon)

    # 중심 좌표를 부드럽게 이동시키는 함수
    def pan_to(new_lat, new_lon):
        st.session_state["center"] = (new_lat, new_lon)

    # HTML 및 JavaScript 코드를 문자열로 정의합니다.
    html_code = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>지도 이동시키기</title>
    </head>
    <body>
    <div id="map" style="width:100%;height:350px;"></div>

    <script type="text/javascript" src="//dapi.kakao.com/v2/maps/sdk.js?appkey=8c4f8f64bbdce79f14f3831edc0c898b"></script>
    <script>
    var mapContainer = document.getElementById('map'), // 지도를 표시할 div 
        mapOption = {{ 
            center: new kakao.maps.LatLng({st.session_state["center"][0]}, {st.session_state["center"][1]}), // 지도의 중심좌표
            level: 3 // 지도의 확대 레벨
        }};

    var map = new kakao.maps.Map(mapContainer, mapOption); // 지도를 생성합니다

    // 마커와 인포윈도우의 정보를 담은 배열
    var positions = [
        {{
            content: '<div style="padding:5px;">{b_store_name} <a href="https://map.kakao.com/link/to/{b_store_name},{lat},{lon}" style="color:blue" target="_blank">길찾기</a></div>', // 인포윈도우에 표출될 내용
            iwRemoveable: true, // 인포윈도우 제거 가능
            latlng: new kakao.maps.LatLng({lat}, {lon})  // 추출한 좌표값으로 마커 설정
        }}
    ];

    for (var i = 0; i < positions.length; i++) {{
        // 마커를 생성합니다
        var marker = new kakao.maps.Marker({{
            map: map, // 마커를 표시할 지도
            position: positions[i].latlng // 마커의 위치
        }});

        // 마커에 표시할 인포윈도우를 생성합니다 
        var infowindow = new kakao.maps.InfoWindow({{
            content: positions[i].content, // 인포윈도우에 표시할 내용
            removable: positions[i].iwRemoveable // 인포윈도우 제거 가능 여부
        }});

        // 마커에 mouseover 이벤트와 mouseout 이벤트를 등록합니다
        kakao.maps.event.addListener(marker, 'mouseover', makeOverListener(map, marker, infowindow));
        kakao.maps.event.addListener(marker, 'mouseout', makeOutListener(infowindow));
    }}

    // 인포윈도우를 표시하는 클로저를 만드는 함수입니다 
    function makeOverListener(map, marker, infowindow) {{
        return function() {{
            infowindow.open(map, marker);
        }};
    }}

    // 인포윈도우를 닫는 클로저를 만드는 함수입니다 
    function makeOutListener(infowindow) {{
        return function() {{
            infowindow.close();
        }};
    }}
    </script>
    </body>
    </html>
    """

    # HTML을 삽입하여 지도를 표시합니다.
    components.html(html_code, height=400)

else:
    st.write("대구 외의 여행지에 대한 정보는 제공하지 않습니다.")
