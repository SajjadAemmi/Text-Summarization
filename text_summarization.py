import math
import re
from operator import itemgetter


class TextSummarization:
    def __init__(self, input_file_name, stop_words_file_name, important_words_file_name, output_file_name):
        self.input_file_name = input_file_name
        self.stop_words_file_name = stop_words_file_name
        self.important_words_file_name = important_words_file_name
        self.output_file_name = output_file_name

        self.BigText = self.read_input_file()
        self.StopWords = self.read_stop_words_file()
        self.ImportantWords = self.read_important_words_file()
        self.SmallText = ""

        self.TextMatrix = []
        self.OriginalTextMatrix = []

        self.MaxSizeOfSmallText = 0

    def read_input_file(self) -> str:
        f = open(self.input_file_name, encoding="utf-8")
        result = f.read()
        return result

    def read_stop_words_file(self) -> list[str]:
        f = open(self.stop_words_file_name, encoding="utf-8")
        result = f.read().split('\n')
        return result

    def read_important_words_file(self) -> list[str]:
        f = open(self.important_words_file_name, encoding="utf-8")
        result = f.read().split('\n')
        return result

    def write_output_file(self):
        f = open(self.output_file_name, "w", encoding="utf-8")
        f.write(self.SmallText)
        f.close()

    def process_word(self, Word):
        this_word = {}
        Word = Word.strip()
        for char in Word:
            if char in "\n\t ؟:،!()":
                Word.replace(char, '')

        this_word["Value"] = Word
        this_word["Weight"] = 0
        return this_word

    def ProcessSentences(self, Sentence):
        ThisSentence = {}
        ThisSentence["Weight"] = 0
        ThisSentence["Value"] = []
        Sentence = Sentence.strip()
        Sentence = Sentence.split(' ')

        for Word in Sentence:
            ThisSentence["Value"].append(self.process_word(Word))

        return ThisSentence

    def build_matrix(self):
        # حذف نمودن فاصله های اضافه به کمک عبارت منظم
        re.sub(' +', ' ', self.BigText)

        # متن ورودی را از جای نقطه ها میشکند و جمله ها را جدا می نماید
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

    def Idf(self, Word):
        # تعداد جملاتی که شامل این کلمه می باشند

        cntr = 0
        for Sentence in self.TextMatrix:
            for W in Sentence["Value"]:
                if W["Value"] == Word["Value"]:
                    cntr = cntr + 1

        N = len(self.TextMatrix)

        return math.log(N/cntr, 10)

    def TF(self, Word, Sentence):
        # تعداد پر تکرار ترین کلمه در جمله

        MaxRepetitiveWordCount = 0
        for W in Sentence["Value"]:
            cntr = 0
            for W2 in Sentence["Value"]:
                if W["Value"] == W2["Value"]:
                    cntr = cntr + 1

            if cntr > MaxRepetitiveWordCount:
                MaxRepetitiveWordCount = cntr

        # تعداد تکرار کلمه مورد بررسی در جمله

        this_wordCount = 0
        for W in Sentence["Value"]:
            if W["Value"] == Word["Value"]:
                this_wordCount = this_wordCount + 1

        return 0.5 + ((0.5 * this_wordCount) / MaxRepetitiveWordCount)

    def Tf_Idf(self):
        for Sentence in self.TextMatrix:
            for Word in Sentence["Value"]:
                Word["Weight"] = Word["Weight"] + \
                    (self.TF(Word, Sentence) * self.Idf(Word))

    def sum_words_weight_for_sentence_weight(self):
        for Sentence in self.TextMatrix:
            for Word in Sentence["Value"]:
                Sentence["Weight"] = Sentence["Weight"] + Word["Weight"]

    def RemoveStopWords(self):
        for Sentence in self.TextMatrix:
            for Word in Sentence["Value"]:
                if Word["Value"] in self.StopWords:
                    Sentence["Value"].remove(Word)

    def SearchImportantWords(self):
        for Sentence in self.TextMatrix:
            for Word in Sentence["Value"]:
                if Word["Value"] in self.ImportantWords:
                    Word["Weight"] = Word["Weight"] + 1

    def CreateSmallText(self):
        SortedTextMatrix = sorted(
            self.TextMatrix, key=itemgetter('Weight'), reverse=True)

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
