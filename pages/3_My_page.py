import streamlit as st

st.title("My Page")

if st.button("저장된 ai 여행 계획"):
    st.session_state.travel = True

    # 저장된 여행 계획 나오는 코드

if st.button("내 여행 선호도"):
    st.session_state.favor = True

    # 사용자가 주로 입력한 내용을 토대로 ai 추천 코스 생성되는 코드
    # ex) 


