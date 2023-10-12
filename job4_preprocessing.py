import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from konlpy.tag import Okt
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.utils import to_categorical
import pickle

pd.set_option('display.unicode.east_asian_width', True)
df_title_category = pd.read_csv('./crawling_data/naver_all_news.csv')

title_series = df_title_category['title']
category_series = df_title_category['category']

label_encoder = LabelEncoder()
labeled_category = label_encoder.fit_transform(category_series)
labels = label_encoder.classes_

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

tokenizer = Tokenizer()
tokenizer.fit_on_texts(title_series)
tokenized_titles = tokenizer.texts_to_sequences(title_series)
word_cnt = len(tokenizer.word_index)

token_max = 0
for tokenized_title in tokenized_titles:
    if len(tokenized_title) > token_max:
        token_max = len(tokenized_title)
tokenized_titles = pad_sequences(tokenized_titles, token_max)

with open('./models/label_encoder.pickle', 'wb') as f_labelEncoder:
    pickle.dump(label_encoder, f_labelEncoder)
with open('./models/tokenizer.pickle', 'wb') as f_tokenizer:
    pickle.dump(tokenizer, f_tokenizer)

train_titles, test_titles, train_categories, test_category = train_test_split(
    tokenized_titles, oneHotEncoded_category, test_size=0.2)

dataset = train_titles, test_titles, train_categories, test_category
np.save('./crawling_data/news_dataset_tokenMax_{}_wordCnt_{}'
        .format(token_max, word_cnt), dataset)
