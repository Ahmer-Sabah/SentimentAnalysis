# -*- coding: utf-8 -*-
"""NLP_Assignment_2_1094343.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1GORtJJ9pRHRRAZrZ9g2UZEfqrcrCbh9r
"""

#IMPORT LIBRARIES

!python -m spacy download en
!pip install torch
import spacy
spacy.load('en')
import torch
from torchtext import data
from torchtext import datasets
import random                                        # will use this to set random seed and shuffle our data
import pandas as pd                                  # Import the pandas library to read our dataset 
from sklearn.model_selection import train_test_split # Get the train/test split package from sklearn for preparing our dataset to # train and test the model with 
import numpy as np                                   # Import the numpy library to work with and manipulate the data
import torch
from torchtext import data
import spacy
spacy.load('en')
import nltk 
from nltk.tokenize import word_tokenize              # For breaking sentences into words
nltk.download('punkt') 
nltk.download('stopwords')                           # For stop-words removal
nltk.download('movie_reviews')                       # import the movie reviews dataset
from nltk.corpus import movie_reviews 
nltk.download('wordnet')                             #For lemmatizing

from google.colab import drive                      # to access our Google drive and save our trained model to it.
drive.mount('/content/gdrive')
#import os
#os.chdir("gdrive/My Drive/")

df = pd.read_csv('https://raw.githubusercontent.com/cacoderquan/Sentiment-Analysis-on-the-Rotten-Tomatoes-movie-review-dataset/master/train.tsv', sep='\t') # reads our tab separated dataset file directly from the url.
df.head()

df = df.sample(frac=1).reset_index(drop=True) # checking a random sample row, returns float value * length of data frame values
df.head()

X_train, X_test, Y_train, Y_test = train_test_split(df ['Phrase'], df ['Sentiment'], test_size=0.3, random_state=2003) #Split dataset into Training and Testing as 70:30 with random state = 2003
documents=[]                                                      #we store the reviews in this list variable, with each item as a tuple
X_train = np.array(X_train.values.tolist())                       #convert training dataset to arrays
Y_train = np.array(Y_train.values.tolist())
for i in range(len(X_train)):
  documents.append([list(word_tokenize(X_train[i])), Y_train[i]]) # converting sentence to list of words

X_test = np.array(X_test.values.tolist())                         #convert test dataset to arrays
Y_test = np.array(Y_test.values.tolist())
for i in range(len(X_test)):
  documents.append([list(word_tokenize(X_test[i])), Y_test[i]])   # converting sentence to list of words

documents[0]

from nltk.corpus import stopwords 
from nltk.stem import WordNetLemmatizer, PorterStemmer, LancasterStemmer 
porter = PorterStemmer() 
lancaster=LancasterStemmer() 
wordnet_lemmatizer = WordNetLemmatizer() 
stopwords_en = stopwords.words("english") #fetches the pre-built stop-words of english language vocabulary
punctuations="?:!.,;'\"-()"

#parameters to adjust to see the impact on outcome 
remove_stopwords = True   # removes stopwords
useStemming = False       # if set to True, performs stemming 
useLemma = False          # if set to True, performs lemmatization
removePuncs = True        # removes punctuations

for l in range(len(documents)):                   #For each review document 
  label = documents[l][1]                         #Save review label 
  tmpReview = []                                  #Placeholder list for new review 
  for w in documents[l][0]:                       #For each word this is review 
    newWord = w                                   #Set newWork to be the updated word 
    if remove_stopwords and (w in stopwords_en):  #if the word is a stopword & we want to remove stopwords 
      continue                                    #skip the word and don’t had it to the normalized review 
    if removePuncs and (w in punctuations):       #if the word is a punc. & we want to remove punctuations 
      continue                                    #skip the word and don’t had it to the normalized review 
    if useStemming:
      #if useStemming is set to True 
      #Use either one of the stemmers 
      #newWord = porter.stem(newWord) #User porter stemmer 
      newWord = lancaster.stem(newWord) #Use Lancaster stemmer 
    if useLemma: 
      newWord = wordnet_lemmatizer.lemmatize(newWord) 
    tmpReview.append(newWord)                     #Add normalized word to the tmp review 
  documents[l] = (tmpReview, label)             #Update the reviews list with clean review 
  documents[l] = (' '.join(tmpReview), label) 

print(documents[0])

df = pd.DataFrame(documents, columns=['text', 'sentiment']) 
df.head()

X_train, X_test, Y_train, Y_test = train_test_split(df['text'],  df['sentiment'], test_size=0.3, random_state=2003)

from sklearn.feature_extraction.text import CountVectorizer , TfidfVectorizer
from keras.utils import to_categorical
#Transform each text into a vector of word counts
vectorizer = TfidfVectorizer(max_features = 3000)#, # ngram_range=(1, 1)) 
X = vectorizer.fit_transform(df["text"]) 
Y = df['sentiment'] 
 
# convert datasets to numpy arrays
X_train = vectorizer.transform(X_train).toarray()
Y_train = Y_train 
X_test = vectorizer.transform(X_test).toarray()
Y_test = Y_test

Y_test

# IMPORT LIBRARIES TO BUILD OUR MODEL

import keras
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras.layers import Conv1D, MaxPooling1D
from keras import backend as K

# CALCULATE PERFORMNACE METRICS

 # calculate recall i.e TP/TP + FN
def metric_recall(y_true,y_pred):                             
  true_positives = K.sum(K.round(K.clip(y_true*y_pred,0,1)))
  possible_positives = K.sum(K.round(K.clip(y_true, 0,1)))
  recall = true_positives / (possible_positives + K.epsilon())
  return recall

 # calculate precision i.e. TP/ TP + FP
def metric_precision(y_true, y_pred):                         
  true_positives = K.sum(K.round(K.clip(y_true*y_pred, 0,1)))
  predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
  precision = true_positives / (predicted_positives + K.epsilon())
  return precision

 # calculate F1-Score i.e 2*(Recall * Precision) / (Recall + Precision)
def f1_score(y_true, y_pred):
  precision= metric_precision(y_true, y_pred)
  recall= metric_recall(y_true, y_pred)
  return 2*((precision*recall)/(precision+recall+K.epsilon()))

batch_size = 128
num_classes = 5
epochs = 10

X_train.shape
# Y_train = to_categorical(Y_train,5)
# y_test = to_categorical(y_test,5)

# convert vectors into matrix to perform cross entropy
Y_train = keras.utils.to_categorical(Y_train, num_classes)
Y_test = keras.utils.to_categorical(Y_test, num_classes)

Y_test

#create model
model = Sequential()
model.add(Conv1D(filters=64, kernel_size=3,
                 activation='relu',
                 input_shape=(3000,1)))                   # Convolutional layer with 64 output channels
model.add(Conv1D(128, kernel_size=3, activation='relu'))  # Convolutional layer with 128 output channels
model.add(Conv1D(128, kernel_size=3, activation='relu'))
model.add(Conv1D(128, kernel_size=3, activation='relu'))
model.add(Conv1D(128, kernel_size=3, activation='relu'))
model.add(Conv1D(128, kernel_size=3, activation='relu'))
model.add(MaxPooling1D(pool_size=2))                      # Pooling layer with a pool window size of 2 x 2
model.add(MaxPooling1D(pool_size=2))
model.add(MaxPooling1D(pool_size=2))
model.add(MaxPooling1D(pool_size=2))
model.add(MaxPooling1D(pool_size=2))
model.add(MaxPooling1D(pool_size=2))
model.add(Dropout(rate = 0.25))                          # perform drop-out regularization to handle over-fitting
model.add(Flatten())
#model.add(Dense(10, activation='relu')) 
model.add(Dense(num_classes, activation='softmax'))       # FC layer

# CALCULATE LOSS AND PERFORM OPTIMIZATION

model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adam(),
              metrics=['accuracy',f1_score, metric_precision, metric_recall]) # adam optimizer
#model.compile(loss=keras.losses.categorical_crossentropy,
#              optimizer=keras.optimizers.SGD(lr=0.02),
#              metrics=['accuracy',f1_score, metric_precision, metric_recall]) #SGD optimizer

# Reshape the arrays to better fit the model
X_train = X_train.reshape(X_train.shape[0], X_train.shape[1], 1)
X_test = X_test.reshape(X_test.shape[0], X_test.shape[1], 1)

#Train the model
model.fit(X_train, Y_train,
          batch_size=128,
          epochs=10)

# SAVE AND RELOAD MODEL

from keras.models import load_model

model.save('1094243_1dconv_cla.h5')

#model = load_model('1094243_1dconv_cla.h5')

# This method fetches all the evaluation metrics and calculates them for testing set and displays the results
def get_metrics (accuracy,f1_score,precision,recall):
  print('CNN Classifier model performance')
  print('Accuracy:', np.round(accuracy,4))
  print('Precision: ', np.round(precision,4))
  print("Recall:", np.round(recall,4 ))
  print("F1-score:", np.round(f1_score,4 ))
  # Test the model
loss, accuracy, f1_score, precision, recall = model.evaluate(X_test, Y_test, verbose=0)

get_metrics(accuracy,f1_score, precision, recall)