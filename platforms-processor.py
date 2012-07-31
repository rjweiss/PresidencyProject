__author__ = 'Rebecca'

import nltk
import pymongo
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.probability import FreqDist

def process():
    mongo = pymongo.Connection('localhost', 27017)
    db = mongo.platforms
    collection = db.platforms
    documents = collection.find()

    for document in documents:
        doc_id = document['_id']
        document['tokens'] = pos_tag(word_tokenize(document['text']))
        print(document)
        collection.update(
                {'_id': doc_id},
                {'$set' : document},
                upsert = False
        )