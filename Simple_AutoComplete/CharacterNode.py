

class CharacterNode:
    # node for the trie for autocomplete algorithm
    def __init__(self, inputChar) -> None:
        self.characterVal = ord(inputChar)
        self.AValue = ord('a')
        self.wordend = int()
        self.weight = float()
        chars = [x for x in range(26)]
        counts = [0 for x in range(26)] 
        self.Alphabet = {x:y for (x,y) in zip(chars,counts)}
        self.Alphabet.update({225-self.AValue:0}) # á
        self.Alphabet.update({241-self.AValue:0}) # ñ
        self.Alphabet.update({233-self.AValue:0}) # é
        self.Alphabet.update({237-self.AValue:0}) # í
        self.Alphabet.update({243-self.AValue:0}) # ó
        self.Alphabet.update({250-self.AValue:0}) # ú
        self.Alphabet.update({252-self.AValue:0}) # ü