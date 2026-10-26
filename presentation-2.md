# Presentation: AI-Based Early Warning System for Electronic Component Failure

## Slide 1 — Title
**AI-Based Early Warning System for Electronic Component Failure**
- Capstone project
- Predictive monitoring using electrical measurements

## Slide 2 — Problem
- Component faults may follow abnormal temperature, voltage, current, or resistance.
- Manual checks can miss developing trends.
- Goal: flag measurements that resemble previously labelled failure cases.

## Slide 3 — Objectives
- Validate and explore measurements.
- Create derived electrical features.
- Train and evaluate a classifier.
- Display risk scores in a dashboard.

## Slide 4 — System architecture
1. CSV / safe sensor measurements
2. Validation and preprocessing
3. Feature engineering
4. Random Forest classifier
5. Risk threshold and warning
6. Streamlit dashboard / downloadable CSV

## Slide 5 — Dataset
- Timestamp and component type/ID
- Temperature (°C), voltage (V), current (A), resistance (Ω)
- Target: failure_within_24h (0/1)
- Included demo data is synthetic and illustrative.

## Slide 6 — Feature engineering
- Power: P = V × I
- Voltage/current ratio
- Temperature excess above 40°C
- Log-transformed resistance
- Component type encoded categorically

## Slide 7 — Model
- Random Forest classifier
- Stratified 80/20 train/test split
- Imputation and one-hot encoding within the pipeline
- Fixed random seed for reproducibility

## Slide 8 — Evaluation
- Accuracy, precision, recall, F1-score, ROC-AUC
- Confusion matrix
- Metrics saved to `artifacts/metrics.json`
- Synthetic-data metrics do not demonstrate real-world accuracy.

## Slide 9 — Dashboard
- Upload a CSV or use demo dataset
- Set alert threshold
- Review risk probability and HIGH/NORMAL status
- Download predictions

## Slide 10 — Safety and limitations
- Synthetic labels are not real failure observations.
- Never create dangerous faults for data collection.
- Use calibrated sensors and qualified supervision.
- Do not use the prototype to control safety-critical equipment.

## Slide 11 — Future scope
- Real labelled data
- Time-aware and component-grouped testing
- ESP32/Arduino data acquisition
- Drift monitoring and alert logging

## Slide 12 — Conclusion
- Complete modular ML prototype
- Demonstrates preprocessing, feature engineering, classification, evaluation, and dashboard reporting
- Requires real-world validation before deployment
