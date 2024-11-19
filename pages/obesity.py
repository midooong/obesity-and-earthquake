import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import rc

# 한글 폰트 설정
rc('font', family='NanumGothic')  # Linux 환경
# rc('font', family='Malgun Gothic')  # Windows 환경
# rc('font', family='AppleGothic')  # Mac 환경
plt.rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨짐 방지

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
file_path = 'obesity.csv'
data = pd.read_csv(file_path, encoding='UTF-8-SIG')

# 데이터 정리
# 첫 번째 행을 열 이름으로 설정
data.columns = data.iloc[0]
data = data[1:].reset_index(drop=True)

# "구분1", "구분2" 값 제거
data = data[(data["구분1"] != "구분1") & (data["구분2"] != "구분2")]

# Unnamed 열 제거
data = data.loc[:, ~data.columns.str.contains('Unnamed')]

# 열 이름 재구성
data.columns = ["구분1", "구분2"] + [f"{year}_{gender}" for year in range(2009, 2023) for gender in ["전체", "남자", "여자"]]

# 연도별 데이터를 숫자로 변환
for col in data.columns[2:]:
    data[col] = pd.to_numeric(data[col], errors='coerce')

# 데이터 확인
st.write("정리된 데이터 미리보기:")
st.dataframe(data.head())

# Streamlit 앱
st.title("비만율 데이터 시각화")

# 사용자 입력: 구분1, 구분2 선택
selected_category1 = st.sidebar.selectbox("구분1 선택:", sorted(data["구분1"].unique()))
filtered_data1 = data[data["구분1"] == selected_category1]

selected_category2 = st.sidebar.selectbox("구분2 선택:", sorted(filtered_data1["구분2"].unique()))
filtered_data2 = filtered_data1[filtered_data1["구분2"] == selected_category2]

# 성별 선택
selected_gender = st.sidebar.radio("성별 선택:", ["전체", "남자", "여자"])

# 데이터 필터링
columns_to_plot = [col for col in data.columns if selected_gender in col]
plot_data = filtered_data2[columns_to_plot].transpose()
plot_data.index = [int(col.split("_")[0]) for col in plot_data.index]  # 연도 추출
plot_data.columns = [selected_category2]

# 데이터 확인
st.write("필터링된 데이터 미리보기:")
st.dataframe(plot_data)

# 꺾은선 그래프
st.subheader(f"{selected_category1} - {selected_category2} ({selected_gender})")
if not plot_data.empty:
    fig, ax = plt.subplots(figsize=(10, 6))
    plot_data.plot(ax=ax, marker='o')
    ax.set_title(f"{selected_category1} - {selected_category2} 데이터 ({selected_gender})")
    ax.set_xlabel("연도")
    ax.set_ylabel("비만율 (%)")
    ax.legend(title="구분")
    st.pyplot(fig)
else:
    st.warning("선택한 조건에 해당하는 데이터가 없습니다.")
