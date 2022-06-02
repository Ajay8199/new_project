import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import textblob
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
import http
import bs4
import requests



nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
import re
from nltk.corpus import stopwords

ps = PorterStemmer()

def clean_text(text):
    text = re.sub('[^a-zA-Z]', " ", text)
    text = text.lower()
    text = text.split()
    text = [ps.stem(word) for word in text if word not in stopwords.words("english")]
    text = ' '.join(text)
    return text

st.title("Identifying Review's Rating")
st.header("Instructions")
st.markdown("1.Review column's name should be **Text**")
st.markdown("2.Rating column's name should be **Star**")
st.markdown("3.Rating range should be 0-5")

url = st.text("")
reviewlist = []
source = http.client.HTTPconnection(url)
submitted =st.button("submit")
try:
    if submitted:
        def get_soup(url):
            r = requests.get(url)
            soup = beautifulsoup(r.text, "text.parser")
            return soup

        def get_reviews(soup):
            reviews = soup.fing_all('div', {'data-hook':'review'})
            try:
                for item in reviews:
                    review = {
                    'tiltle':item.find('a',{'data-hook':'review-title'}).text.strip(),
                    'rating':  float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
                    'body': item.find('span', {'data-hook': 'review-body'}).text.strip(),
                    }
                    reviewlist.append(review)
            except:
                pass

        soup=get_soup(url)
        get_reviews(soup)
        print(len(reviewlist))

        for x in range (1,1999):
            soup = get_soup(f(url))
            print(f'Getting page: {x}')
            get_reviews(soup)
            print(len(reviewlist))
            if not soup.find('li', {'class': 'a-disabled a-last'}):
                pass
            else:
                break
                data = pd.DataFrame(reviewlist)
except:
    break
                
if st.button('Click for Result'):  
     data["Cleaned_Text"] = data["body"].apply(lambda x: clean_text(str(x)))
     sid = SentimentIntensityAnalyzer()
     data["Vader_Score"] = data["Cleaned_Text"].apply(lambda review:sid.polarity_scores(review))
     data["Vader_Compound_Score"]  = data['Vader_Score'].apply(lambda score_dict: score_dict['compound'])
     data["Result"] = data["Vader_Compound_Score"].apply(lambda c: 'positive' if c > 0 else ('negative' if c < 0 else 'neutral'))
     st.bar_chart(df.Result.value_counts())          
