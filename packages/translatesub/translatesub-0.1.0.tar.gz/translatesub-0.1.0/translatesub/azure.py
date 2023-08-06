import os
import requests
import json
import pysubs2

def azure_verify():
  return (os.environ.get('TRANSLATOR_TEXT_ENDPOINT') is not None) and (os.environ.get('TRANSLATOR_TEXT_SUBSCRIPTION_KEY') is not None) and ((os.environ.get('TRANSLATOR_TEXT_REGION') is not None))

def azure_translate_text_bulk(texts, target_lang='pt', source_lang='en'):
    constructed_url = f"{os.environ.get('TRANSLATOR_TEXT_ENDPOINT')}translator/text/v3.0/translate"
    params = {
        "from": source_lang,
        "to": [target_lang]
    }
    headers = {
        'Ocp-Apim-Subscription-Key': os.environ.get('TRANSLATOR_TEXT_SUBSCRIPTION_KEY'),
        # location required if you're using a multi-service or regional (not global) resource.
        'Ocp-Apim-Subscription-Region': os.environ.get('TRANSLATOR_TEXT_REGION'),
        'Content-type': 'application/json'
    }
    body = [{
        'text': text.replace("\\N", " \\N ").replace("\\n", " \\n ")
    } for text in texts]
    request = requests.post(constructed_url, params=params, headers=headers, json=body)
    response = request.json()

    try:
        return [translation['translations'][0]['text'] for translation in response]
    except:
        raise Exception(json.dumps(response, sort_keys=True, ensure_ascii=False, indent=4, separators=(',', ': ')))

def translate_subtitles(srt, target_lang, source_lang='en'):
    # Azure
    subs = pysubs2.SSAFile.from_string(srt)

    translations = azure_translate_text_bulk([line.text for line in subs], target_lang=target_lang, source_lang=source_lang)
    i = 0

    for line in subs:
        line.text = translations[i]
        i = i + 1

    return subs