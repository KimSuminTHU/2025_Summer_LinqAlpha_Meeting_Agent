import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# 데이터 로드
df = pd.read_csv('meeting_informations (1).csv')

# Streamlit 대시보드 제목
st.title("미팅 에이전트 사용량 대시보드")

# 1. 회의 상태 분포 (성공/실패)
st.header("회의 상태 분포")
status_counts = df['status'].value_counts()
st.bar_chart(status_counts)

# 2. 플랫폼 사용 분포
st.header("플랫폼 사용 분포")
platform_counts = df['platform'].value_counts()
st.bar_chart(platform_counts)

# 3. 회의 시간 분석
st.header("회의 시간 분석")
df['start_time'] = pd.to_datetime(df['start_time'])
df['end_time'] = pd.to_datetime(df['end_time'])
df['duration'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 60  # 회의 시간(분)

# 시간 분포 차트
fig, ax = plt.subplots()
ax.hist(df['duration'], bins=20, color='skyblue')
ax.set_title('회의 지속 시간 분포 (분)')
ax.set_xlabel('시간 (분)')
ax.set_ylabel('빈도')
st.pyplot(fig)

# 4. 회의 리스트 (시간순으로 정렬)
st.header("회의 리스트")
df_sorted = df.sort_values('start_time')
st.dataframe(df_sorted[['meeting_name', 'start_time', 'end_time', 'platform', 'status']])

