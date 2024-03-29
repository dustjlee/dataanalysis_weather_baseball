# -*- coding: utf-8 -*-
"""num_WL

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/17owkeqAaPLh4YzzC0nmjiETGSVkzgbad
"""

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


# 모든 월을 기준으로 '승'과 '패' 결과가 있는지 확인하여 없는 경우에는 0으로 채움
all_months = df_results['yyyymm'].unique()
monthly_wins = monthly_wins.reindex(all_months, fill_value=0)
monthly_losses = monthly_losses.reindex(all_months, fill_value=0)


# 그래프 그리기
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), sharex=True)

# 월별 '승' 막대 그래프
ax1.bar(monthly_wins.index.astype(str), monthly_wins, width=0.4, alpha=0.7, color='green', label='승')
ax1.set_ylabel('승 수')
ax1.set_title('월별 승과 패 그래프')

# 각 막대 위에 숫자로 승 표시
for rect in ax1.patches:
    height = rect.get_height()
    ax1.text(rect.get_x() + rect.get_width()/2, height, f'{int(height)}', ha='center', va='bottom')

# 월별 '패' 막대 그래프
ax2.bar(monthly_losses.index.astype(str), monthly_losses, width=0.4, alpha=0.7, color='red', label='패')
ax2.set_xlabel('월')
ax2.set_ylabel('패 수')

# 각 막대 위에 숫자로 패 표시
for rect in ax2.patches:
    height = rect.get_height()
    ax2.text(rect.get_x() + rect.get_width()/2, height, f'{int(height)}', ha='center', va='bottom')

plt.show()