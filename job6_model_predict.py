import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle
from tensorflow.keras.models import load_model

df = pd.read_csv('./crawling_data/naver_headline_news_20231012.csv')
print(df.head())
df.info()

title_series = df['title']
category_series = df['category']

with open('./models/label_encoder.pickle', 'rb') as f_labelEncoder:
    label_encoder = pickle.load(f_labelEncoder)
labeled_category = label_encoder.transform(category_series)
label = label_encoder.classes_

oneHotEncoded_category = to_categorical(labeled_category)

okt = Okt()
for idx in range(len(title_series)):
    title_series[idx] = okt.morphs(title_series[idx], stem=True)

df_stopword = pd.read_csv('./stopwords.csv', index_col=0)
for idx in range(len(title_series)):
    words = []
    for word_idx in range(len(title_series[idx])):
        word = title_series[idx][word_idx]
        if len(word) > 1 and word not in list(df_stopword['stopword']):
            words.append(word)
    title_series[idx] = ' '.join(words)

with open('./models/tokenizer.pickle', 'rb') as f_tokenizer:
    tokenizer = pickle.load(f_tokenizer)
tokenized_titles = tokenizer.texts_to_sequences(title_series)
for tokenized_title_idx in range(len(tokenized_titles)):
    if len(tokenized_titles[tokenized_title_idx]) > 20:
        tokenized_titles[tokenized_title_idx] = tokenized_titles[tokenized_title_idx][:20]
tokenized_titles = pad_sequences(tokenized_titles, 20)

model = load_model('./models/news_category_classification_model_0.723.h5')
predict_results = model.predict(tokenized_titles)
predicts = []
for predict_result in predict_results:
    first_predict = label[np.argmax(predict_result)]
    predict_result[np.argmax(predict_result)] = 0
    second_predict = label[np.argmax(predict_result)]
    predicts.append([first_predict, second_predict])
df['predict'] = predicts
print(df)

df['is_correct'] = 0
for idx in range(len(df)):
    if df.loc[idx, 'category'] in df.loc[idx, 'predict']:
        df.loc[idx, 'is_correct'] = 1
print(df['is_correct'].value_counts())
print(df['is_correct'].value_counts() / len(df) * 100)
for idx in range(len(df)):
    if df['category'][idx] not in df['predict'][idx]:
        print(df.iloc[idx])
