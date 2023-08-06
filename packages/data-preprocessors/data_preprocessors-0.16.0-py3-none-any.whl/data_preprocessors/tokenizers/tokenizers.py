import nltk
from bnlp import NLTKTokenizer


class Tokenizers:
    def __init__(self):
        self.file_path = ""
        self.modified_file_path = ""
        self.paragraph = ""
        self.sentence = ""

    def split_paragraph_file(file_path="", modified_file_path=""):
        """
        This function split a English paragraph into sentences
        """
        with open(file_path, "r") as fp:
            data = fp.read()
            mylist = nltk.tokenize.sent_tokenize(data)

        # Converting list to text file
        with open(modified_file_path, "w") as new_file:
            for listitem in mylist:
                new_file.write("%s\n" % listitem)

    def split_paragraph(paragraph=""):
        """
        This function split a English Paragraph into sentences
        """
        sent_tokens = nltk.tokenize.sent_tokenize(paragraph)
        return sent_tokens

    def split_sentence(sentence):
        """
        This function split a English Sentence into words
        """
        word_tokens = nltk.tokenize.word_tokenize(sentence)
        return word_tokens

    def split_bangla_paragraph_file(file_path="", modified_file_path=""):
        """
        This function split a Bangla paragraph file into sentences
        """
        with open(file_path, "r") as fp:
            data = fp.read()
            bnltk = NLTKTokenizer()
            mylist = bnltk.sentence_tokenize(data)

        # Converting list to text file
        with open(modified_file_path, "w") as new_file:
            for listitem in mylist:
                new_file.write("%s\n" % listitem)

    def split_bangla_paragraph(paragraph=""):
        """
        This function split a English Paragraph into sentences
        """
        bnltk = NLTKTokenizer()
        sent_tokens = bnltk.sentence_tokenize(paragraph)
        return sent_tokens

    def split_bangla_sentence(sentence):
        """
        This function split a Bangla Sentence into words
        """
        bnltk = NLTKTokenizer()
        word_tokens = bnltk.word_tokenize(sentence)
        return word_tokens
