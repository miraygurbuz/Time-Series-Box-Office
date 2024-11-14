import data_preprocessing
import visualizations
import pandas as pd

df = pd.read_csv('../data/processed/processed.csv', parse_dates=['date'], index_col='date')

def main():
    data_preprocessing.preprocess_data()
    visualizations.plot_revenue_averages(df)
    visualizations.plot_seasonality(df)
    visualizations.plot_decomposition(df)
    visualizations.plot_acf_graph(df)

if __name__ == "__main__":
    main()