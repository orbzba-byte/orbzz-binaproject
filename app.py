import streamlit as st
import pandas as pd
import joblib

model = joblib.load('xgb_final_model.pkl')
scaler = joblib.load('scaler_final.pkl')

FEATURES_ORDER = [
    'Total Length of Fwd Packets', 'Total Length of Bwd Packets', 'Fwd Packet Length Max',
    'Bwd Packet Length Max', 'Bwd Packet Length Mean', 'Max Packet Length',
    'Packet Length Mean', 'Packet Length Std', 'Packet Length Variance',
    'Average Packet Size', 'Avg Bwd Segment Size', 'Subflow Fwd Bytes',
    'Subflow Bwd Bytes', 'Init_Win_bytes_forward', 'Init_Win_bytes_backward'
]

CLASSES = [
    'BENIGN', 'Bot', 'DDoS', 'DoS GoldenEye', 'DoS Hulk',
    'DoS Slowhttptest', 'DoS slowloris', 'FTP-Patator',
    'Heartbleed', 'Infiltration', 'PortScan', 'SSH-Patator',
    'Web Attack - Brute Force', 'Web Attack - Sql Injection', 'Web Attack - XSS'
]

st.title("Cyber Attack Detection System")

tab1, tab2 = st.tabs(["- Detection System ", "- About the Project "])

with tab1:
    st.markdown("### Traffic Analysis (Normal vs. Attack)")
    inputs = {}
    col1, col2 = st.columns(2)
    for i, f in enumerate(FEATURES_ORDER):
        with col1 if i < 8 else col2:
            inputs[f] = st.text_input(f"{i+1}. {f}", "0.0")

    if st.button("Predict"):
        try:
            data = pd.DataFrame([[float(inputs[f]) for f in FEATURES_ORDER]], columns=FEATURES_ORDER)
            scaled_data = scaler.transform(data)
            pred_idx = model.predict(scaled_data)[0]
            predicted_label = CLASSES[pred_idx]
            
            if predicted_label == 'BENIGN':
                st.success(f"Normal Network Traffic (BENIGN)")
            else:
                st.error(f"Cyber Attack Detected! \n\nAttack Type: **{predicted_label}**")
        except Exception as e:
            st.error(f"Error: {e}")

with tab2:
    st.markdown("About the Project:")
    st.write("A security model that monitors website traffic to detect and predict cyber attacks.")
    st.info("Using an XGBoost Multi-Class classification model.")
