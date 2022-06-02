import streamlit as st
import numpy as np
import pandas as pd
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import bs4
from bs4 import BeautifulSoup as bs
import requests



nltk.download('stopwords')
from nltk.stem.porter import PorterStemmer
import re
from nltk.corpus import stopwords
import warnings
warnings.filterwarnings('ignore')

ps = PorterStemmer()

def clean_text(text):
    text = re.sub('[^a-zA-Z]', " ", text)
    text = text.lower()
    text = text.split()
    text = [ps.stem(word) for word in text if word not in stopwords.words("english")]
    text = ' '.join(text)
    return text

st.title("AMAZON PRODUCT SENTIMENT ANALYSIS")
st.header("Instructions")
st.markdown("1.You have paste review page link")
st.markdown("2.please link of all review's page")

url = st.text_input("paste url Here")
reviewlist = []
submitted =st.button("submit")
if submitted:
    def get_soup(url):
        r = requests.get("https://www.amazon.in/boAt-Smartwatch-Multiple-Monitoring-Resistance/product-reviews/B096VF5YYF/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")
        soup = bs(r.text, "html.parser")
        return soup

    def get_reviews(soup):
        reviews = soup.find_all('div', {'data-hook':'review'})
        try:
            for item in reviews:
                review = {
                'tiltle':item.find('a',{'data-hook':'review-title'}).text.strip(),
                'rating':  float(item.find('i', {'data-hook': 'review-star-rating'}).text.replace('out of 5 stars', '').strip()),
                'review': item.find('span', {'data-hook': 'review-body'}).text.strip(),
                }
                reviewlist.append(review)
        except:
            pass

    for x in range (1,10):
        soup = get_soup(f"https://www.amazon.in/boAt-Smartwatch-Multiple-Monitoring-Resistance/product-reviews/B096VF5YYF/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")
        get_reviews(soup)
        if not soup.find('li', {'class': 'a-disabled a-last'}):
            pass
        else:
            break
        
data = pd.DataFrame(reviewlist)
st.dataframe(data)
                
if st.button('Click for Result'):  
     data['Cleaned_Text']=data['review'].apply(clean_text)
     sid = SentimentIntensityAnalyzer()
     data["Vader_Score"] = data["Cleaned_Text"].apply(lambda review:sid.polarity_scores(review))
     data["Vader_Compound_Score"]  = data['Vader_Score'].apply(lambda score_dict: score_dict['compound'])
     data["Result"] = data["Vader_Compound_Score"].apply(lambda c: 'positive' if c > 0 else ('negative' if c < 0 else 'neutral'))
     st.bar_chart(df.Result.value_counts())          
