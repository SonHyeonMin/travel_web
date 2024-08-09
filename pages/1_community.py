import streamlit as st

# 제목 설정
st.title("공유 커뮤니티")

# 로그인 상태 확인
if 'email' not in st.session_state:
    st.error("로그인 후 사용 가능합니다.")
else:
    # 로그인한 이메일 표시
    email = st.session_state.email

    # 세션 상태에 저장된 텍스트 초기화
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # 추가 텍스트 입력받기
    additional_text = st.text_input("각자의 생각을 자유롭게 나눠보세요")

    # 입력한 텍스트를 리스트에 추가
    if additional_text:
        st.session_state.messages.append(f"{email}: {additional_text}")

    # 입력된 모든 메시지를 화면에 표시
    for message in st.session_state.messages:
        st.write(message)
