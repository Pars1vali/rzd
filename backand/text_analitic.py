import json
from thefuzz import process
import spacy

def _detect_special_words(text_json):
    nlp = spacy.load("ru_core_news_sm")
    special_words = ['спасибо', 'пожалуйста', 'здравствуйте', 'здравствуй']

    def _detect(text):
        doc = nlp(text)
        for token in doc:
            if len(token) >= 3:
                special_word, probability_special = process.extractOne(str(token), special_words)
                if probability_special >= 85:
                    return True
        return False

    is_detect = False
    result = dict()

    for key, value in text_json.items():
        text_clear = value.replace(",", "")
        result_detect = _detect(text_clear)
        result[key] = result_detect
        if result_detect:
            is_detect = True

    return is_detect, result

def _note_template_speak(text):
    return False


def text_process(text_dict):
    text_json = json.loads(text_dict)
    valid = None
    type_problem = []

    # Ищет слова, которые не соответствуют разговору служебному, возвращает есть ли такие слова и проверку каждого предложения для указания ошибки
    is_detect, result = _detect_special_words(text_json)
    if is_detect == True:
        type_problem.append("special_words")
        valid = True

    #Оценка соотвествию начала разговора регламенту
    is_template_error = _note_template_speak(text_json)
    if is_template_error == True:
        type_problem.append("template_error")
        valid = True

    return valid, type_problem,

