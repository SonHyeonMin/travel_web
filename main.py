import streamlit as st
from firebase_admin import firestore, credentials
import firebase_admin
import time

# Firebase Admin SDK 초기화
cred = credentials.Certificate('secret_sw.json')
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Firestore 클라이언트 초기화
db = firestore.client()

def get_user_data(email):
    user_ref = db.collection('users').document(email)
    doc = user_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None

def add_user(email, password):
    user_ref = db.collection('users').document(email)
    user_ref.set({'password': password})

def login(email, password):
    user_data = get_user_data(email)
    if user_data and user_data.get('password') == password:
        return True
    return False

if 'show_register' not in st.session_state:
    st.session_state.show_register = False

if 'message' not in st.session_state:
    st.session_state.message = None

# Function to clear text inputs
def clear_inputs():
    st.session_state.login_email = ""
    st.session_state.login_password = ""
    st.session_state.register_email = ""
    st.session_state.register_password = ""

st.title("느린 여행")
st.write("저희 느린 여행 홈페이지를 방문해 주셔서 감사합니다.")
st.write("느린 여행은 휠체어 사용자를 위한 맞춤형 여행 계획을 제공하는 사이트로")
st.write("로그인 후 이용이 가능합니다")

# Display message if available
if st.session_state.message:
    st.success(st.session_state.message)
    time.sleep(3)  # Wait for 3 seconds
    st.session_state.message = None
    clear_inputs()  # Clear all inputs after message display
    st.experimental_rerun()  # Refresh page

# Login Form
if not st.session_state.message:
    st.subheader("로그인")
    email = st.text_input("이메일", key="login_email")
    password = st.text_input("비밀번호", type="password", key="login_password")

    if st.button("로그인하기"):
        if login(email, password):
            st.session_state.email = email
            st.session_state.message = "로그인 성공!"
            st.experimental_rerun()  # 로그인 후 페이지 새로고침
        else:
            st.error("잘못된 자격 증명입니다")

    if st.button("회원가입"):
        st.session_state.show_register = True

# Registration Form
if st.session_state.show_register and not st.session_state.message:
    st.subheader("회원가입")
    register_email = st.text_input("이메일 (회원가입용)", key="register_email")
    register_password = st.text_input("비밀번호 (회원가입용)", type="password", key="register_password")

    if st.button("회원가입 확인"):
        if register_email and register_password:
            add_user(register_email, register_password)
            st.session_state.message = "회원가입 성공!"
            st.experimental_rerun()  # 페이지 새로고침
        else:
            st.error("이메일과 비밀번호를 입력하세요")
