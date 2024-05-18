@echo off

pip "install" "-r" "requirements.txt"
pip "install" "nemo_toolkit[all]"
python "-m" "spacy" "download" "ru_core_news_sm"
