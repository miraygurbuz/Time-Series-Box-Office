[![en](https://img.shields.io/badge/lang-en-blue.svg)](https://github.com/miraygurbuz/Time-Series-Box-Office/blob/main/README.md)
[![tr](https://img.shields.io/badge/lang-tr-red.svg)](https://github.com/miraygurbuz/Time-Series-Box-Office/blob/main/README.tr.md)
# 🎬 Box Office Gross Revenue Forecasting Based on Daily Data
This project aims to forecast daily box office gross revenue using Transformer-based models.
## Project Overview
Daily box office data was scraped from the [Box Office Mojo](https://www.boxofficemojo.com/date/) website using Python. The data scraping process utilized the Selenium, BeautifulSoup4, and Requests libraries. Handling missing data, decomposition into trend and seasonality components, autocorrelation analysis, and feature engineering steps were applied to the scraped data.

In the second phase of the project, Transformer-based models were used to forecast box office gross revenue.
### Models Used:
* Autoformer
* TFT (Temporal Fusion Transformer)
* Informer
* FEDformer
* VanillaTransformer

### Libraries Used: 
* Selenium, BeautifulSoup4, Requests
* Statsmodels
* NeuralForecast

## Setup
* Clone the project:
```
git clone https://github.com/miraygurbuz/Time-Series-Box-Office.git
```
* Install the dependencies:
```
pip install -r requirements.txt
```
## Usage
### 1. Data Scraping
* You need to add the appropriate driver for your browser into the `driver` folder.
  
   * **For Chrome:** Download the `chromedriver` file and place it in the `driver` folder.
   * **For Firefox:** Download the `geckodriver` file and place it in the `driver` folder.
     
> ❗**Note:** After adding the driver to the folder, update the `DRIVER_PATH` section in the `scraper/settings.py` file to specify the driver path.

* Run the scraper:
```
python scraper/scraper.py
```
### 2. Data Preprocessing
#### The following steps were applied:
* Handling Missing Data
* Adding Time Variables
* Resampling the Time Series
* Decomposition of Time Series into Trend and Seasonality Components
* Autocorrelation Analysis
* Feature Engineering
    
You can perform the data preprocessing steps either via Jupyter Notebook or Python script:
* Using Jupyter Notebook:
```
jupyter notebook data_preprocessing/data_preprocessing.ipynb
```
* Using Python script:
```
python data_preprocessing/main.py
```
### 3. Transformer-Based Models
Google Colab was used for training and evaluating Transformer-based models. The detailed model training process can be accessed via the following Google Colab link:

[![](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/gist/miraygurbuz/e26773471c3ba83e45a00a9cef97f7b5/transformers.ipynb)
## Results
### Error Metrics Comparison

| Model               | MAPE (%)| MAE (million) | MSE (trillion) | RMSE (million) | R-squared (%)|
|---------------------|---------|--------------|---------------|---------------|------------|
| Autoformer          | 10.80 | 1.30         | 3.03          | 1.74          | 99.29     |
| TFT                 | 2.59  | 0.64         | 0.86          | 0.93          | 99.80     |
| Informer            | 4.05  | 0.60         | 0.58          | 0.76          | 99.73     |
| FEDformer           | 8.74  | 1.11         | 2.11          | 1.45          | 99.51     |
| VanillaTransformer  | 3.03  | 0.44         | 0.30          | 0.55          | 99.93     |

By examining the error metrics, it is evident that the VanillaTransformer model is the most accurate. It has the lowest MAPE and MAE values, indicating both a lower error rate and more stable forecasts, and its lower RMSE compared to other models suggests that it produces more consistent forecasts.

The TFT and Informer models also exhibited very close performance to each other, performing better than Autoformer and FEDformer but slightly behind VanillaTransformer.

The Autoformer model showed relatively lower performance compared to the others.

**Overall Performance Ranking:**

VanillaTransformer > Informer ≥ TFT > FEDformer > Autoformer
