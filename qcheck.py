from fuzzywuzzy import process

# Данные
data = {
    "0": "на утро десять",
    "1": "",
    "2": "понятно опе по первому пути на станции населка",
    "3": "второй, радельно оператор перегольный красногвардей, загромная здравствуйте, не затягиваетесь, хорошо, до станции сорочинская проедьте пожалуйста по тоцкой, по первому пути будете ехать до мц барного",
    "4": "а шиленкой на поездной ой на маникрую переходите на окав"
}

str_count = 2  
count_first_words = 2  

target_words = ['машинист', 'оператор']

# Функция для проверки наличия целевых слов в первых нескольких строках текста
def check_input(dialog, target_words, str_count, count_first_words):
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

    return target

# Проверка данных
print(check_input(data, target_words, str_count, count_first_words))



