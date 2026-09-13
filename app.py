"""Streamlit interface for the Indian rainfall prediction model."""

import json
from pathlib import Path

import pandas as pd
import streamlit as st

from src.predict import MODEL_PATH, predict_rainfall


st.set_page_config(page_title="Indian Rainfall Prediction", page_icon="🌧️", layout="centered")
st.title("Indian Rainfall Prediction")
st.caption("A machine learning mini-project using NASA POWER monthly climate data")

if not MODEL_PATH.exists():
    st.warning("The model has not been trained yet. Run `python src/train_model.py` in the project folder.")
    st.stop()

states = [
    "Kerala", "Karnataka", "Maharashtra", "Tamil Nadu", "Odisha", "West Bengal",
    "Assam", "Rajasthan", "Gujarat", "Uttar Pradesh", "Bihar", "Delhi",
]
months = {
    "January": 1, "February": 2, "March": 3, "April": 4, "May": 5, "June": 6,
    "July": 7, "August": 8, "September": 9, "October": 10, "November": 11, "December": 12,
}
data_path = Path(__file__).parent / "data" / "indian_rainfall_sample.csv"
climate_data = pd.read_csv(data_path) if data_path.exists() else pd.DataFrame()

with st.form("prediction_form"):
    state = st.selectbox("Indian state", states)
    month_name = st.selectbox("Month", list(months))
    selected_month = months[month_name]
    if climate_data.empty:
        defaults = {
            "Temperature_C": 28.0,
            "Humidity_pct": 70.0,
            "Pressure_hPa": 1008.0,
            "WindSpeed_kmph": 12.0,
            "CloudCover_pct": 60.0,
        }
    else:
        selected_data = climate_data[
            climate_data["State"].eq(state) & climate_data["Month"].eq(selected_month)
        ]
        defaults = selected_data.mean(numeric_only=True).to_dict()
    temperature = st.slider("Temperature (°C)", 10.0, 45.0, float(defaults["Temperature_C"]), 0.5)
    humidity = st.slider("Relative humidity (%)", 20.0, 100.0, float(defaults["Humidity_pct"]), 1.0)
    pressure = st.slider("Atmospheric pressure (hPa)", 990.0, 1030.0, float(defaults["Pressure_hPa"]), 0.5)
    wind_speed = st.slider("Wind speed (km/h)", 0.0, 40.0, float(defaults["WindSpeed_kmph"]), 0.5)
    cloud_cover = st.slider("Cloud cover (%)", 0.0, 100.0, float(defaults["CloudCover_pct"]), 1.0)
    submitted = st.form_submit_button("Predict rainfall")

if submitted:
    input_data = {
        "State": state,
        "Month": selected_month,
        "Temperature_C": temperature,
        "Humidity_pct": humidity,
        "Pressure_hPa": pressure,
        "WindSpeed_kmph": wind_speed,
        "CloudCover_pct": cloud_cover,
    }
    rainfall, category = predict_rainfall(input_data)
    st.metric("Predicted rainfall", f"{rainfall:.1f} mm")
    st.success(category)

metrics_path = MODEL_PATH.parent / "metrics.json"
if metrics_path.exists():
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    with st.expander("Model performance"):
        st.write(f"Mean absolute error: {metrics['mae_mm']} mm")
        st.write(f"Root mean squared error: {metrics['rmse_mm']} mm")
        st.write(f"R² score: {metrics['r2']}")
