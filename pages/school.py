import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 로그인 상태 확인
if "ID" not in st.session_state or st.session_state["ID"] == "None":
    st.warning("로그인이 필요합니다. 로그인 페이지로 이동하세요.")
    st.stop()  # 페이지 렌더링 중단

data = pd.read_csv("학생현황.csv")

if "ID" not in st.session_state:
    st.session_state["ID"] = "None"

ID = st.session_state["ID"]

with st.sidebar:
    st.caption(f'{ID}님 접속중')
        # 로그아웃 버튼
    if st.button("로그아웃"):
        st.session_state["ID"] = "None"  # 로그인 상태 초기화
        st.write("로그아웃 되었습니다. 새로고침하여 로그인 페이지로 돌아가세요.")
        st.stop()  # 페이지 렌더링 중단
    
with st.form("input"):
    region = st.multiselect("지역", data['Region'].unique())
    gender = st.multiselect("성별", data['Gender'].unique())
    school = st.multiselect("학교", data['School'].unique())
    submitted = st.form_submit_button("조회")
    
    if submitted:
        name_list = []
        result = data["Year"].drop_duplicates().sort_values().reset_index(drop=True)
        for re in region:
            for ge in gender:
                for sc in school:
                    name = f"{re}_{ge}_{sc}"
                    name_list.append(name)
                    selected_df = data[(data['Region'] == re) & (data['Gender'] == ge)& (data['School'] == sc)]
                    selected_df = selected_df[["Year","Students"]].rename(columns={"Students": name})
                    result = pd.merge(result, selected_df, on='Year').sort_values('Year')
        
        st.line_chart(data=result, x='Year', y=name_list,use_container_width=True)
        