import pandas as pd
#import plotly.graph_objects as go
import streamlit as st

# 데이터 로드 함수
def load_data(file_path):
    df = pd.read_csv(file_path)
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])
    
    # 5월 이후 데이터만 필터링
    df = df[df['start_time'].dt.month >= 5]
    
    return df

# 이동 평균 함수 (이동 평균을 적용하여 데이터를 부드럽게 만듦)
def apply_moving_average(data, window=3):
    return data.rolling(window=window, min_periods=1).mean()  # NaN을 최소한으로 처리

# 이동 평균 성장률 계산
def calculate_growth(ma_data):
    growth = (ma_data - ma_data.shift(1)) / ma_data.shift(1) * 100
    growth = growth.fillna(0)  # 첫 번째 값은 변화가 없으므로 0으로 설정
    return growth

# 일별 회의 수 시각화 함수 (7일 이동 평균 및 이동 평균 성장률)
def plot_meetings_per_day(df):
    df['day'] = df['start_time'].dt.date
    df = df[~df['start_time'].dt.weekday.isin([5, 6])]  # 주말 제외
    meetings_per_day = df.groupby(['day']).size().reset_index(name='meeting_count')

    # 0,1 값을 제외한 일별 회의 수 계산
    meetings_per_day = meetings_per_day[~meetings_per_day['meeting_count'].isin([0, 1])]

    # 7일 이동 평균 적용
    meetings_per_day['daily_count_ma'] = apply_moving_average(meetings_per_day['meeting_count'], window=7)
    # 7일 이동 평균 성장률 계산
    meetings_per_day['daily_count_ma_growth'] = calculate_growth(meetings_per_day['daily_count_ma'])

    # 시각화에 필요한 데이터 준비
    x_values = meetings_per_day['day']
    y_values_daily_count = meetings_per_day['meeting_count']
    y_values_daily_count_ma = meetings_per_day['daily_count_ma']
    y_values_daily_count_ma_growth = meetings_per_day['daily_count_ma_growth']

    fig = go.Figure()

    # Bar 그래프 (회의 수)
    fig.add_trace(go.Bar(
        x=x_values,
        y=y_values_daily_count,
        name="Daily Meetings",
        marker_color='rgba(58, 71, 80, 0.3)',  # 연한 회색
        hovertemplate="Day: %{x}<br>Meetings: %{y}<extra></extra>"
    ))

    # Line 그래프 (7일 이동 평균)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values_daily_count_ma,
        mode='lines+markers',
        name="7-Day Moving Average (Daily Count)",
        line=dict(color='rgba(169, 169, 169, 1)', width=2),  # 진한 그레이 색상
        hovertemplate="Day: %{x}<br>Daily Count (7-Day MA): %{y}<extra></extra>"
    ))

    # 7일 이동 평균 성장률 (Secondary Y Axis)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values_daily_count_ma_growth,
        mode='lines+markers',
        name="7-Day MA Growth",
        line=dict(color='rgba(255, 99, 71, 0.8)', width=2),  # 연한 빨강 색상
        hovertemplate="Day: %{x}<br>MA Growth: %{y}%<extra></extra>",
        yaxis="y2"  # 2nd y-axis에 적용
    ))

    fig.update_layout(
        title="Daily Meetings with 7-Day Moving Average and Growth",
        xaxis_title="Day",
        yaxis_title="Daily Meetings",
        yaxis2=dict(
            title="7-Day MA Growth (%)",
            overlaying="y",
            side="right",
            showgrid=False,
            zeroline=False
        ),
        hovermode="x unified",
        xaxis=dict(tickangle=-45)
    )

    st.plotly_chart(fig)

# 주별 회의 수 시각화 함수 (3주 이동 평균 및 이동 평균 성장률)
def plot_meetings_per_week(df):
    df['week_number'] = df['start_time'].dt.isocalendar().week
    df['year'] = df['start_time'].dt.year
    meetings_per_week = df.groupby(['year', 'week_number']).size().reset_index(name='meeting_count')

    # 3주 이동 평균 적용
    meetings_per_week['weekly_increase_ma'] = apply_moving_average(meetings_per_week['meeting_count'], window=3)
    # 3주 이동 평균 성장률 계산
    meetings_per_week['weekly_increase_ma_growth'] = calculate_growth(meetings_per_week['weekly_increase_ma'])

    x_values = meetings_per_week['week_number']
    y_values_weekly_increase = meetings_per_week['meeting_count']
    y_values_weekly_increase_ma = meetings_per_week['weekly_increase_ma']
    y_values_weekly_increase_ma_growth = meetings_per_week['weekly_increase_ma_growth']

    fig = go.Figure()

    # Bar 그래프 (회의 수)
    fig.add_trace(go.Bar(
        x=x_values,
        y=y_values_weekly_increase,
        name="Weekly Meetings",
        marker_color='rgba(58, 71, 80, 0.3)',  # 연한 회색
        hovertemplate="Week: %{x}<br>Meetings: %{y}<extra></extra>"
    ))

    # Line 그래프 (3주 이동 평균)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values_weekly_increase_ma,
        mode='lines+markers',
        name="3-Week Moving Average",
        line=dict(color='rgba(169, 169, 169, 1)', width=2),  # 진한 그레이 색상
        hovertemplate="Week: %{x}<br>Weekly Count (3-Week MA): %{y}<extra></extra>"
    ))

    # 3주 이동 평균 성장률 (Secondary Y Axis)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values_weekly_increase_ma_growth,
        mode='lines+markers',
        name="3-Week MA Growth",
        line=dict(color='rgba(255, 99, 71, 0.8)', width=2),  # 연한 빨강 색상
        hovertemplate="Week: %{x}<br>MA Growth: %{y}%<extra></extra>",
        yaxis="y2"  # 2nd y-axis에 적용
    ))

    fig.update_layout(
        title="Weekly Meetings with 3-Week Moving Average and Growth",
        xaxis_title="Week",
        yaxis_title="Weekly Meetings",
        yaxis2=dict(
            title="3-Week MA Growth (%)",
            overlaying="y",
            side="right",
            showgrid=False,
            zeroline=False
        ),
        hovermode="x unified",
        xaxis=dict(tickangle=-45)
    )

    st.plotly_chart(fig)

# 2주 단위 회의 수 시각화 함수 (3주 이동 평균 및 이동 평균 성장률)
def plot_meetings_per_biweekly(df):
    df['biweekly'] = (df['start_time'].dt.isocalendar().week // 2) + 1
    df['year'] = df['start_time'].dt.year
    meetings_per_biweekly = df.groupby(['year', 'biweekly']).size().reset_index(name='meeting_count')

    # 3주 이동 평균 적용
    meetings_per_biweekly['biweekly_increase_ma'] = apply_moving_average(meetings_per_biweekly['meeting_count'], window=3)
    # 3주 이동 평균 성장률 계산
    meetings_per_biweekly['biweekly_increase_ma_growth'] = calculate_growth(meetings_per_biweekly['biweekly_increase_ma'])

    x_values = meetings_per_biweekly['biweekly']
    y_values_biweekly_increase = meetings_per_biweekly['meeting_count']
    y_values_biweekly_increase_ma = meetings_per_biweekly['biweekly_increase_ma']
    y_values_biweekly_increase_ma_growth = meetings_per_biweekly['biweekly_increase_ma_growth']

    fig = go.Figure()

    # Bar 그래프 (회의 수)
    fig.add_trace(go.Bar(
        x=x_values,
        y=y_values_biweekly_increase,
        name="Biweekly Meetings",
        marker_color='rgba(58, 71, 80, 0.3)',  # 연한 회색
        hovertemplate="2-Week: %{x}<br>Meetings: %{y}<extra></extra>"
    ))

    # Line 그래프 (3주 이동 평균)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values_biweekly_increase_ma,
        mode='lines+markers',
        name="3-Biweekly Moving Average",
        line=dict(color='rgba(169, 169, 169, 1)', width=2),  # 진한 그레이 색상
        hovertemplate="2-Week: %{x}<br>Biweekly Count (3-Biweekly MA): %{y}<extra></extra>"
    ))

    # 3주 이동 평균 성장률 (Secondary Y Axis)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values_biweekly_increase_ma_growth,
        mode='lines+markers',
        name="3-Biweekly MA Growth",
        line=dict(color='rgba(255, 99, 71, 0.8)', width=2),  # 연한 빨강 색상
        hovertemplate="2-Week: %{x}<br>MA Growth: %{y}%<extra></extra>",
        yaxis="y2"  # 2nd y-axis에 적용
    ))

    fig.update_layout(
        title="Biweekly Meetings with 3-Biweekly Moving Average and Growth",
        xaxis_title="2-Week Period",
        yaxis_title="Biweekly Meetings",
        yaxis2=dict(
            title="3-Biweekly MA Growth (%)",
            overlaying="y",
            side="right",
            showgrid=False,
            zeroline=False
        ),
        hovermode="x unified",
        xaxis=dict(tickangle=-45)
    )

    st.plotly_chart(fig)

# 월별 회의 수 시각화 함수 (3개월 이동 평균 및 이동 평균 성장률)
def plot_meetings_per_month(df):
    df['month'] = df['start_time'].dt.to_period('M')
    meetings_per_month = df.groupby(['month']).size().reset_index(name='meeting_count')

    # 3개월 이동 평균 적용
    meetings_per_month['monthly_increase_ma'] = apply_moving_average(meetings_per_month['meeting_count'], window=3)
    # 3개월 이동 평균 성장률 계산
    meetings_per_month['monthly_increase_ma_growth'] = calculate_growth(meetings_per_month['monthly_increase_ma'])

    x_values = meetings_per_month['month'].astype(str)
    y_values_monthly_increase = meetings_per_month['meeting_count']
    y_values_monthly_increase_ma = meetings_per_month['monthly_increase_ma']
    y_values_monthly_increase_ma_growth = meetings_per_month['monthly_increase_ma_growth']

    fig = go.Figure()

    # Bar 그래프 (회의 수)
    fig.add_trace(go.Bar(
        x=x_values,
        y=y_values_monthly_increase,
        name="Monthly Meetings",
        marker_color='rgba(58, 71, 80, 0.3)',  # 연한 회색
        hovertemplate="Month: %{x}<br>Meetings: %{y}<extra></extra>"
    ))

    # Line 그래프 (3개월 이동 평균)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values_monthly_increase_ma,
        mode='lines+markers',
        name="3-Month Moving Average",
        line=dict(color='rgba(169, 169, 169, 1)', width=2),  # 진한 그레이 색상
        hovertemplate="Month: %{x}<br>Monthly Count (3-Month MA): %{y}<extra></extra>"
    ))

    # 3개월 이동 평균 성장률 (Secondary Y Axis)
    fig.add_trace(go.Scatter(
        x=x_values,
        y=y_values_monthly_increase_ma_growth,
        mode='lines+markers',
        name="3-Month MA Growth",
        line=dict(color='rgba(255, 99, 71, 0.8)', width=2),  # 연한 빨강 색상
        hovertemplate="Month: %{x}<br>MA Growth: %{y}%<extra></extra>",
        yaxis="y2"  # 2nd y-axis에 적용
    ))

    fig.update_layout(
        title="Monthly Meetings with 3-Month Moving Average and Growth",
        xaxis_title="Month",
        yaxis_title="Monthly Meetings",
        yaxis2=dict(
            title="3-Month MA Growth (%)",
            overlaying="y",
            side="right",
            showgrid=False,
            zeroline=False
        ),
        hovermode="x unified",
        xaxis=dict(tickangle=-45)
    )

    st.plotly_chart(fig)

# 메인 함수
def main():
    st.title("Meeting Agent Dashboard")

    # 데이터 로드
    file_path = 'meeting_informations (1).csv'  # 파일 경로를 맞춰주세요
    df = load_data(file_path)

    # 보기 옵션을 드롭다운으로 선택 (week -> biweekly -> month -> daily)
    view_option = st.selectbox("Select View Option", ['week', 'biweekly', 'month', 'daily'])

    # 시각화 함수 호출
    if view_option == 'week':
        plot_meetings_per_week(df)
    elif view_option == 'biweekly':
        plot_meetings_per_biweekly(df)
    elif view_option == 'month':
        plot_meetings_per_month(df)
    elif view_option == 'daily':
        plot_meetings_per_day(df)

if __name__ == "__main__":
    main()
