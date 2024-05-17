import streamlit as st
import requests

url="http://127.0.0.1:8000/audio"
st.title("РЖД для служебных переговоров")

uploaded_file = st.file_uploader("Choose a file")

if uploaded_file is not None:
    files = {"file": (uploaded_file.name, uploaded_file.getvalue())}
    response = requests.post(url, files=files)

    if response.status_code == 200:
        st.success(f"File '{uploaded_file.name}' uploaded successfully!")
    else:
        st.error(f"Failed to upload file. Status code: {response.status_code}")
