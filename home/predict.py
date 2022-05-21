from ast import literal_eval
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob
import pickle
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
df = {}


def levenshtein(a, b):
    m = [[*range(len(a) + 1)] for _ in range(len(b) + 1)]
    for i in range(len(b) + 1):
        m[i][0] = i
    for i in range(1, len(b) + 1):
        for j in range(1, len(a) + 1):
            m[i][j] = min(m[i-1][j] + 1, m[i][j-1] + 1,
                          m[i-1][j-1] + (b[i-1] != a[j-1]))
    return m[-1][-1]


def editSymptom(text):
    #     print(text)
    if type(text) == str:
        text = nltk.word_tokenize(text)
        res = []

        # print(text)

        for i in text:
            b = TextBlob(i)
            res.append(str(b.correct()))

        # lemmatizer = WordNetLemmatizer()
        # result = []
        result1 = []
        unwanted = ['i', 'am', 'be', 'are', 'is', 'was', 'were', 'being', 'can', 'could', 'do', 'did', 'does', 'doing',
                    'have', 'had', 'has', 'having', 'may', 'might', 'must', 'shall', 'should', 'will', 'would', 'days', 'day']
        pos_tagged = nltk.pos_tag(res)

        print(pos_tagged)

        text = filter(lambda x: x[1] == 'NN' or x[1] == 'NNS' or x[1] == 'NNP' or x[1] == 'JJ' or x[1] == 'NNPS' or x[1] == 'PRP' or x[1] == 'PRP$' or x[1] ==
                      'RB' or x[1] == 'RBR' or x[1] == 'RBS' or x[1] == 'VB' or x[1] == 'VBG' or x[1] == 'VBD' or x[1] == 'VBN' or x[1] == 'VBP' or x[1] == 'VBZ', pos_tagged)
        for i in text:
            if i[0] not in unwanted:
                tem = i[0].replace('.', '')
                result1.append(tem)

        print(result1)
        return result1

    else:
        return []


def findSimilarity(text):
    similarDict = {}
    finalList = []
    for i in text:
        for j in range(len(df['symptoms'])):
            temp = []
            if len(df['symptoms'][j]) != 0:
                for k in df['symptoms'][j]:
                    temp.append(fuzz.partial_ratio(i, k))

                if j not in similarDict:
                    similarDict[j] = {}
                # print('temp--->>>', temp)
                similarDict[j][i] = max(temp)
            else:
                if j not in similarDict:
                    similarDict[j] = {}
                similarDict[j][i] = 0

    for i in range(len(similarDict)):
        finalList.append(sum(similarDict[i].values()))

    return finalList.index(max(finalList))


def main():
    global df
    df = pd.read_csv(r'home/final-disease.csv',
                     converters={"symptoms": literal_eval})
    print('done')


def predictOut(text):
    text = text.lower()
    botin = {'greet': ['hi', 'hello', 'hey', 'good morning', 'good afternoon', 'good evening', 'good night', 'hai', 'hoi', 'heey', 'healthkonvo'], 'bye': [
        'thanks', 'thank you', 'thank', 'thank u', 'bye', 'byee', 'good bye'], 'hru': ['how are you', 'how r u', 'how r you', 'how are u', 'whats up', "what's up"], 'no': ['no', 'no thanks'], 'yes': ['yes', 'I want to know', 'yes i want to know', 'yes i want', 'yes, i want', 'yes, i want to know'],
        'help': ['i need your help', 'i need you', 'i want your help', 'can you help', 'can you help me?', 'can you help me', 'can u help me']
    }

    botout = {'greet': 'Hello, I am healthKonvo, a disease diagnosis bot. Send me a list of symptoms , i will diagnose the disease.',
              'hru': 'I am fine.', 'bye': 'Do you want to know something more?', 'no': 'Happy to help you.', 'yes': 'How can I help you?', 'help': 'How can I help you?'}
    for i in botin:
        if text in botin[i]:
            return {'text': botout[i], 'details': ''}

    edited = editSymptom(text)

    # print(edited)

    if len(edited) == 0:
        return {'text': "Hey , I can't diagnose your disease. Please share all symptoms and conditions you have.", 'details': ''}
    # edited = ' '.join(edited)

    # res = process.extract(edited, df['symptoms'], limit=10)

    ind = findSimilarity(edited)

    print(ind)

    # ind = res[0][2]

    dis = df.iloc[ind]

    # print(dis)

    resp = 'I think you have '+dis[0]

    det = {}

    # print(type(dis[1]))

    if type(dis[1]) == str:
        # print('hai')
        det['About disease'] = dis[1]
    if type(dis[3]) == str:
        det['Causes'] = dis[3]
    if type(dis[4]) == str:
        det['Diagnosis'] = dis[4]
    if type(dis[5]) == str:
        det['Management'] = dis[5]
    if type(dis[6]) == str:
        det['Complications'] = dis[6]
    if type(dis[7]) == str:
        det['Prevention'] = dis[7]
    if type(dis[8]) == str:
        det['Classification'] = dis[8]
    if type(dis[9]) == str:
        det['Transmission'] = dis[9]
    if type(dis[10]) == str:
        det['Treatment'] = dis[10]

    # print({'text': resp, 'details': det})

    return {'text': resp, 'details': det}
    # return "hai"


main()
