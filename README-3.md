# AI-Based Early Warning System for Electronic Component Failure

A complete, modular educational project that analyzes voltage, current, temperature, and resistance measurements, classifies component failure risk, evaluates the model, and provides a Streamlit dashboard.

## Features
- Synthetic, clearly labelled demo dataset generator (safe; no hardware required)
- Data validation, preprocessing, exploratory data analysis (EDA)
- Feature engineering from electrical measurements and rolling trends
- Random Forest classifier with train/test split and metrics
- Saved model, preprocessing pipeline, and evaluation report
- Streamlit dashboard for CSV upload and interactive risk prediction
- Optional ESP32/Arduino sensor collection guidance

> **Important:** The included data is synthetic demo data, not evidence of real component reliability. Do not use predictions to operate safety-critical equipment. Validate with real labelled data before any practical deployment.

## Project structure
- `requirements.txt` — Python dependencies
- `generate_dataset.py` — creates `data/component_measurements.csv`
- `src/data_utils.py` — validation and preprocessing
- `src/features.py` — feature engineering
- `src/train_model.py` — training, metrics, artifacts
- `src/predict.py` — prediction helper
- `app.py` — Streamlit warning dashboard
- `eda.py` — EDA plots and summary
- `tests/test_pipeline.py` — basic tests
- `report.md` — project report
- `presentation.md` — PPT slide content
- `data/` — generated dataset goes here
- `artifacts/` — trained model and metrics are written here
- `outputs/` — EDA plots and evaluation visuals

## Quick start (Python 3.10+ recommended)
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python generate_dataset.py --rows 3000
python eda.py
python -m src.train_model
streamlit run app.py
```

Open the local URL printed by Streamlit. The dashboard can use the included CSV or an uploaded CSV.

## Dataset columns
Required input columns:
- `timestamp` — sample time (ISO timestamp)
- `component_id` — identifier, e.g. `R1`, `C1`, `U1`
- `component_type` — resistor/capacitor/regulator/diode
- `temperature_c` — temperature in °C
- `voltage_v` — voltage in V
- `current_a` — current in A
- `resistance_ohm` — resistance in ohms
- `failure_within_24h` — target label: 1 if failure occurred / was labelled within 24h, otherwise 0

The generator creates illustrative labels from a transparent risk rule plus noise. This is useful for testing the pipeline, but the resulting high scores do not establish real-world predictive performance.

## CSV upload
For a custom dataset, include the required columns above. For dashboard predictions, the target column may be omitted. If the target is present, it is used only for evaluation. Units must match the column names. Missing numeric values are imputed using medians; invalid rows are dropped with a warning.

## Common commands
```bash
python generate_dataset.py --rows 3000 --seed 42
python -m src.train_model --data data/component_measurements.csv
python eda.py --data data/component_measurements.csv
pytest -q
```
