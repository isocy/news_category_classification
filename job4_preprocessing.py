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

encoder = LabelEncoder()
labeled_category_series = encoder.fit_transform(category_series)
print(labeled_category_series[:3])
