from nltk.translate import AlignedSent, Alignment
from nltk.translate import IBMModel3
import sqlite3

lang1 = []
lang2 = []

grammar_objects = [',','"','?','!']
corpus = []

lang1_words = []
lang2_words = []

def create_database():
    try:
        conn = sqlite3.connect('trans_table.db')
        conn.execute(('''CREATE TABLE TRANSLATION_TABLE
       (ID INTEGER PRIMARY KEY,
       WORD1   TEXT,
       WORD2 TEXT,
       PROB FLOAT
       );'''))
        conn.commit()
        conn.close()
    except:
        pass

def sentences_to_langs(file,lang):
    with open(file,'r',encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            lang.append(line)

def sentence_parser(sentence,lang):
    for object in grammar_objects:
        sentence = sentence.replace(object,'')
    sentence = sentence.split(' ')
    for word in sentence:
        if word not in lang:
            lang.append(word)
    return sentence


def aligned_sentences(sentence_lang1,sentence_lang2,corpus):
    corpus.append(AlignedSent(sentence_lang1,sentence_lang2))

def main_parser():
    sentences_to_langs('ru.txt',lang1)
    sentences_to_langs('en.txt',lang2)
    while len(lang1)> 0:
        lang_1_line = lang1.pop()
        lang_2_line = lang2.pop()
        lang_1_line = sentence_parser(lang_1_line,lang1_words)
        lang_2_line = sentence_parser(lang_2_line,lang2_words)
        aligned_sentences(lang_1_line,lang_2_line,corpus)

def relationships():
    ibm1 = IBMModel3(corpus,5)
    for word in lang1_words:
        for word2 in lang2_words:
            number = (ibm1.translation_table[word][word2])
            number = float(number)
            conn = sqlite3.connect('trans_table.db')
            conn.execute('''INSERT OR REPLACE INTO TRANSLATION_TABLE (WORD1,WORD2,PROB)
                        VALUES(?,?,?)''', (word, word2, number))
            conn.commit()
            conn.close()

try:
    create_database()
except:
    pass
main_parser()
relationships()
