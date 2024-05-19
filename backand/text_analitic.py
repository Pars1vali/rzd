import json
from thefuzz import process
import spacy

def _check_input_frases(dialog):
    valid = False
    str_count = 2
    count_first_words = 2

    target_words = ['внимание', 'машинист', 'оператор', 'дежурный']
    target = {word: False for word in target_words}

    # Удаление пустых строк из диалога
    dialog = {key: dialog[key] for key in dialog if dialog[key] != ''}

    for i, key in enumerate(dialog):
        if i >= str_count:
            break
        words = dialog[key].split()
        if len(words) > count_first_words:
            dialog_str = ' '.join(words[:count_first_words])
        else:
            dialog_str = ' '.join(words)

        for el in target_words:
            match, score = process.extractOne(el, dialog_str.split())
            if score >= 80:
                target[el] = True
    
    valid = False
    if target['машинист'] and (target['оператор'] or target['дежурный']):
        valid = True
    elif target['внимание'] and target['машинист']:
        valid = True

    return valid


# Функция для проверки наличия целевых слов в первых нескольких строках текста
def _detect_special_words(text_json):
    nlp = spacy.load("ru_core_news_sm")
    special_words = ['спасибо', 'пожалуйста', 'здравствуйте', 'здравствуй', 'хорошо']

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


def text_process(text_dict):
    text_json = json.loads(text_dict)
    valid = True
    type_problem = []

    # Ищет слова, которые не соответствуют разговору служебному, возвращает есть ли такие слова и проверку каждого предложения для указания ошибки
    is_detect, result = _detect_special_words(text_json)
    if is_detect == True:
        type_problem.append("special_words")
        valid = False

    #Оценка соотвествию начала разговора регламенту
    check_frases = _check_input_frases(text_json)
    if check_frases == False:
        type_problem.append("template_error")
        valid = False

    return valid, type_problem,

