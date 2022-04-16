import nltk
import requests
from rake_nltk import Rake
from nltk.corpus import wordnet
from nltk.stem import WordNetLemmatizer,PorterStemmer
from utils import _get_soup_object

GRAMMAR_URL = "https://api.textgears.com/grammar"
API_KEY="0JfABzC0bNDoybFn"

max_score=10
train_data=['the theory and development of computer systems able to perform tasks normally requiring human intelligence,' \
           'such as visual perception, speech recognition, decision-making, and translation between languages.' ,
           'Machine learning is an application of artificial intelligence (AI) that provides systems the ability to automatically learn and improve ' \
           'from experience without being explicitly programmed. Machine learning focuses on the development of computer programs that can access ' \
           'data and use it learn for themselves.' ,
           'A genetic algorithm (GA) is a method for solving both constrained and unconstrained optimization problems ' \
           'based on a natural selection process that mimics biological evolution. The algorithm repeatedly modifies a population of individual ' \
           'solutions.' ,
           'the application of computational techniques to the analysis and synthesis of natural language and speech.' ,
           'the branch of technology that deals with the design, construction, operation, and application of robots.']

key=[{'human': 5, 'recognition': 5, 'computer': 5, 'able': 5, 'visual': 5, 'speech': 5, 'task': 5, 'translation': 5, 'making': 5,
       'perception': 5, 'language': 5, 'development': 5, 'normally': 5, 'intelligence': 5, 'decision': 5, 'system': 5,
       'theory': 8, 'requiring': 7},{'system': 5, 'experience': 5, 'learn': 5, 'automatically': 5, 'explicitly': 5, 'computer': 5, 'application': 5, 'program': 5,
       'intelligence': 5, 'access': 5, 'programmed': 5, 'artificial': 5, 'machine': 5, 'data': 5, 'improve': 5, 'ai': 5, 'without': 5,
       'focus': 3, 'ability': 2, 'development': 2, 'provides': 2, 'use': 3, 'learning': 3},{'process': 5, 'optimization': 5, 'genetic': 5,
        'modifies': 5, 'population': 5, 'method': 5, 'based': 5, 'selection': 5, 'solving': 5, 'solution': 5, 'individual': 5, 'natural': 5,
       'repeatedly': 5, 'algorithm': 5, 'mimic': 5, 'evolution': 5, 'constrained': 5, 'problem': 5, 'biological': 5, 'ga': 2, 'unconstrained': 3},
        {'language': 15, 'computational': 15, 'synthesis': 15, 'speech': 15, 'application': 10, 'natural': 10, 'technique': 10, 'analysis': 10},
        {'deal': 10, 'operation': 10, 'application': 10, 'design': 20, 'branch': 10, 'technology': 20, 'construction': 10, 'robot': 10}
]

testlist=[]
trainlist=[]
i=0

def synonyms(term, formatted=False):
    if len(term.split()) > 1:
        print("Error: A Term must be only a single word")
    else:
        try:
            data = _get_soup_object("https://www.synonym.com/synonyms/{0}".format(term))
            section = data.find('div', {'class': 'type-synonym'})
            spans = section.findAll('a')
            synonyms = [span.text.strip() for span in spans]
            if formatted:
                return {term: synonyms}
            return synonyms
        except:
            return


def lematize(lista):
    w=WordNetLemmatizer()
    a=list(map(w.lemmatize,lista))
    return a
def stem(lista):
    s=PorterStemmer()
    a=list(map(s.stem,lista))
    return a
def break_phrases(list):
    a=[]
    for x in list:
        if len(x.split())==1:
            a.append(x)
        else:
            a.extend(x.split())
    return a

def grammatical_mistakes(data):
    payload={"text":data,"language":"en-GB","key":API_KEY}
    res = requests.post(GRAMMAR_URL,params=payload)
    result=res.json()
    return len(result['response']['errors'])
    
def Extract(train_data,test_data,max_score,j,Enter_rank=True):
    train,test = Rake(),Rake()
    train.extract_keywords_from_text(train_data)
    test.extract_keywords_from_text(test_data)
    train_keywords=lematize(break_phrases(train.get_ranked_phrases()))
    test_keywords=lematize(break_phrases(test.get_ranked_phrases()))
    for x in train_keywords:
        trainlist.append(x)
    for x in test_keywords:
        testlist.append(x)

    result=0

    #score for len of ans
    if len(test_keywords)>2:
        result=len(test_data)*0.009

    print("\nScore for len of ans: "+str(result))

    #score for grammar mistakes
    mistakes=grammatical_mistakes(test_data)
    print("Grammatical mistakes: "+str(mistakes))
    result=result-(mistakes)*0.1

    dict=key[j]
    for x in testlist:


        if x in dict.keys():
            result=result+(dict[x]*max_score)/100
        else:
            syn=synonyms(trainlist[i])
            if syn==None:
                continue
            for j in syn :
                if j in testlist:
                    dict[j]=(dict[x]*max_score)/100
                    result = result + dict[j] * max_score
    return result


while True:
    print("\n1.What is Ai")
    print("2.What is Machine learning")
    print("3.What is Genetic algo")
    print("4.What is NLp")
    print("5.What is robotics")
    print("6.exit")

    num = int(input("Enter your choice: "))
    i=num-1
    # choice(num)

    if num==6:
        exit();
    print("Enter your ans: ")
    test=input()
    print("Score: "+str(Extract(train_data[i],test,max_score,i))+"/15")


