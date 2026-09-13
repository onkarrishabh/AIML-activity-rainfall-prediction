# Indian Rainfall Prediction

A mini-project that predicts monthly rainfall in India using machine learning. It downloads monthly climate data from NASA POWER, trains a model, and provides an interactive Streamlit app.

## Features

- Random forest regression for rainfall prediction in millimetres
- Indian state and month inputs
- Automatic one-hot encoding for categorical features
- Evaluation with MAE, RMSE, and R2
- Feature importance export
- Streamlit prediction interface

## Project structure

```text
indian-rainfall-prediction/
|-- data/
|   |-- generate_dataset.py
|   `-- indian_rainfall_sample.csv
|-- models/
|-- reports/
|-- src/
|   |-- train_model.py
|   `-- predict.py
|-- app.py
|-- requirements.txt
`-- README.md
```

## Setup

Use Python 3.10 or newer.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Train the model

The data script downloads 2000-2023 monthly NASA POWER records for representative locations in 12 Indian states. An internet connection is required when refreshing the CSV.

```powershell
py data\generate_dataset.py
python src\train_model.py
```

Training creates:

- `models/rainfall_model.joblib`
- `models/metrics.json`
- `reports/feature_importance.csv`

## Run the app

```powershell
py -m streamlit run app.py
```

Then open the local URL shown by Streamlit. The app predicts monthly rainfall from state, month, temperature, humidity, pressure, wind speed, and cloud cover.

## Data source and using another real dataset

The included CSV is sourced from [NASA POWER](https://power.larc.nasa.gov/), using monthly values from representative state-capital coordinates. Rainfall is converted from daily millimetres to monthly millimetres; pressure and wind speed are converted to hPa and km/h.

You can replace `data/indian_rainfall_sample.csv` with another CSV containing these columns:

```text
State,Month,Temperature_C,Humidity_pct,Pressure_hPa,WindSpeed_kmph,CloudCover_pct,Rainfall_mm
```

`Month` may be a number from 1 to 12 or a month name. `Rainfall_mm` is the target. The downloader shows the expected schema.

## Important note

This is an academic demonstration, not an operational weather forecasting system. Real forecasting quality depends on a sufficiently large, trusted, time-indexed dataset and careful validation across years and locations.
