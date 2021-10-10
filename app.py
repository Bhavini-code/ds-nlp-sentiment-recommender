# -*- coding: utf-8 -*-
"""
Created on Wed Oct  6 17:03:29 2021

@author: bgadhiwala
"""

from flask import Flask,render_template,request
import pickle
import numpy as np
import pandas as pd


app = Flask(__name__)

@app.route('/')
def home():
	return render_template('index.html')

@app.route('/predict',methods=['POST'])
def predict():
    #tfidf = pickle.load(open('Tfidf_vectorizer.pkl','rb'))
    #chosen_model = pickle.load(open('LogisticRegression.pkl','rb'))
    user_final_rating=pickle.load(open('user_final_rating.pkl', 'rb'))
    product_popularity_sentiment_review=pickle.load(open('ProductPopularityWithName.pkl', 'rb'))
    
    if (request.method == 'POST'):
        user_name = request.form['Username']
        top20 = pd.DataFrame(user_final_rating.loc[user_name]).reset_index()
        top20.rename(columns={top20.columns[0]: "id", top20.columns[1]: "user_pred_rating" }, inplace = True)
        top20 = top20.sort_values(by='user_pred_rating', ascending=False)[0:20]
        
        product_popularity_sentiment_review.rename(columns={product_popularity_sentiment_review.columns[0]: "id", product_popularity_sentiment_review.columns[1]: "name", product_popularity_sentiment_review.columns[2]: "popularity" }, inplace = True)
        top20=top20.merge(product_popularity_sentiment_review, left_on='id', right_on='id')[['id','name', 'popularity']]
        improved_recommendations=top20.sort_values(by=['popularity'],ascending=False)
        output_top5=improved_recommendations['name'].to_list()[:5]
        #print(output_top5)
        output_text=''
        for num, item in enumerate(output_top5):
            output_text=output_text+str(num+1)+'.  '+item+str('\n')
            
        #output_text=''.join(output_top5)
    return render_template('index.html', prediction_text='The top 5 product recommendations for '+user_name+' are : ',prediction_item1= '1. '+ output_top5[0],prediction_item2='2. '+output_top5[1],prediction_item3='3. '+output_top5[2],prediction_item4='4. '+output_top5[3],prediction_item5='5. '+output_top5[4])



if __name__ == '__main__':
    app.debug = True
    app.run()
