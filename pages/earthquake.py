import streamlit as st
import pandas as pd
import pydeck as pdk

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


# 데이터 로드
data = pd.read_csv("IEB_export.csv")

# Streamlit 제목
st.title("지진 발생 위치 데이터 시각화")

# 중간 제목
st.header("전체 지진 데이터")

# 데이터 정리
data = data.rename(columns={
    "위도": "latitude",
    "경도": "longitude",
    "규모": "magnitude",
    "깊이": "depth"
})

# 규모에 따라 색상 및 크기 설정
data["color"] = data["magnitude"].apply(lambda x: [255, 0, 0] if x > 5 else [0, 0, 255])

# 반경을 크게 확대 (배율 조정)
data["radius"] = data["magnitude"] * 5000  # 반경 크기를 5배로 확대

# Pydeck 지도 설정
layer = pdk.Layer(
    "ScatterplotLayer",
    data=data,
    get_position=["longitude", "latitude"],
    get_fill_color="color",
    get_radius="radius",
    pickable=True
)

view_state = pdk.ViewState(
    latitude=data["latitude"].mean(),
    longitude=data["longitude"].mean(),
    zoom=5,
    pitch=0
)

# 지도 렌더링
st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# 데이터 테이블 표시
st.write("데이터 미리보기:")
st.dataframe(data.head())

# 데이터 테이블 보기 버튼
if "show_data" not in st.session_state:
    st.session_state["show_data"] = False

if st.button("모든 데이터 보기"):
    st.session_state["show_data"] = not st.session_state["show_data"]  # 상태 토글

if st.session_state["show_data"]:
    st.write("전체 데이터:")
    st.dataframe(data)
    
# 중간 제목
st.header("원하는 날짜의 지진 데이터 필터링")


# 데이터 정리: 열 이름 확인 및 수정
if "연" in data.columns and "월" in data.columns and "일" in data.columns:
    data = data.rename(columns={
        "연": "year",
        "월": "month",
        "일": "day",
        "위도": "latitude",
        "경도": "longitude",
        "규모": "magnitude",
        "깊이": "depth"
    })
else:
    st.error("필수 열(연, 월, 일)이 데이터에 없습니다. 데이터를 확인하세요.")
    st.stop()

# 결측값 제거
data = data.dropna(subset=["latitude", "longitude"])

# 규모에 따라 색상 및 크기 설정
data["color"] = data["magnitude"].apply(lambda x: [255, 0, 0] if x > 5 else [0, 0, 255])
data["radius"] = data["magnitude"] * 5000  # 반경 크기 확대

# 사용자 입력을 통해 날짜 필터링
st.sidebar.header("날짜 필터링")
selected_year = st.sidebar.selectbox("연도 선택", sorted(data["year"].unique()))
selected_month = st.sidebar.selectbox("월 선택", sorted(data[data["year"] == selected_year]["month"].unique()))
selected_day = st.sidebar.selectbox("일 선택", sorted(data[(data["year"] == selected_year) & (data["month"] == selected_month)]["day"].unique()))

# 데이터 필터링: 연도, 월, 일 기준
filtered_data = data[
    (data["year"] == selected_year) &
    (data["month"] == selected_month) &
    (data["day"] == selected_day)
]

# 필터링된 데이터가 없을 경우 처리
if filtered_data.empty:
    st.warning("선택한 날짜에 해당하는 데이터가 없습니다.")
else:
    # Pydeck 지도 설정
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=filtered_data,
        get_position=["longitude", "latitude"],
        get_fill_color="color",
        get_radius="radius",
        pickable=True
    )

    view_state = pdk.ViewState(
        latitude=filtered_data["latitude"].mean(),
        longitude=filtered_data["longitude"].mean(),
        zoom=5,
        pitch=0
    )

    # 지도 렌더링
    st.pydeck_chart(pdk.Deck(layers=[layer], initial_view_state=view_state))

# 데이터 테이블 표시
st.write("필터링된 데이터 미리보기:")
st.dataframe(filtered_data)