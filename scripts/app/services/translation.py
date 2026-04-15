"""Translation service for multi-language support"""

from googletrans import Translator

translator = Translator()

def translate_to_english(text):
    """Translate Hindi/Telugu complaints to English automatically"""
    try:
        translated = translator.translate(text, dest='en')
        print(f"[v0] Translated to English: {translated.text}")
        return translated.text
    except Exception as e:
        print(f"[v0] Translation error: {e}")
        return text
