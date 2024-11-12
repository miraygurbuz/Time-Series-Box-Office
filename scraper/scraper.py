import settings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.select import Select
from bs4 import BeautifulSoup
import requests
import time
import numpy as np
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

driver_path = settings.DRIVER_PATH
url = settings.BASE_URL
years = settings.YEARS
data_path = settings.OUTPUT_PATH

service = Service(driver_path)
driver = webdriver.Chrome(service=service)
driver.get(url)
driver.maximize_window()

all_dates, date_urls, all_days_of_year = [], [], []
all_releases, all_top_10_gross, all_top_1_gross = [], [], []
all_top_1_releases = []

def save_to_csv():
    df = pd.DataFrame({
        'url': date_urls,
        'date': all_dates,
        'day_of_year': all_days_of_year,
        'releases': all_releases,
        'top_1_gross': all_top_1_gross,
        'top_1_release': all_top_1_releases,
        'top_10_gross': all_top_10_gross,
        'total_gross': all_total_gross
    })
    df.to_csv(data_path, index=False)
    print(f"CSV dosyası {data_path} adresine kaydedildi.")

def save_yearly_daily_data():
    for year in years:
        dropdown = Select(driver.find_element("id", "year-navSelector"))
        dropdown.select_by_visible_text(str(year))
        time.sleep(0.5)
        page_source = driver.page_source
        soup = BeautifulSoup(page_source, 'html.parser')

        dates = soup.find_all('td', class_='a-text-left mojo-header-column mojo-truncate mojo-field-type-date_interval mojo-sort-column')
        for date in dates:
            href = date.select('a')[0]['href']
            date_str = href.split('/')[2]
            all_dates.append(date_str)
            date_url = f"https://www.boxofficemojo.com{href}"
            date_urls.append(date_url)

        days_of_year = soup.find_all('td', class_='a-text-right mojo-field-type-date_interval')
        for day_of_year in days_of_year:
            day_of_year_str = day_of_year.select('a')[0].string
            all_days_of_year.append(day_of_year_str)

        releases = soup.find_all('td', class_='a-text-right mojo-field-type-positive_integer')
        for release in releases:
            release_str = release.get_text()
            all_releases.append(int(release_str))

        top_1_releases = soup.find_all('td', class_='a-text-left mojo-field-type-release mojo-cell-wide')
        for top_1_release in top_1_releases:
            top_1_release_str = top_1_release.get_text().strip()
            all_top_1_releases.append(top_1_release_str)

        rows = soup.find_all('tr')
        for row in rows:
            gross = row.find_all('td', class_='a-text-right mojo-field-type-money')
            if len(gross) >= 2:
                top10gross_str = gross[0].text.strip()
                top10gross_str = top10gross_str.replace('$', '').replace(',', '')
                all_top_10_gross.append(int(top10gross_str))
                top1gross_str = gross[1].text.strip()
                top1gross_str = top1gross_str.replace('$', '').replace(',', '')
                all_top_1_gross.append(int(top1gross_str))
        time.sleep(0.5)
    driver.quit()

def get_daily_gross(date_url):
    try:
        response = requests.get(date_url, timeout=20)
        soup = BeautifulSoup(response.content, 'html.parser')
        rows = soup.select('tr')
        grosses = []
        for row in rows:
            money = row.find_all('td', class_='a-text-right mojo-field-type-money mojo-estimatable')
            if not money:
                continue
            daily_gross = money[0].text.strip()
            daily_gross = daily_gross.replace('$', '').replace(',', '')
            grosses.append(int(daily_gross))
        total_gross = sum(grosses) if grosses else 0
        print(f"Adres: {date_url}, Vizyondaki filmlerin günlük toplam hasılatı: {total_gross}")
        return int(total_gross)
    except Exception as e:
        print(e)

save_yearly_daily_data()
with ThreadPoolExecutor(max_workers=40) as executor:
    all_total_gross = list(executor.map(get_daily_gross, date_urls))
save_to_csv()