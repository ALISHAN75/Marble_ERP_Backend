import googletrans
from googletrans import Translator

def lang_translate(stringToConvert, from_lang, to_lang):
    if stringToConvert is None: 
        return "", ""

    translator = Translator()
    converted_result = translator.translate(stringToConvert, src=from_lang, dest=to_lang).text

    if from_lang == "en": 
        return  stringToConvert, converted_result
    return converted_result, stringToConvert
