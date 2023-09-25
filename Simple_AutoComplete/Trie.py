#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 16 19:55:21 2023

@author: Michael Baker

"""

from CharacterNode import CharacterNode as CN
import pickle
from ASD_LSTM_Model import ASD_TF_Object

class Trie:
    '''
    The autocomplete algorithm of the assisted speech app will make use of a Trie data structure
    This class works in tandum with the CharacterNode class
    '''
    
    def __init__(self) -> None:
        '''
        Construct an instance of the AssistedSpeachApplication
        '''
        with open("./Wordlist_Spanish.txt",'r') as fid:
            lines = fid.readlines()
            fid.close()
        
        with open("./all_Words_from_web_scraping.txt",'r') as fid:
            lines2 = fid.readlines()
            fid.close()

        # load in the pickle file that contains the weights
        with open("word_weight_dict.pkl", 'rb') as f:
            self.word_dict = pickle.load(f)
        
        lines.extend(lines2)
        wordList = []
        for L in lines:
            L = L.strip() # remove newline characters
            wordList.append(L)
        
        self.wordSet = set(wordList)
        self.WordList = wordList
        self.Trie = CN("0")

        # Initialize a reference to the language model for the application
        self.ASD_NN = ASD_TF_Object()
        self.ASD_NN.restoreWeights('./Finalized_Model/ASD_LSTM_Weights')
        pass
    
    def buildTrie(self) -> CN:
        '''
        Load in a list of words and insert them into a trie structure 
        '''
        # create the root node trie
        RootTrie = CN("0")
        for L in self.WordList:
            # get rid of newline characters
            L = L.strip()
            
            # the word list I started with has common prefixes identified, so ignore those when building the trie
            if L.find('-') != -1:
                continue
            
            # some 'words' are actually phrases, so parce those out into words
            if len(L.split()) > 1:
                notL = L.split()
                for nL in notL:
                    self.__appendToTrie(Trie=RootTrie, inputWord=nL, weight=self.__getWeightofWord(nL))
                    
            else:   
                # put word to trie
                self.__appendToTrie(Trie=RootTrie, inputWord=L, weight=self.__getWeightofWord(L))
        
        self.Trie = RootTrie
        return RootTrie
    
    def buildEmptyTrie(self) -> CN:
        '''
        create an empty Trie object
        '''
        return CN("0")

    def __getWeightofWord(self, inputWord:str) -> float:
        '''
        Check if the input word exits in the word dict, if it does return the weight, otherwise return .1 NOTE: this value is arbitrary, might be worth looking into more later
        '''
        # this is the simple way NOTE: This does not check if the word exists in the set of words
        return(self.word_dict.get(inputWord,.1))


    def __appendToTrie(self, Trie:CN, inputWord:str, weight:float) -> None:
        # append word to trie
        for ind,char in enumerate(inputWord):
            indexOfChar = ord(char.lower()) - Trie.AValue
            try:
                if 0 == Trie.Alphabet[indexOfChar]:
                    # make a node
                    Trie.Alphabet[indexOfChar] = CN(char.lower())

                    # move the reference to the new node
                    Trie = Trie.Alphabet[indexOfChar]
                    
                else:
                    # if the node already exists move to that node
                    Trie = Trie.Alphabet[indexOfChar]

                if ind == len(inputWord)-1: # if the letter is at the end of the word add 1 to the end of word count and add the weight
                    Trie.wordend += 1
                    Trie.weight = weight
            except KeyError:
                #print(f"KeyError on the following character: {char.lower()} in word: {inputWord}")
                return
        
        return


    def searchTrie(self, Trie:CN, userStr:str) -> list:
        '''
        First of two functions that provides the bulk of the search funcionality of the App
            TODO: Make it so that the number of returned variables is initialized by the user elsewhere (i.e. not at this level)
        '''

        nReturns = 10
        # for every letter in the userStr traverse the Trie to find words that could be in the trie structure
        T = Trie
        
        
        for C in userStr:
            indexOfChar = ord(C.lower()) - T.AValue
            T = T.Alphabet[indexOfChar]
            if T == 0:
                print('No hay una palabra con esta prefijo ...')
                return(-1)
            else:
                continue
       
        # search through trie for all words that could come from the provided prefix
        out = self.__throughSearch(T, userStr,[])
        
        # Query the ASD_NN to get a list of the predicted words -- this list is limited in size to 50 words
        # not implemented here yet - still figuring out functional flow between classes
        '''
        # This code will maybe be used in the future to do the model query
        # search the array of words from the trie to see if they contian any shared elements
        trieWordSet = set([out[x][0] for x in range(nReturns)])
        nnWordSet = set(nnPredictions)
        commonWordSet = trieWordSet.intersection(nnWordSet)

        if commonWordSet:
            # if there are words in common, find their index in the out array

        '''
        out.sort(key=lambda x:x[1], reverse=True)

        # at this point the list contains n tuples of length 2 where index 0 is the word and index 1 is the weight
        # we only care for the words at this point

        return([out[x][0] for x in range(nReturns)])
    
   

        

    def __throughSearch(self, Trie:CN, inputStr:str, outList:list) -> list:
        '''
        look through the remaining levels of the trie and find words that are still incomplete
        Only return the top 10 results by weight
            TODO: Implement a way to track the highest weight path along a given substring
        '''

        for k in Trie.Alphabet.keys():
            # if there are no more characters, continue
            if Trie.Alphabet[k] == 0:
                continue

            else: 
                currentNode = Trie.Alphabet[k]
                if currentNode.wordend > 0:
                    OWS = inputStr + chr(currentNode.characterVal)
                    outList.append((OWS,currentNode.weight))

                OWS = inputStr + chr(currentNode.characterVal)
                self.__throughSearch(currentNode, OWS, outList)

        return(outList)
    