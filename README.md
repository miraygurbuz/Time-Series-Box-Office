# 🎞️ Gişe Verilerine Göre Hasılat Tahmini 🎞️

## Proje Hakkında
Günlük gişe verileri, Box Office Mojo web sitesinden Python kullanılarak toplanmıştır. Veri toplama sürecinde Selenium, BeautifulSoup4 ve Requests kütüphaneleri kullanılmıştır. Toplanan veriler üzerinde eksik verilerin tamamlanması, trend ve mevsimsellik bileşenlerine ayrıştırma, otokorelasyon analizi ve özellik mühendisliği adımları uygulanmıştır. Projenin ikinci kısmında, Transformer tabanlı modeller kullanılarak gişe hasılat tahmini gerçekleştirilmiştir.

Kullanılan modeller:
- Autoformer
- TFT (Temporal Fusion Transformer)
- Informer
- FEDformer
- VanillaTransformer

## Kullanılan Kütüphaneler
- Selenium, BeautifulSoup4, Requests
- Statsmodels
- NeuralForecast

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
  
> 🔔 **Not:** Sürücüyü `driver` klasörüne ekledikten sonra `scraper` klasörü içindeki `settings.py` dosyasının `DRIVER_PATH` kısmını güncelleyerek sürücü yolunu belirtin.

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
* Otokorelasyon Analizi
* Özellik Mühendisliği
  
Veri ön işleme adımlarını Jupyter Notebook veya Python scripti kullanarak gerçekleştirebilirsiniz:
* Jupyter Notebook ile:
```
jupyter notebook data_preprocessing/data_preprocessing.ipynb
```
* Python scripti ile:
```
python data_preprocessing/main.py
```

### 3. Transformer Tabanlı Tahmin Modelleri
Transformer tabanlı modellerin eğitimi ve değerlendirilmesi Google Colab ortamında gerçekleştirilmiştir. 
  
Detaylı model eğitim sürecine erişmek için Google Colab bağlantısını kullanabilirsiniz: [![](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/gist/miraygurbuz/e26773471c3ba83e45a00a9cef97f7b5/transformers.ipynb)

## Sonuçlar 
### Model Performans Karşılaştırma Metrikleri

| Model               | MAPE    | MAE (milyon) | MSE (trilyon) | RMSE (milyon) | R-squared  |
|---------------------|---------|--------------|---------------|---------------|------------|
| Autoformer          | %10,80 | 1,30         | 3,03          | 1,74          | %99,29     |
| TFT                 | %2,59  | 0,64         | 0,86          | 0,93          | %99,80     |
| Informer            | %4,05  | 0,60         | 0,58          | 0,76          | %99,73     |
| FEDformer           | %8,74  | 1,11         | 2,11          | 1,45          | %99,51     |
| VanillaTransformer  | %3,03  | 0,44         | 0,30          | 0,55          | %99,93     |

Model performans karşılaştırma metrikleri incelendiğinde, VanillaTransformer modelinin %3,03 MAPE ve 0,44 milyon MAE ile gişe hasılatı tahmininde en başarılı model olduğu görülmektedir. TFT ve Informer modelleri de oldukça yakın performans sergilemiştir. Autoformer modeli ise diğer modellerden düşük performans göstermiştir. Genel başarı sıralaması VanillaTransformer > Informer ≥ TFT > FEDformer > Autoformer şeklindedir.
