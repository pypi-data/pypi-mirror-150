from collections import Counter


class CountManager:
    """
    CountManager class
    """

    def __init__(self):
        self.counts = Counter()
        self.sentence = ""

    def set_sentence(self, sentence):
        """
        Set sentence
        :param sentence:
        :return:
        """
        self.sentence = sentence

    def get_sentence(self):
        """
        Get sentence
        :return:
        """
        return self.sentence

    def get_counts(self):
        """
        Get counts
        :return:
        """
        return self.counts

    def get_count(self, key):
        """
        Get count of a key
        :param key:
        :return:
        """
        return self.counts[key]

    def count_lines(file_path=""):
        """
        Count total no of lines in a text file
        """
        with open(file_path, "r") as fp:
            for count, line in enumerate(fp):
                pass
        return count + 1

    def count_words(sentence):
        """
        Count total words in a sentence
        """
        return len(sentence.split())

    def count_unique_words(sentence: str) -> int:
        """
        Count total unique words in a sentence
        """
        unique_count = 0
        for letter, count in Counter(sentence.split()).items():
            if count == 1:
                unique_count += 1
        return unique_count

    def count_chars(sentence):
        """
        Count total characters in a sentence
        """
        return len(sentence)
