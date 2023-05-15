def lang_detect(string):
    if string[:20].upper() != string[:20].lower():
        return 'en', "ur"
    else: return 'ur', "en"

