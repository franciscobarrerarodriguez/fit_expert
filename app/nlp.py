import random

import requests

from nltk import NaiveBayesClassifier as nbc
from nltk import chunk

from nltk.corpus import stopwords
from nltk.corpus import names

from nltk.tokenize import word_tokenize
from nltk.tokenize import RegexpTokenizer

from nltk.tag import pos_tag

from nameparser.parser import HumanName

class NaturalLanguageProcessing(object):
    """docstring for Nlp."""

    def __init__(self):

        self.stop_words = set(stopwords.words('english'))

        # List of examples and corresponding class labels.
        self.labeled_names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])
        random.shuffle(self.labeled_names)

        featuresets = [(self.gender_features(n), gender) for (n, gender) in self.labeled_names]
        self.classifier = self.train_gender(featuresets[1000:])

        # print(self.classifier.classify(self.gender_features('Laura')))

    # Transforms text to array and remove punctuation
    def tokenize_text(self, text):
        # text = text.lower()
        tokenizer = RegexpTokenizer(r'\w+')
        return tokenizer.tokenize(text)

    # Delete empty words in spanish language
    def clear_empty_words(self, words):
        filtered_sentence = []
        for word in words:
            if word.lower() not in self.stop_words:
                filtered_sentence.append(word)
        return list(filtered_sentence)

    # Find human names in a text, text must be tokenized
    def find_human_names(self, words):
        pos = pos_tag(words)
        sentt = chunk.ne_chunk(pos, binary = False)
        person_list = []
        person = []
        name = ""
        for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
            for leaf in subtree.leaves():
                person.append(leaf[0])
            if len(person) > 1: #avoid grabbing lone surnames
                for part in person:
                    name += part + ' '
                if name[:-1] not in person_list:
                    person_list.append(name[:-1])
                name = ''
            person = []
        if (len(person_list) > 0):
            person_list = self.tokenize_text(person_list[0])
            return person_list[0]
        else:
            return False

    # Find all digits in an array
    def find_digits(self, words):
        aux = []
        for word in words:
            if (word.isdigit()):
                aux.append(word)
        return aux

    # Validate user's age
    def validate_age(self, age):
        return True if age >= 10 and age <= 100 else False

    # Define features to evaluate names
    def gender_features(self, name):
        features = {}
        features["first_letter"] = name[0].lower()
        features["last_letter"] = name[-1].lower()
        for letter in 'abcdefghijklmnopqrstuvwxyz':
            features["count({})".format(letter)] = name.lower().count(letter)
            features["has({})".format(letter)] = (letter in name.lower())
        return features

    def find_gender(self, name):
        return self.classifier.classify(self.gender_features(name))

    def train_gender(self, train_set):
        return nbc.train(train_set)

    # Get all stop word
    def get_stop_words(self):
        return self.stop_words

    # Return mood in text
    # status_code 200 sussesfull
    # http://text-processing.com/docs/sentiment.html
    # API url:  http://text-processing.com/api/sentiment/
    def find_mood(self, text):
        params = {"text" : text}
        response = requests.post("http://text-processing.com/api/sentiment/", params)
        if (response.status_code == 200):
            response = response.json()
            return response #label/probability
        else:
            return False

# nlp = NaturalLanguageProcessing()
# mood = nlp.find_mood("I'm so happy today")
# label = mood['label']
# print(mood['probability'][label])

# sentence = "an They My name is michael Francisco Barrera and I'm 23 years old"
# names = nlp.find_human_names(nlp.tokenize_text(sentence))
# names = nlp.tokenize_text(names[0])
# print(names)
# print(nlp.find_gender('Francisco'))

# print(nlp.get_stop_words())
# print('\n')

# sentence = "an They My name is michael Francisco Barrera and I'm 23 years old"
# # print(sentence)
# # print('\n')
# sentence = nlp.tokenize_text(sentence)
# print(sentence)
# print('\n')
# sentence = nlp.clear_empty_words(sentence)
# print(sentence)
# print('\n')
# sentence = nlp.find_proper_nouns(sentence)

# print('Gender features---------')
# name = 'Francisco'
# print('Name: ' + name)
# print(nlp.gender_features(name))
#
# labeled_names = ([(name, 'male') for name in names.words('male.txt')] + [(name, 'female') for name in names.words('female.txt')])
# import random
# import nltk
# # random.shuffle(labeled_names)
# featuresets = [(nlp.gender_features(n), gender) for (n, gender) in labeled_names]
# train_set = featuresets[1000:]
# classifier = nltk.NaiveBayesClassifier.train(train_set)
# print(classifier.classify(nlp.gender_features('Katherine')))
# import nltk
# qry = "who is Francisco "
# tokens = nltk.tokenize.word_tokenize(qry)
# pos = nltk.pos_tag(tokens)
# sentt = nltk.ne_chunk(pos, binary = False)
# print(sentt)
# # for word in sentt:
# #     print(word)
# person = []
# for subtree in sentt.subtrees(filter=lambda t: t.label() == 'PERSON'):
#     for leave in subtree.leaves():
#         person.append(leave)
# print ("person=", person[0])
# if len(person) > 1: #avoid grabbing lone surnames
#     for part in person:
#         name += part + ' '
#     if name[:-1] not in person_list:
#         person_list.append(name[:-1])
#     name = ''
# person = []
# print(person)

# names = get_human_names(text)
# print("LAST, FIRST")
# for name in names:
#     last_first = HumanName(name).last + ', ' + HumanName(name).first
#     print(last_first)
