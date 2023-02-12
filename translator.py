import requests
import json



oxford_id = ""
oxford_keys = ""
language = "en-gb"

wordId = "work"

def get_definition(word_id):
    url = "https://od-api.oxforddictionaries.com:443/api/v2/entries/" + language + "/" + word_id.lower()
    r = requests.get(url, headers={"app_id": oxford_id, "app_key": oxford_keys})
    res = r.json()

    if 'error' in res:
        return False

    output = {}
    definitions = []
    senses = res['results'][0]['lexicalEntries'][0]['entries'][0]['senses']
    for sense in senses:
        definitions.append(f"-> {sense['definitions'][0]}")
    output['definitions'] = "\n".join(definitions)

    if res['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0].get('audioFile'):
        output['audio'] = res['results'][0]['lexicalEntries'][0]['entries'][0]['pronunciations'][0]['audioFile']
    
    return output   
    
    


if __name__ == '__main__':
    print(get_definition(word_id=wordId))