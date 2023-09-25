import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding
from keras.utils import Sequence
from ASD_LSTM_Model import ASD_TF_Object
import pickle

class SequenceDataGenerator(Sequence):
    def __init__(self, sequence_data, one_hot_classes, batch_size, seq_length, vocab_length):
        self.data = sequence_data
        self.targets = one_hot_classes
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.vocab_size = vocab_length

    def __len__(self):
        return int(np.ceil(len(self.data) / float(self.batch_size)))

    def __getitem__(self, idx):
        batch_data = self.data[idx * self.batch_size:(idx + 1) * self.batch_size]
        batch_targets = self.targets[idx * self.batch_size:(idx + 1) * self.batch_size]

        X = np.zeros((len(batch_data), self.seq_length))
        y = np.zeros((len(batch_data), 1))

        for i, sequence in enumerate(batch_data):
            truncated_seq = sequence[:self.seq_length]
            X[i, :len(truncated_seq)] = truncated_seq
            y[i] = batch_targets[i]

        return X, to_categorical(y, num_classes = self.vocab_size)

total_Text_Link = '//Users//michael//Documents//Programming//Python//Assisted_Speech_Device//Web_Scraping//Total_Text.txt'
tt_fid = open(total_Text_Link,'r')
TotalText = tt_fid.read()
tt_fid.close()

# Generate input sequences and their corresponding next words
sequence_length = 3
input_sequences = []
next_words = []

###########
###########
# Cut out a slice of the data I am using to train and train a model on that to see how it performs
all_TotalText = TotalText
#TotalText = TotalText[0:10000000]
TotalText = TotalText[0:10000000]

###########
tokenizer = Tokenizer()
tokenizer.fit_on_texts([TotalText])
tokens = tokenizer.texts_to_sequences([TotalText])[0]

# saving
with open('tokenizer.pickle', 'wb') as handle:
    pickle.dump(tokenizer, handle, protocol=pickle.HIGHEST_PROTOCOL)

for i in range(len(tokens) - sequence_length):
    input_sequences.append(tokens[i:i + sequence_length])
    next_words.append(tokens[i + sequence_length])

# Convert input sequences and next words to numerical representation
# input_sequences = tokenizer.texts_to_sequences(input_sequences)
# next_words = tokenizer.texts_to_sequences([next_words])[0]

# Convert input sequences and next words to one-hot encoded vectors
vocab_size = len(tokenizer.word_index) + 1

# Create the LSTM model
vocab_size = len(tokenizer.word_index) + 1
ASD_NN = ASD_TF_Object()


# make sequential data
nEpochs = 150

# Set the batch size and number of training steps
batch_size = 1000

# set hardware to GPU
tf.device('/gpu:0')

# Create training generator
trainingGenerator = SequenceDataGenerator(np.array(input_sequences),np.array(next_words),batch_size,sequence_length,vocab_size)

# create a callback that saves off model weights
cp_callback = tf.keras.callbacks.ModelCheckpoint('training_1.ckpt',save_weights_only=True,verbose=1)

# Fit model
ASD_NN.tfModel.fit(trainingGenerator,epochs=nEpochs,callbacks=[cp_callback])

# Save off final model weights to a separate file
ASD_NN.tfModel.save_weights('./Finalized_Model/ASD_LSTM_Weights')