import json
import streamlit as st
import requests

url="https://pars1vali-rzd-b134.twc1.net/audio"

def send_audio(uploaded_file):
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        response_json = json.loads(response.text)
        st.write(response_json)
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    else:
        st.error(f"Failed to upload file. Status code: {response.status_code}")


st.title("РЖД для служебных переговоров")
uploaded_file = st.file_uploader("Загрузите аудио", type=['wav','mp3'] )

if uploaded_file is not None:
    with st.spinner("Обработка"):
        send_audio(uploaded_file)

