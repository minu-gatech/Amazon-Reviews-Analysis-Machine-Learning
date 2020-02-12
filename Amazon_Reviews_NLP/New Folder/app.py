import os

import pandas as pd
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template,url_for,request
from flask_sqlalchemy import SQLAlchemy
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.externals import joblib


#Naive Bayes Model
amazon= pd.read_csv("static/data/amazon_Reviews.csv")
X=amazon['reviews.text'].values.astype('U')
y=amazon['review_rating']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.23, random_state=42)

vectorizer= TfidfVectorizer()
X_train_vectors=vectorizer.fit_transform(X_train)
X_test_vectors = vectorizer.transform(X_test)


model_nb = MultinomialNB()
model_nb.fit(X_train_vectors,y_train)
model_nb.predict(X_test_vectors)

app = Flask(__name__)

filename = 'NaiveBayesModel.pkl'
joblib.dump(model_nb, filename)
NB_model = open('NaiveBayesModel.pkl','rb')
NB_model_loaded = joblib.load(NB_model)

# ---------------------------------------------------------------------------------

# amazon= pd.read_csv("static/data/amazon_Reviews.csv")
# X=amazon['reviews.text'].values.astype('U')
# y=amazon['review_rating']
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.23, random_state=42)

# vectorizer= TfidfVectorizer()
# X_train_vectors=vectorizer.fit_transform(X_train)
# X_test_vectors = vectorizer.transform(X_test)


# model_log = LogisticRegression()
# model_log.fit(X_train_vectors,y_train)
# model_log.predict(X_test_vectors)

# app = Flask(__name__)

# filename = 'LogisticRegressionModel.pkl'
# joblib.dump(model_log, filename)
# LogReg_model = open('LogisticRegressionModel.pkl','rb')
# LogReg_model_loaded = joblib.load(LogReg_model)

# ---------------------------------------------------------------------------------


# rendering templates for all html pages
@app.route("/")
def index():
#     """Return the homepage."""
    return render_template("index.html")


@app.route("/predictor",methods=['POST'])
def predict():
     if request.method == "POST":
          message = request.form["message"]
          data = [message]
          vect = vectorizer.transform(data)
          my_prediction = NB_model_loaded.predict(vect)
          if my_prediction == 'POSITIVE' :
               prediction = "This review is POSITIVE"

          if my_prediction == 'NEGATIVE' :
               prediction = "This review is NEGATIVE"

	
	
     return render_template('predictor.html',prediction = prediction, message= message)


# ---------------------------------------------------------------------------------
# # Log Reg Model
# @app.route("/")
# def index():
# #     """Return the homepage."""
#     return render_template("index.html")


# @app.route("/predictor",methods=['POST'])
# def predict():
#      if request.method == "POST":
#           message = request.form["message"]
#           data = [message]
#           vect = vectorizer.transform(data)
#           my_prediction = LogReg_model_loaded.predict(vect)
#           if my_prediction == 'POSITIVE' :
#                prediction = "This review is POSITIVE"

#           if my_prediction == 'NEGATIVE' :
#                prediction = "This review is NEGATIVE"

	
	
#      return render_template('predictor.html',prediction = prediction, message= message)



@app.route("/data")
def datatabicon():
     return render_template("data_table.html")



@app.route("/precision")
def precisionicon():
     return render_template("precision.html")


@app.route("/predictor")
def predictoricon():
     return render_template("predictor.html")

@app.route("/model")
def modelicon():
     return render_template("model.html")

@app.route("/visual")
def visualicon():
     return render_template("visualization.html") 

if __name__ == "__main__":
     app.run(debug=True)
    