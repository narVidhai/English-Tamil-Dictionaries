from tqdm import tqdm
import re
import pandas as pd

en_lang_pairs_count = {}

def add_pair(en_word, lang_word):
    if type(en_word) is not str or type(lang_word) is not str:
        return
    en_word = en_word.replace('"', '').strip().lower().rstrip('.')
    lang_word = lang_word.replace('"', '').strip().rstrip('.')
    key = (en_word, lang_word)
    if len(key[0])<2 or len(key[1])<2:
        return
    if key in en_lang_pairs_count:
        en_lang_pairs_count[key] += 1
    else:
        en_lang_pairs_count[key] = 1
    return

###################################################################

# https://github.com/linuxkathirvel/eng2tamildictionary

import json
data = json.load(open('raw/eng2tamildictionary/dictionary.json', encoding="utf-8"))

for record in tqdm(data, desc='eng2tamildictionary'):
    try:
        en_word, lang_words = record["eng"], record["tamil"]
    except:
        if 'word_list' in record:
            continue
        raise
    
    en_word = re.sub('\([^)]*?\)', '', en_word) # Remove brackets
    lang_words = re.sub('\([^)]*?\)', '', lang_words) # Remove brackets
    lang_words = re.sub("[A-Za-z]\.?", ' ', lang_words) # Remove English words from tamil
    lang_words = re.sub("-[1-9]", ' ', lang_words) # Remove numbered bullets
    for lang_word in lang_words.split(','):
        add_pair(en_word, lang_word)

# https://github.com/abuvanth/english-tamil-dictionary-api
# Same as above, so ignore.

# https://github.com/sathia27/dictionary
# Bad format. TODO: Clean and parse

# import sqlite3, os
# con = sqlite3.connect('raw/dictionary/word.db', isolation_level=None, detect_types=sqlite3.PARSE_COLNAMES)

# df = pd.read_sql_query("SELECT * FROM words", con)
# os.makedirs('tmp', exist_ok=True)
# df.to_csv("tmp/dict.csv")

## WRITE

out = open('consolidated.tsv', 'w', encoding='utf-8')
out.write(f"ENG\tLANG\tCOUNT\n")
for (en_word, lang_word), count in en_lang_pairs_count.items():
    out.write(f"{en_word}\t{lang_word}\t{count}\n")
out.close()
