import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

# 데이터 로드 (여기서 파일 경로를 맞춰주세요)
df = pd.read_csv('meeting_informations (1).csv')

# start_time을 datetime으로 변환
df['start_time'] = pd.to_datetime(df['start_time'])

# 앱 제목
st.title("Meeting Agent Dashboard")

# 1. 주차별 회의 수 카운트
df['week_number'] = df['start_time'].dt.isocalendar().week
meetings_per_week = df.groupby('week_number').size()

# 주차별 회의 수 시각화
st.subheader('Number of Meetings per Week')
st.bar_chart(meetings_per_week)

# 2. 플랫폼별 회의 수 카운트
platform_counts = df['platform'].value_counts()

# 플랫폼 사용 시각화
st.subheader('Platform Usage Distribution')
st.bar_chart(platform_counts)

# 3. 주차별 플랫폼별 회의 수
meetings_per_week_platform = df.groupby(['week_number', 'platform']).size().unstack().fillna(0)

# 주차별 플랫폼별 회의 수 시각화
st.subheader('Meetings per Week by Platform')
st.bar_chart(meetings_per_week_platform)

# 4. 회의 지속 시간 분석
df['end_time'] = pd.to_datetime(df['end_time'])
df['duration'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 60  # 지속 시간(분)

# 회의 지속 시간 분포 시각화
st.subheader('Meeting Duration Distribution (minutes)')
fig, ax = plt.subplots()
ax.hist(df['duration'], bins=20, color='skyblue')
ax.set_title('Meeting Duration Distribution (minutes)')
ax.set_xlabel('Duration (minutes)')
ax.set_ylabel('Frequency')
st.pyplot(fig)

# 5. 회의 목록 (시작 시간 기준으로 정렬)
df_sorted = df.sort_values('start_time')

# 회의 목록 시각화 (Plotly 사용)
st.subheader('Meeting List')
fig = px.scatter(df_sorted, x='start_time', y='meeting_name', color='status', title="Meeting List", labels={"start_time": "Meeting Start Time", "meeting_name": "Meeting Name"})
st.plotly_chart(fig)
