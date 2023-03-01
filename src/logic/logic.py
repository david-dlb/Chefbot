from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
import pandas as pd
import json
import spacy as sp

nlp = sp.load("es_core_news_md")

df = pd.read_json("assest/Data/train-esp.json")
df_cook = pd.read_csv("assest/Data/intents_cook.csv")
df_cook_others = pd.read_csv('assest/Data/intents_cook_others.csv')


with open('assest/Data/intents.json') as json_data:
    intents = json.load(json_data)


df_cook_others["label"] = df_cook_others.label.map({ 'cook': 1, 'others': 0})
df_cook["label"] = df_cook.label.map({ 'title': 2, 'instructions': 1, 'title_instructions': 0})

X_train, X_test, y_train, y_test = train_test_split(df_cook_varios['text'], df_cook_varios['label'], random_state=0.2)

# Instantiate the CountVectorizer method
count_vector = CountVectorizer()
# Fit the training data and then return the matrix
training_data = count_vector.fit_transform(X_train)
# Transform testing data and return the matrix. Note we are not fitting the testing data into the CountVectorizer()
testing_data = count_vector.transform(X_test)

naive_bayes = MultinomialNB()
naive_bayes.fit(training_data, y_train)
predictions = naive_bayes.predict(testing_data)


def cook_others(text):
    # Dividir el conjunto de datos de entrenamiento y test
    X_train, X_test, y_train, y_test = train_test_split(df_cook_others['text'], df_cook_others['label'], random_state=1)
    
    # Instantiate the CountVectorizer method
    count_vector = CountVectorizer()
    # Fit the training data and then return the matrix
    training_data = count_vector.fit_transform(X_train)
    # Transform testing data and return the matrix. Note we are not fitting the testing data into the CountVectorizer()
    testing_data = count_vector.transform(X_test)
    text_data = count_vector.transform([text])

    naive_bayes = MultinomialNB()
    naive_bayes.fit(training_data, y_train)
    
    return naive_bayes.predict(text_data)


def cook(text):
    # Dividir el conjunto de datos de entrenamiento y test
    X_train, X_test, y_train, y_test = train_test_split(df_cook['text'], df_cook['label'], random_state=1)
    
    # Instantiate the CountVectorizer method
    count_vector = CountVectorizer()
    # Fit the training data and then return the matrix
    training_data = count_vector.fit_transform(X_train)
    # Transform testing data and return the matrix. Note we are not fitting the testing data into the CountVectorizer()
    testing_data = count_vector.transform(X_test)
    text_data = count_vector.transform([text])

    naive_bayes = MultinomialNB()
    naive_bayes.fit(training_data, y_train)
    
    return naive_bayes.predict(text_data)


def others(text):
    x = []
    y_train = []
    for i in range(4):
    #     print(intents["intents"][i])
        label = intents["intents"][i]["tag"]
        for j in intents["intents"][i]["patterns"]:
            x.append(j)
            y_train.append(label)
            
    # Instantiate the CountVectorizer method
    count_vector = CountVectorizer()
    # Fit the training data and then return the matrix
    training_data = count_vector.fit_transform(x)
    text_data = count_vector.transform([text])

    naive_bayes = MultinomialNB()
    naive_bayes.fit(training_data, y_train)
    
    return naive_bayes.predict(text_data)


def search(text, first, second):
    ma = -1000000
    sol = ""
    doc = nlp(text)
    doc = doc.similarity(text)
    return sol
        
def response_others(tag):
    for i in range(4):
    #     print(intents["intents"][i])
        label = intents["intents"][i]["tag"]
        if label == tag:
            return intents["intents"][i]["responses"][0]


def get_response(text):
    firstIntent = cook_others(text)[0]
    if firstIntent == 0:
        intentOthers = others(text)[0]
        return response_others(intentOthers)
    else:
        cook_intents = cook(text)
        if cook_intents == 1:
            return search(text, "ingredients", "instructions")

        if cook_intents == 2:
            return search(text, "ingredients", "title")

        if cook_intents == 0:
            return search(text, "title", "instructions")
    return firstIntent