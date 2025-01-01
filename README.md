# 🎞️ Gişe Verilerine Göre Hasılat Tahmini 🎞️ 

## Proje Hakkında
2009 – 2024 yılları arasındaki günlük gişe verileri Box Office Mojo web sitesinden toplanmıştır. Veri toplama süreci Python programlama dili kullanılarak; Selenium, BeautifulSoup4 ve Requests kütüphaneleri ile gerçekleştirilmiştir.

Veri ön işleme aşamasında eksik veriler tamamlanmış; zaman serisi verisi yeniden örneklenmiş ve trend ile mevsimsellik bileşenleri ayrıştırılmıştır. Ayrıca otokorelasyon analizi yapılmıştır. Bu adımların sonunda özellik mühendisliği sürecine geçilmiş ve yeni değişkenler eklenmiştir.
## Kullanılan Araç ve Teknolojiler 
* **Python:** Proje dili
* **PyCharm:** IDE
* **Selenium:** Web sitesindeki dinamik verilere erişim
* **Requests, BeautifulSoup4:** Statik sayfalara istek gönderme, HTML verisini parse etme ve verileri çekme
* **Pandas, NumPy:** Veri manipülasyonu ve analiz
* **Matplotlib, Seaborn:** Veri görselleştirme
* **Statsmodels, scikit-learn:** Zaman serisi analizi, hasılat verilerinin normalizasyonu
* **Jupyter Notebook:** Veri ön işleme, veri analizi ve görselleştirme için geliştirme ortamı

## Kurulum
* Projeyi klonlayın:

```
git clone https://github.com/miraygurbuz/Time-Series-Box-Office.git
```
* Gereksinimleri yükleyin:
```
pip install -r requirements.txt
```

## Kullanım
### 1. Veri Kazıma

* Çalışmakta olduğunuz tarayıcıya uygun sürücüyü `driver` klasöre eklemeniz gerekmektedir.

   * **Chrome için:** chromedriver dosyasını indirin ve `driver` klasörüne yerleştirin.

   * **Firefox için:** geckodriver dosyasını indirin ve  `driver` klasörüne yerleştirin.
  
> 🔔 **Not:** 🔔 Sürücüyü `driver` klasörüne ekledikten sonra `scraper` klasörü içindeki `settings.py` dosyasının `DRIVER_PATH` kısmını güncelleyerek sürücü yolunu (driver/chromedriver gibi) belirtin.

* `scraper.py` dosyasını çalıştırın:
```
python scraper/scraper.py
```

### 2. Veri Ön İşleme

#### Uygulanan Adımlar:
* Eksik Verilerin Doldurulması
* Zaman Değişkenlerinin Eklenmesi
* Zaman Serisinin Yeniden Örneklenmesi
* Zaman Serisinin Trend ve Mevsimsellik Bileşenlerine Ayrıştırılması
* Otokorelasyon
* Özellik Mühendisliği
* Verilerin Görselleştirilmesi
  
Veri ön işleme adımlarını Jupyter Notebook veya Python scripti kullanarak gerçekleştirebilirsiniz:
* Jupyter Notebook ile:
```
jupyter notebook data_preprocessing/data_preprocessing.ipynb
```
* Python scripti ile:
```
python data_preprocessing/main.py
```

## Verilerin Görselleştirmesi
### Aylık ve Çeyreklik Mevsimsellik Grafikleri
<img src="https://github.com/user-attachments/assets/9ca5c8a6-d4d4-48c8-b71c-8690dd6568b5" width="800" height="auto" />

### Verinin Bileşenlerine Ayrıştırılması
<img src="https://github.com/user-attachments/assets/dc5ea671-8ce3-44ca-9688-4ea6b75c7f9d" width="800" height="auto" />

### Otokorelasyon Grafiği
<img src="https://github.com/user-attachments/assets/832a35ee-3adc-4f58-a1e6-55147b77fce2" width="800" height="auto" />

### Yıllara Göre Günün İlk Sırasına En Çok Hasılatla Yerleşen Filmlerin Grafiği
<img src="https://github.com/user-attachments/assets/71b8a79c-05f0-4ecd-831a-f1c71fd3ee66" width="800" height="auto" />

