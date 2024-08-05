#The following storage method makes use redis, a no-SQL database tool.
import redis
import json
import zlib

class RedisVocabStore:

    def __init__(self):
        self.defaultTokenizerIDs = ["Tokenizer_1","Tokenizer_2","Tokenizer_3","Tokenizer_4","Tokenizer_5","Tokenizer_6","Tokenizer_7","Tokenizer_8","Tokenizer_9","Tokenizer_10","Tokenizer_11","Tokenizer_12","Tokenizer_13","Tokenizer_14","Tokenizer_15","Tokenizer_16","Tokenizer_17","Tokenizer_18","Tokenizer_19","Tokenizer_20"]
        self.storedTokenIDs = []
        self.dbClientObj = redis.Redis(host='localhost',port=6379,db=0)

    #Data Pre-Processing/Preparation
    def vocabToCompJson(self,trainedVocab):
        serialisedVocab = json.dump(trainedVocab)
        compVocab = zlib.compress(serialisedVocab.encode('utf-8'))
        return compVocab
    
    def compJsonToVocab(self,encodedCompVocab):
        deserialisedVocab = zlib.decompress(encodedCompVocab)
        decodedVocab = deserialisedVocab.decode('utf-8')
        tokenizerVocab = json.loads(decodedVocab)
        return tokenizerVocab

    def assignVocabKey(self,chosenTokenizerName):
        assignedName = ''
        if (chosenTokenizerName == 'noChanceOfaUserNamingItThis'):
            assignedName = self.defaultTokenizerIDs[0]
            self.defaultTokenizerIDs.pop(0)
        else:
            assignedName = chosenTokenizerName
        
        return assignedName
    
    def saveTokenizer(self, trainedVocab, tokenizerName ='noChanceOfaUserNamingItThis'):
        jsonFormatVocab = self.vocabToCompJson(trainedVocab)
        tokenizerObjKey = self.assignVocabKey(tokenizerName)
        self.dbClientObj.set(tokenizerObjKey,jsonFormatVocab)
        self.storedTokenIDs.append(tokenizerObjKey)
    
    def retrieveTokenizer(self,selectedTokenIDIndex):
        tokenizerObjKey = self.storedTokenIDs[selectedTokenIDIndex]
        storedTokenizer = self.dbClientObj.get(tokenizerObjKey)
        processedTokenizer = self.compJsonToVocab(storedTokenizer)
        return processedTokenizer
