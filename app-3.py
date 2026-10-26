"""Streamlit dashboard for early-warning failure risk."""
from pathlib import Path
import json
import pandas as pd
import streamlit as st
from src.data_utils import validate_measurements, TARGET
from src.features import engineer_features, model_feature_columns
import joblib

ROOT = Path(__file__).resolve().parent
st.set_page_config(page_title="Component Failure Early Warning", page_icon="⚡", layout="wide")
st.title("⚡ AI-Based Early Warning System")
st.caption("Educational prototype • Predictions are risk estimates, not guarantees.")
model_path = ROOT / "artifacts" / "failure_model.joblib"
default_data = ROOT / "data" / "component_measurements.csv"

with st.sidebar:
    st.header("Data source")
    uploaded = st.file_uploader("Upload CSV measurements", type=["csv"])
    threshold = st.slider("High-risk alert threshold", 0.10, 0.90, 0.50, 0.05)
    st.info("Required: component_type, temperature_c, voltage_v, current_a, resistance_ohm. Target label is optional.")

if uploaded is not None:
    raw = pd.read_csv(uploaded)
elif default_data.exists():
    raw = pd.read_csv(default_data)
else:
    st.warning("Dataset not found. Run `python generate_dataset.py` first.")
    st.stop()

try:
    df = validate_measurements(raw, require_target=False)
except Exception as e:
    st.error(str(e)); st.stop()

st.subheader("Latest measurements")
st.dataframe(df.tail(100), use_container_width=True)
if not model_path.exists():
    st.warning("Trained model not found. Run `python -m src.train_model` and refresh this page.")
    st.stop()

model = joblib.load(model_path)
X = engineer_features(df)[model_feature_columns()]
probs = model.predict_proba(X)[:, 1]
results = df.copy()
results["failure_risk_probability"] = probs
results["warning_level"] = ["HIGH" if p >= threshold else "NORMAL" for p in probs]
high = int((results["warning_level"] == "HIGH").sum())
c1, c2, c3 = st.columns(3)
c1.metric("Measurements analysed", f"{len(results):,}")
c2.metric("High-risk alerts", f"{high:,}")
c3.metric("Alert rate", f"{high / len(results):.1%}")
st.subheader("Risk results")
st.dataframe(results.sort_values("failure_risk_probability", ascending=False), use_container_width=True)
st.download_button("Download predictions CSV", results.to_csv(index=False).encode("utf-8"),
                   "failure_risk_predictions.csv", "text/csv")
st.subheader("Risk distribution")
st.bar_chart(results["failure_risk_probability"].round(1).value_counts().sort_index())
if TARGET in raw.columns:
    st.subheader("Evaluation on labelled uploaded data")
    from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
    labelled = raw.loc[df.index, TARGET] if len(raw) == len(df) else None
    if labelled is not None:
        try:
            y = pd.to_numeric(labelled, errors="coerce")
            valid = y.isin([0,1])
            if valid.any():
                pred = (results.loc[valid, "failure_risk_probability"] >= threshold).astype(int)
                y = y.loc[valid].astype(int)
                st.write({"accuracy": round(accuracy_score(y, pred), 3),
                          "precision": round(precision_score(y, pred, zero_division=0), 3),
                          "recall": round(recall_score(y, pred, zero_division=0), 3),
                          "f1_score": round(f1_score(y, pred, zero_division=0), 3)})
        except Exception:
            st.info("Could not calculate metrics for this upload.")
st.warning("Synthetic demo data and labels are not a substitute for validated engineering data. Use appropriate electrical protection and qualified supervision.")
