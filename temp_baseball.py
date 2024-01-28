# -*- coding: utf-8 -*-
"""temp_baseball

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1y776K27lxCV0XHh4cpfRJ5UMDlVS31e2
"""

#최종기온
from google.colab import drive
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Google Drive 마운트
#drive.mount('/content/drive')
drive.mount("/content/drive", force_remount=True)
# 경로 설정
excel_path = "/content/drive/MyDrive/baseball_data.xlsx"
excel_path2 = "/content/drive/MyDrive/temperature_data.xlsx"

# 야구 데이터 로드 및 처리
df_results = pd.read_excel(excel_path, engine='openpyxl')
df_results.columns = ['날짜', '상대팀', '승패', '구장']
df_results['날짜'] = pd.to_datetime(df_results['날짜'])
df_results['yyyymm'] = df_results['날짜'].dt.strftime('%Y%m')  # 'yyyymm' 열 추가
df_results.set_index('날짜', inplace=True)

# 기온 데이터 로드 및 처리
df_weather = pd.read_excel(excel_path2, engine='openpyxl')
df_weather.columns = ['날짜', '구장', '기온', '강수량', '풍속', '상대습도']
df_weather['날짜'] = pd.to_datetime(df_weather['날짜'])
df_weather['yyyymm'] = df_weather['날짜'].dt.strftime('%Y%m')  # 'yyyymm' 열 추가
df_weather.set_index('날짜', inplace=True)

# 두 데이터프레임 Merge
df_merged = pd.merge(df_results, df_weather, on='날짜', how='inner')
print(df_merged)

# 월별 '승'과 '패' 합계 계산
monthly_wins = df_results[df_results['승패'] == '승'].groupby('yyyymm').size()
monthly_losses = df_results[df_results['승패'] == '패'].groupby('yyyymm').size()

print(monthly_wins)
print(monthly_losses)

# 월별 기온의 평균값 계산
monthly_avg_temperature = df_weather.groupby('yyyymm')['기온'].mean()   #풍속, 강수량, 기온 변경해서

print(monthly_avg_temperature)

# 그래프 그리기
fig, ax1 = plt.subplots(figsize=(16, 10))

# 월별 기온 dot 그래프
ax1.plot(monthly_avg_temperature.index.astype(str), monthly_avg_temperature.values, marker='o', color='blue', label='Monthly AVG Temp.')
ax1.set_xlabel('Month')
ax1.set_ylabel('Temp(°C)', color='blue')
ax1.tick_params('y', colors='blue')

# 막대 그래프를 위한 두 번째 y 축 생성
ax2 = ax1.twinx()


# 월별 '승'과 '패' 막대 그래프
bar1 = ax2.bar(monthly_wins.index.astype(str), monthly_wins, width=0.4, alpha=0.7, color='green', label='WIN')
bar2 = ax2.bar(monthly_losses.index.astype(str), monthly_losses, width=0.4, alpha=0.7, color='red', label='LOOSE')


# 각 막대 위에 숫자로 승과 패 표시
for rect in bar1:
   height = rect.get_height()
   ax2.text(rect.get_x() + rect.get_width()/2, height, f'{int(height)}', ha='center', va='bottom')

for rect in bar2:
   height = rect.get_height()
   ax2.text(rect.get_x() + rect.get_width()/2, height, f'{int(height)}', ha='center', va='bottom')


ax2.set_ylabel('Game Number', color='black')
ax2.tick_params('y', colors='black')

# 그래프 제목
plt.title('Montly AVG Temperature & Won-Loose Graph')

# 범례 표시
ax1.legend(loc='upper left')
ax2.legend(loc='upper right')

plt.show()