import json
import random

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
    else:
        print("조건에 맞는 항목이 없습니다.")

except (AttributeError, TypeError, KeyError) as e:
    print("데이터를 처리하는 동안 오류가 발생했습니다.")
    print(f"오류: {e}")
