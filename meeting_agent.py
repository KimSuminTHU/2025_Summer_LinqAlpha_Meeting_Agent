import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st

# 데이터 로드 함수
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    return df

# 주차별 회의 수 시각화 함수
def plot_meetings_per_week(df):
    df['week_number'] = df['start_time'].dt.isocalendar().week
    meetings_per_week = df.groupby('week_number').size()
    st.subheader('Number of Meetings per Week')
    st.bar_chart(meetings_per_week)

# 플랫폼별 회의 수 시각화 함수
def plot_platform_usage(df):
    platform_counts = df['platform'].value_counts()
    st.subheader('Platform Usage Distribution')
    st.bar_chart(platform_counts)

# 주차별 플랫폼별 회의 수 시각화 함수
def plot_meetings_per_week_platform(df):
    meetings_per_week_platform = df.groupby(['week_number', 'platform']).size().unstack().fillna(0)
    st.subheader('Meetings per Week by Platform')
    st.bar_chart(meetings_per_week_platform)

# 회의 지속 시간 분석 함수
def plot_meeting_duration(df):
    df['duration'] = (df['end_time'] - df['start_time']).dt.total_seconds() / 60  # 지속 시간(분)
    st.subheader('Meeting Duration Distribution (minutes)')
    fig, ax = plt.subplots()
    ax.hist(df['duration'], bins=20, color='skyblue')
    ax.set_title('Meeting Duration Distribution (minutes)')
    ax.set_xlabel('Duration (minutes)')
    ax.set_ylabel('Frequency')
    st.pyplot(fig)

# 회의 목록 시각화 함수 (start_time, platform, status 사용)
def plot_meeting_list(df):
    df_sorted = df.sort_values('start_time')
    st.subheader('Meeting List by Start Time and Status')
    fig = px.scatter(df_sorted, x='start_time', y='platform', color='status', title="Meeting List", labels={"start_time": "Meeting Start Time", "platform": "Platform"})
    st.plotly_chart(fig)

# 메인 함수
def main():
    st.title("Meeting Agent Dashboard")

    # 데이터 로드
    file_path = 'meeting_informations (1).csv'  # 파일 경로를 맞춰주세요
    df = load_data(file_path)

    # 시각화 함수 호출
    plot_meetings_per_week(df)
    plot_platform_usage(df)
    plot_meetings_per_week_platform(df)
    plot_meeting_duration(df)
    plot_meeting_list(df)

if __name__ == "__main__":
    main()
