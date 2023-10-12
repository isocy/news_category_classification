import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.models import *
from tensorflow.keras.layers import *

train_titles, test_titles, train_categories, test_categories = np.load(
    './crawling_data/news_dataset_tokenMax_20_wordCnt_11994.npy',
    allow_pickle=True)

model = Sequential([
    Embedding(11994 + 1, 300, input_length=20),
    Conv1D(32, kernel_size=5, padding='same', activation='relu'),
    MaxPooling1D(pool_size=1),
    LSTM(128, activation='tanh', return_sequences=True),
    Dropout(0.3),
    LSTM(64, activation='tanh', return_sequences=True),
    Dropout(0.3),
    LSTM(64, activation='tanh'),
    Dropout(0.3),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(6, activation='softmax')
])
model.summary()

model.compile(optimizer='adam', loss='categorical_crossentropy',
              metrics=['accuracy'])
fit_hist = model.fit(train_titles, train_categories, batch_size=128, epochs=10,
                     validation_data=(test_titles, test_categories))
plt.plot(fit_hist.history['val_accuracy'], label='validation accuracy')
plt.plot(fit_hist.history['accuracy'], label='accuracy')
plt.legend()
plt.show()

model.save('./models/news_category_classification_model_{}.h5'
           .format(round(fit_hist.history['val_accuracy'][-1], 3)))
