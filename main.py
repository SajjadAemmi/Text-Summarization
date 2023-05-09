import argparse
from text_summarization import TextSummarization


parser = argparse.ArgumentParser()
parser.add_argument("--input", default="io/input/big_text.txt", type=str, help="input big text")
parser.add_argument("--stop-words", default="io/input/stop_words.txt", type=str, help="input stop words")
parser.add_argument("--important-words", default="io/input/important_words.txt", type=str, help="input important words")
parser.add_argument("--output", default="io/output/small_text.txt", type=str, help="output small text")
args = parser.parse_args()


if __name__ == "__main__":
    TS = TextSummarization(args.input, args.stop_words, args.important_words, args.output)

    TS.build_matrix()
    TS.RemoveStopWords()
    TS.Tf_Idf()
    TS.SearchImportantWords()
    TS.sum_words_weight_for_sentence_weight()
    TS.MaxSizeOfSmallText = input("حداکثر تعداد کلمات متن خروجی را وارد نمایید: ")
    TS.CreateSmallText()
    print(TS.SmallText)
    TS.write_output_file()
