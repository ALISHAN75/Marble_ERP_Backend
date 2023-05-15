# import googletrans
from googletrans import Translator
translator = Translator()

def func_en_to_ur(text):
    result = translator.translate(text, src='en', dest='ur')
    # result = translator.translate("""Ali Shan""", src='en', dest='ur')
    return result.text
    
def func_ur_to_en(text):
    # result = translator.translate("""علی شان""", src='ur', dest='en')
    result = translator.translate(text, src='ur', dest='en')
    return result.text



def lang_detect(string):
    if string[:20].upper() != string[:20].lower():
        return 'en'
    else: return 'ur'