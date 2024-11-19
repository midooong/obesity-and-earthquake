import streamlit as st
import pandas as pd

# 로그인 상태 확인
if "ID" not in st.session_state or st.session_state["ID"] == "None":
    st.warning("로그인이 필요합니다. 로그인 페이지로 이동하세요.")
    st.stop()  # 페이지 렌더링 중단

# 로그인된 사용자만 볼 수 있는 콘텐츠
ID = st.session_state["ID"]

with st.sidebar:
    st.caption(f'{ID}님 접속 중')

    # 로그아웃 버튼
    if st.button("로그아웃"):
        st.session_state["ID"] = "None"  # 로그인 상태 초기화
        st.write("로그아웃 되었습니다. 새로고침하여 로그인 페이지로 돌아가세요.")
        st.stop()  # 페이지 렌더링 중단

# 데이터 로드 및 처리
data = pd.read_csv("공공자전거.csv")

st.title('공공자전거 어디있지?')

data = data.copy().fillna(0)
data.loc[:, 'size'] = 5 * (data['LCD'] + data['QR'])
data

color = {'QR': '#37eb91',
         'LCD': '#ebbb37'}
data.loc[:, 'color'] = data.copy().loc[:, '운영방식'].map(color)

st.map(data, latitude="위도",
       longitude="경도",
       size="size",
       color="color")
