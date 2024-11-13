import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import holidays
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.graphics.tsaplots import month_plot, quarter_plot, plot_acf
from sklearn.preprocessing import MinMaxScaler

df = pd.read_csv('../data/raw/box_office.csv')
                                                                                                # Verilerin İşlenmesi

# URL Sütununun Kaldırılması ve Eksik Verilerin Doldurulması

processed_df = df.drop('url', axis=1)
processed_df['total_gross'] = processed_df['total_gross'].interpolate(method='linear')
processed_df['total_gross'] = processed_df['total_gross'].astype(int)

# Zaman Serisi için İndeks Seçimi

processed_df['date'] = pd.to_datetime(processed_df['date'], format='%Y-%m-%d')
processed_df.set_index('date', inplace=True)
processed_df = processed_df.sort_index()

# Zaman Değişkenlerinin Eklenmesi

processed_df['year'] = processed_df.index.year
processed_df['month'] = processed_df.index.month
processed_df['day_of_month'] = processed_df.index.day
processed_df['weekday'] = processed_df.index.weekday
processed_df['is_weekend'] = processed_df.index.weekday > 4
processed_df['quarter'] = ((processed_df.index.month - 1) // 3) + 1
processed_df.head()

                                                                                                # Zaman Serisinin Yeniden Örneklenmesi

# Günlük Toplam Hasılat Sütununun Yeniden Örneklenmesi

weekly_resample = processed_df['total_gross'].resample('W').mean()
monthly_resample = processed_df['total_gross'].resample('ME').mean()
quarterly_resample = processed_df['total_gross'].resample('QE').mean()
yearly_resample = processed_df['total_gross'].resample('YE').mean()

# Yıllık, Çeyreklik, Aylık ve Haftalık Ortalama Hasılat Grafiği

plt.figure(figsize=(10, 5))
plt.plot(weekly_resample.index, weekly_resample.values, label='Haftalık Ortalama Hasılat', linestyle='--', marker='x', color='black')
plt.plot(monthly_resample.index, monthly_resample.values, label='Aylık Ortalama Hasılat', marker='o', color='red')
plt.plot(quarterly_resample.index, quarterly_resample.values, label='Çeyreklik Ortalama Hasılat', linestyle='-.', marker='D', color='lightgreen')
plt.plot(yearly_resample.index, yearly_resample.values, label='Yıllık Ortalama Hasılat', linestyle='-.', marker='o', color='yellow')
plt.plot(processed_df.index, processed_df['total_gross'], label='Orijinal Günlük Değerler', linestyle='', marker='x', color='blue', alpha=0.09)
plt.title('Yıllık, Çeyreklik, Aylık ve Haftalık Ortalama Hasılat')
plt.xlabel('Tarihler')
plt.ylabel('Hasılat')
plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.ticklabel_format(style='plain', axis='y')

# Sayısal Değerlerden Oluşan Aşağı Örnekleme Uygulanmış Veri Setleri Oluşturma ve Csv Dosyası Olarak Kaydetme

numeric_df = processed_df.select_dtypes(include='number')
columns_to_drop = ['year', 'month', 'day_of_month', 'quarter', 'weekday', 'day_of_year']
numeric_df = numeric_df.drop(columns=columns_to_drop)
df_weekly = numeric_df.resample('W').mean()
df_monthly = numeric_df.resample('ME').mean()
df_quarterly = numeric_df.resample('QE').mean()
df_yearly = numeric_df.resample('YE').mean()
df_weekly.to_csv('../data/resampled/weekly_box_office.csv')
df_monthly.to_csv('../data/resampled/monthly_box_office.csv')
df_quarterly.to_csv('../data/resampled/quarterly_box_office.csv')
df_yearly.to_csv('../data/resampled/yearly_box_office.csv')

                                                                                                # Zaman Serisinin Trend ve Mevsimsellik Bileşenlerine Ayrıştırılması
# Aylık ve Çeyreklik Mevsimsellik Grafikleri

fig, axes = plt.subplots(1, 2, figsize=(10, 5))
month_plot(monthly_resample, ax=axes[0])
axes[0].set_xlabel('Aylar')
axes[0].set_ylabel('Hasılat')
axes[0].set_title('Aylık Mevsimsellik Grafiği')
quarter_plot(quarterly_resample, ax=axes[1])
axes[1].set_xlabel('Çeyreklikler')
axes[1].set_ylabel('Hasılat')
axes[1].set_title('Çeyreklik Mevsimsellik Grafiği')

# Verinin Trend ve Mevsimsellik Bileşenlerine Ayrıştırılması

decomposition = seasonal_decompose(processed_df['total_gross'], model='multiplicative', period=365)
fig = decomposition.plot()
fig.set_size_inches(10, 5)

                                                                                                # Otokorelasyon

# 30 Gecikmeli Otokorelasyon Grafiği
plot_acf(processed_df['total_gross'], lags=30)
plt.xticks(range(0, 31, 1))
plt.grid(True)

                                                                                                # Özellik Mühendisliği

# Yeni Sütunların Eklenmesi

# 7 Günlük Gecikmeli Değer
processed_df['total_gross_lag7'] = processed_df['total_gross'].shift(7).bfill()
# Hareketli Ortalamalar
processed_df['7_day_rolling_total'] = processed_df['total_gross'].rolling(window = 7).mean()
processed_df['30_day_rolling_total'] = processed_df['total_gross'].rolling(window = 30).mean()
# Günlük Getiri
processed_df['daily_returns'] = processed_df['total_gross'].pct_change(fill_method=None) * 100
# Tatiller
holidays = holidays.US()
processed_df['is_holiday'] = processed_df.index.to_series().apply(lambda x: x in holidays)
# 7 ve 30 günlük hareketli ortalamalardaki sütunlar sırasıyla ilk 7 ve ilk 30 günün değerlerini hesaplamaz.
# Günlük getiri sütunu ilk günün, haftalık getiri sütunu ilk 7 günün değerini hesaplamaz.
# Bu yüzden backward fill kullanıyoruz:
processed_df['7_day_rolling_total'] = processed_df['7_day_rolling_total'].bfill()
processed_df['30_day_rolling_total'] = processed_df['30_day_rolling_total'].bfill()
processed_df['daily_returns'] = processed_df['daily_returns'].bfill()

# Döngüsel Verilerin İşlenmesi ve Tür Dönüşümleri

# Haftanın günleri
processed_df['weekday_sin'] = np.sin(2 * np.pi * processed_df['weekday'] / 7)
processed_df['weekday_cos'] = np.cos(2 * np.pi * processed_df['weekday'] / 7)
# Aylar
processed_df['month_sin'] = np.sin(2 * np.pi * processed_df['month'] / 12)
processed_df['month_cos'] = np.cos(2 * np.pi * processed_df['month'] / 12)
# Çeyreklikler
processed_df['quarter_sin'] = np.sin(2 * np.pi * processed_df['quarter'] / 4)
processed_df['quarter_cos'] = np.cos(2 * np.pi * processed_df['quarter'] / 4)
# Yılın günleri
processed_df['day_of_year_sin'] = np.sin(2 * np.pi * processed_df['day_of_year'] / 365.25)
processed_df['day_of_year_cos'] = np.cos(2 * np.pi * processed_df['day_of_year'] / 365.25)
# Boolean değişkenler
processed_df['is_holiday'] = processed_df['is_holiday'].astype(int)
processed_df['is_weekend'] = processed_df['is_weekend'].astype(int)

# Kullanılmayacak Sütunların Silinmesi

processed_df = processed_df.drop(columns=['top_1_release', 'weekday', 'month', 'quarter'])

# Veri Setini Dönemlere Ayırma

pandemic_start = pd.to_datetime('2020-03-12')
pandemic_end = pd.to_datetime('2021-06-14')
post_pandemic_start = pd.to_datetime('2021-06-15')
# Pandemi öncesi
pre_pandemic_df = processed_df[processed_df.index < pandemic_start]
# Pandemi dönemi
pandemic_df = processed_df[(processed_df.index >= pandemic_start) & (processed_df.index <= pandemic_end)]
# Pandemi sonrası
post_pandemic_df = processed_df[processed_df.index >= post_pandemic_start]
# is_pandemic Sütununun Eklenmesi
processed_df['is_pandemic'] = ((processed_df.index >= pandemic_start) & (processed_df.index <= pandemic_end)).astype(int)

                                                                                                # Normalizasyon

columns_to_normalize = ['top_1_gross', 'top_10_gross', 'total_gross',
                        '7_day_rolling_total', '30_day_rolling_total',
                        'total_gross_lag7']
normalized_processed_df = processed_df.copy()
scaler = MinMaxScaler()
normalized_processed_df[columns_to_normalize] = scaler.fit_transform(processed_df[columns_to_normalize])

                                                                                                # Yeni Veri Setlerinin Kaydedilmesi

data_path = '../data/processed/processed.csv'
processed_df.to_csv(data_path, index=True)

data_path = '../data/processed/normalized_processed.csv'
normalized_processed_df.to_csv(data_path, index=True)

data_path = '../data/processed/pre_pandemic.csv'
pre_pandemic_df.to_csv(data_path, index=True)

data_path = '../data/processed/pandemic.csv'
pandemic_df.to_csv(data_path, index=True)

data_path = '../data/processed/post_pandemic.csv'
post_pandemic_df.to_csv(data_path, index=True)

plt.show()