import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import month_plot, quarter_plot, plot_acf
from statsmodels.tsa.seasonal import seasonal_decompose

def plot_revenue_averages(df):
    weekly_average = df['total_gross'].resample('W').mean()
    monthly_average = df['total_gross'].resample('ME').mean()
    quarterly_average = df['total_gross'].resample('QE').mean()
    yearly_average = df['total_gross'].resample('YE').mean()
    plt.figure(figsize=(12, 6))
    plt.plot(df['total_gross'], label='Orijinal Günlük Değerler', color='blue', alpha=0.5)
    plt.plot(weekly_average, label='Haftalık Ortalama', color='black')
    plt.plot(monthly_average, label='Aylık Ortalama', color='red')
    plt.plot(quarterly_average, label='Çeyreklik Ortalama', color='lightgreen')
    plt.plot(yearly_average, label='Yıllık Ortalama', color='yellow')
    plt.title('Yıllık, Çeyreklik, Aylık ve Haftalık Ortalama Hasılat')
    plt.xlabel('Tarihler')
    plt.ylabel('Hasılat')
    plt.legend()
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.ticklabel_format(style='plain', axis='y')
    plt.show()

def plot_seasonality(df):
    monthly_average = df['total_gross'].resample('ME').mean()
    quarterly_average = df['total_gross'].resample('QE').mean()
    fig, axes = plt.subplots(1, 2, figsize=(12, 6))
    month_plot(monthly_average, ax=axes[0])
    axes[0].set_xlabel('Aylar')
    axes[0].set_ylabel('Hasılat')
    axes[0].set_title('Aylık Mevsimsellik Grafiği')
    quarter_plot(quarterly_average, ax=axes[1])
    axes[1].set_xlabel('Çeyrekler')
    axes[1].set_ylabel('Hasılat')
    axes[1].set_title('Çeyreklik Mevsimsellik Grafiği')
    plt.show()

def plot_decomposition(df):
    decomposition = seasonal_decompose(df['total_gross'], model='multiplicative', period=365)
    fig = decomposition.plot()
    fig.set_size_inches(12, 6)
    plt.show()

def plot_acf_graph(df):
    plt.figure(figsize=(10, 6))
    plot_acf(df['total_gross'], lags=30)
    plt.grid(True)
    plt.xticks(range(0, 31, 1))
    plt.show()
