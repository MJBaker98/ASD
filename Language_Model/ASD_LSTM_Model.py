'''
Class that contains the model information and other necessary information for the 
implementation of the ASD language model
Properties
    - tfModel : tensorflow/keras sequential model 
    - tokenizer : keras tokenizer object with the vocab list and tokens
    - sequence_length : the size of the n-gram model

'''

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Embedding, Dropout
from tensorflow.keras.preprocessing.text import Tokenizer
from keras.utils import Sequence
import numpy as np
import tensorflow as tf
import pickle


class ASD_TF_Object:
    def __init__(self) -> None:
        '''
        Initialize the TF object - load necessary data

        TODO: come up with a more clever way to have the user interface with the class to assign things like sequence lengths and change paths
        '''
        self.sequence_length = 3 # the model implemented a 3-gram methodology to train, so retain that here to ensure proper input size dimensions

        # load tokenizer
        with open('./Finalized_Model/tokenizer.pickle', 'rb') as handle:
            self.tokenizer = pickle.load(handle)

        # create an instance of the model
        self.tfModel = self.__createModel(len(self.tokenizer.word_index)+1, 3)

    def __createModel(self,vocab_size, sequence_length):
        '''
        This function creates an empty model with the necessary layers and parameters
        '''
        model = Sequential()
        model.add(Embedding(vocab_size, 50, input_length=sequence_length))
        model.add(LSTM(500,return_sequences=True))
        model.add(Dropout(.2))
        model.add(LSTM(300,return_sequences=True))
        model.add(Dropout(.2))
        model.add(LSTM(100))
        #model.add(Dense(200, activation='relu'))
        model.add(Dense(vocab_size, activation='softmax'))
        model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

        return(model)
    
    def restoreWeights(self, path:str) -> None:
        '''
        function to restore weights from where they are saved 
        '''
        self.tfModel.load_weights(path)


    def queryModel(self,InputString:str) -> list:
        '''
        Create the functionality to call on the TF model created to predict words the user is typing
        '''
        Input_as_sequence = self.tokenizer.texts_to_sequence([InputString])[0]
        
        # append empty space to allow the model to predict for less than 3 word inputs
        # - TODO: look into how much this simplification effects the quality of results
        while len(test_sequence) < self.sequence_length:
            test_sequence = [0, *test_sequence]
        
        test_sequence = np.reshape(Input_as_sequence, (1, self.sequence_length))
        predictions = self.tfModel.predict(test_sequence)
        top50guesses_index = (-predictions[0]).argsort()[:50]
        top50guesses_words = [self.tokenizer.index_word[x] for x in top50guesses_index]

        return (top50guesses_words)