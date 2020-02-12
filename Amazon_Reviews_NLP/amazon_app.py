from flask import Flask,render_template,url_for,request
import pandas as pd 
import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.externals import joblib


app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():

	amazon= pd.read_csv('amazon_Reviews.csv')

	X1=amazon['reviews.text'].values.astype('U')
	y1=amazon['review_rating']

	X1_train, X1_test, y1_train, y1_test = train_test_split(X1, y1, test_size=0.33, random_state=42)
	
	vectorizer= TfidfVectorizer()
	X1_train_vectors=vectorizer.fit_transform(X1_train)
	X1_test_vectors = vectorizer.transform(X1_test)
	

	model_nb = MultinomialNB()
	model_nb.fit(X1_train_vectors,y1_train)
	model_nb.predict(X1_test_vectors)

	filename = 'NaiveBayesModel.pkl'
	joblib.dump(model_nb, filename)
	NB_model = open('NaiveBayesModel.pkl','rb')
	NB_model_loaded = joblib.load(NB_model)

	#Alternative Usage of Saved Model
	# joblib.dump(clf, 'NB_spam_model.pkl')
	# NB_spam_model = open('NB_spam_model.pkl','rb')
	# clf = joblib.load(NB_spam_model)

	if request.method == 'POST':
		message = request.form['message']
		data = [message]
		vect = vectorizer.transform(data).toarray()
		my_prediction = NB_model_loaded.predict(vect)
	return render_template('result.html',prediction = my_prediction)



if __name__ == '__main__':
	app.run(debug=True)