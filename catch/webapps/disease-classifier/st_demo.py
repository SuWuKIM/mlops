import json
import time
from pathlib import Path

import bentoml
import numpy as np
import streamlit as st

# wide page (증상 체크박스가 많아서...)
st.set_page_config(layout="wide")
st.title("증상으로 질병 예측")
st.write("아래 증상 중 해당되는 항목을 모두 선택하세요")

# sidebar 있어야 안정감
st.sidebar.title("DEMOs")
st.sidebar.selectbox("데모 프로젝트 선택", ["질병 예측", "드라마 추천"])


def load_symptoms():
    arr = []
    curr_dir = Path(__file__).resolve().parent
    with open(f"{curr_dir}/symptoms.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        arr.extend(data["symptoms"])
    return arr


def predict_disease(data):
    resp = None
    try:
        with bentoml.SyncHTTPClient("http://localhost:3000") as client:
            return client.predict(data)
    except Exception as e:
        st.error(f"요청 실패: {e}")

    return resp


# 증상 체크 박스
num_cols = 5
checked = []
button = st.button("예측 요청")
symptoms = load_symptoms()


def to_model_input(checked_symptoms: list):
    arr = [0] * len(symptoms)
    for s in checked_symptoms:
        arr[symptoms.index(s)] = 1
    return arr


cols = st.columns(num_cols)
for idx, symptom in enumerate(symptoms):
    if cols[idx % num_cols].checkbox(symptom, key=f"symptom_{idx}"):
        checked.append(symptom)

if button:
    message = None
    if not checked:
        message = (
            "환자분은 건망증에 걸리셨어요. 증상 체크 박스를 한 개 이상 선택해주세요"
        )
    else:
        input_data = to_model_input(checked)
        resp = predict_disease(input_data)
        if resp:
            pred = resp["prediction"][0]
            message = f"환자분은 {pred}일 가능성이 큽니다. 해당 질병의 평균 사망률은 ... 입니다"

    st_message = st.success(message)
    time.sleep(3)
    st_message.empty()
