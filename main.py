import codecs
import math
import re
from operator import itemgetter

s = "به نام خدا"

class TextSummarization:

    BigText = ""
    SmallText = ""

    TextMatrix = []
    OriginalTextMatrix = []
    StopWords = []
    ImportantWords = []

    MaxSizeOfSmallText = 0

    def ReadFileBigText(self):

        f = open("bigtext.txt", encoding="utf-8")
        self.BigText = f.read()

    #########################################

    def ReadFileStopWords(self):

        f = open("stopwords.txt", encoding="utf-8")
        temp = f.read()
        self.StopWords = temp.split('\n')

    #########################################

    def ReadFileImportantWords(self):

        f = open("importantwords.txt", encoding="utf-8")
        temp = f.read()
        self.ImportantWords = temp.split('\n')

    #########################################

    def ProcessWord(self, Word):

        ThisWord = {}
        Word = Word.strip()
        for char in Word:
            if char in "\n\t ؟:،!()":
                Word.replace(char, '')

        ThisWord["Value"] = Word
        ThisWord["Weight"] = 0
        return ThisWord

    #########################################

    def ProcessSentences(self, Sentence):

        ThisSentence = {}
        ThisSentence["Weight"] = 0
        ThisSentence["Value"] = []
        Sentence = Sentence.strip()
        Sentence = Sentence.split(' ');

        for Word in Sentence:
            ThisSentence["Value"].append(self.ProcessWord(Word))

        return ThisSentence

    #########################################

    def BuildMatrix(self):

        #حذف نمودن فاصله های اضافه به کمک عبارت منظم
        re.sub(' +', ' ', self.BigText)

        #متن ورودی را از جای نقطه ها میشکند و جمله ها را جدا می نماید
        Sentences = self.BigText.split('.')

        index = 0

        for Sentence in Sentences:
            self.OriginalTextMatrix.append({"Value": Sentence, "Index": index})
            index = index + 1

        for Sentence in Sentences:
            self.TextMatrix.append(self.ProcessSentences(Sentence))

        index = 0

        for Sentence in self.TextMatrix:
            Sentence["Index"] = index
            index = index + 1

    #########################################

    def Idf(self, Word):

        #تعداد جملاتی که شامل این کلمه می باشند

        cntr = 0
        for Sentence in self.TextMatrix:
            for W in Sentence["Value"]:
                if W["Value"] == Word["Value"]:
                    cntr = cntr + 1

        N = len(self.TextMatrix)

        return math.log(N/cntr ,10)

    #########################################

    def TF(self, Word, Sentence):

         #تعداد پر تکرار ترین کلمه در جمله

        MaxRepetitiveWordCount = 0
        for W in Sentence["Value"]:
            cntr = 0
            for W2 in Sentence["Value"]:
                if W["Value"] == W2["Value"]:
                    cntr = cntr + 1

            if cntr > MaxRepetitiveWordCount:
                MaxRepetitiveWordCount = cntr

        #تعداد تکرار کلمه مورد بررسی در جمله

        ThisWordCount = 0
        for W in Sentence["Value"]:
            if W["Value"] == Word["Value"]:
                ThisWordCount = ThisWordCount + 1

        return 0.5 + ((0.5 * ThisWordCount) / MaxRepetitiveWordCount)

    #########################################

    def Tf_Idf(self):
        for Sentence in self.TextMatrix:
            for Word in Sentence["Value"]:
                Word["Weight"] = Word["Weight"] + (self.TF(Word, Sentence) * self.Idf(Word))

    #########################################

    def SumWordsWeightForSentenceWeight(self):
        for Sentence in self.TextMatrix:
            for Word in Sentence["Value"]:
                Sentence["Weight"] = Sentence["Weight"] + Word["Weight"]

    #########################################

    def RemoveStopWords(self):
        for Sentence in self.TextMatrix:
            for Word in Sentence["Value"]:
                if Word["Value"] in self.StopWords:
                    Sentence["Value"].remove(Word)

    #########################################

    def SearchImportantWords(self):
        for Sentence in self.TextMatrix:
            for Word in Sentence["Value"]:
                if Word["Value"] in self.ImportantWords:
                    Word["Weight"] = Word["Weight"] + 1

    #########################################

    def CreateSmallText(self):

        SortedTextMatrix = sorted(self.TextMatrix, key=itemgetter('Weight'), reverse=True)

        index = 0
        indexes = []
        ResultText = []
        ResultTextSize = 0

        while int(ResultTextSize) < int(self.MaxSizeOfSmallText) and index < len(SortedTextMatrix):

            ThisSentence = SortedTextMatrix[index]

            if (len(ThisSentence["Value"]) + int(ResultTextSize)) <= int(self.MaxSizeOfSmallText):
                ResultText.append(ThisSentence)
                ResultTextSize = ResultTextSize + len(ThisSentence["Value"])

            index = index + 1

        for Sentence in ResultText:
            indexes.append(Sentence["Index"])

        for Sentence in self.OriginalTextMatrix:
            if Sentence["Index"] in indexes:
                self.SmallText = self.SmallText + Sentence["Value"] + "."

    #########################################

    def WriteFileSmallText(self):

        f = codecs.open("smalltext.txt", "w", "utf-8")
        f.write(self.SmallText)
        f.close()

#Start Of Project

TS = TextSummarization()

TS.ReadFileBigText()
TS.ReadFileStopWords()
TS.ReadFileImportantWords()
TS.BuildMatrix()
TS.RemoveStopWords()
TS.Tf_Idf()
TS.SearchImportantWords()
TS.SumWordsWeightForSentenceWeight()

TS.MaxSizeOfSmallText = input("حداکثر تعداد کلمات متن خروجی را وارد نمایید: ")

TS.CreateSmallText()

print(TS.SmallText)
TS.WriteFileSmallText()
