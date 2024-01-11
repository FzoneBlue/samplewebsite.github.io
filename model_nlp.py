import nltk
from nltk.stem import WordNetLemmatizer
import json
import pickle
import numpy as np
from keras.models import Sequential
from keras.layers import Embedding, LSTM, Dense, Flatten
from keras.optimizers import SGD
import random

nltk.download('punkt')
nltk.download('wordnet')

# Instantiate the lemmatizer
lemmatizer = WordNetLemmatizer()

# Load and preprocess the data
words = []
classes = []
documents = []
ignore_words = ['?', '!']
data_file = open('masakan.json').read()
intents = json.loads(data_file)

for intent in intents['intents']:
    for pattern in intent['patterns']:
        # Tokenize each word
        w = nltk.word_tokenize(pattern)
        words.extend(w)
        # Add documents to the corpus
        documents.append((w, intent['tag']))

        # Add to the classes list
        if intent['tag'] not in classes:
            classes.append(intent['tag'])

# Lemmatize and lowercase each word and remove duplicates
words = [lemmatizer.lemmatize(w.lower()) for w in words if w not in ignore_words]
words = sorted(list(set(words)))

# Sort classes
classes = sorted(list(set(classes)))

# Create training data
training = []
output_empty = [0] * len(classes)

for doc in documents:
    bag = []
    pattern_words = doc[0]
    pattern_words = [lemmatizer.lemmatize(word.lower()) for word in pattern_words]

    for w in words:
        bag.append(1) if w in pattern_words else bag.append(0)

    output_row = list(output_empty)
    output_row[classes.index(doc[1])] = 1

    training.append([bag, output_row])

random.shuffle(training)
training = np.array(training)
train_x = list(training[:, 0])
train_y = list(training[:, 1])

# Create and compile the LSTM model
# Create and compile the LSTM model
model = Sequential()
model.add(Embedding(len(words), 256, input_length=len(train_x[0])))
model.add(LSTM(256))  # Replace the Flatten and Dense layers with an LSTM layer
model.add(Dense(len(train_y[0]), activation='softmax'))
model.summary()
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
model.fit(np.array(train_x), np.array(train_y), epochs=100, batch_size=32, verbose=1)

# Save the model
model.save('model.h5')

print("Model created and trained.")
