"""
Reads words from a URL or file for use in creating a crossword puzzle
"""
from urllib.request import urlopen

class Words:
    wordlist = []  # list of words
    max_word_length = 0

    def read_words_file(self, file_name):
        """
        Read words into a list from a file

        :param
            file_name: Name of file containing strings of words (one per line)

        :return:
            list: A list containing all words from the given file
        """

        try:
            f = open(file_name, "r")

            # File format is assumed to be strings (one per line)
            for line in f:
                self.wordlist.append(line.rstrip('\n'))

            f.close()
            word_set = set(self.wordlist)
            self.wordlist = list(word_set)

        except Exception:
            print("TODO: Clarify exceptions for file read failure")

        # debug: Show list of words we just read in
        #if (__debug__):
        #    for word in words:
        #        print(word)

        return self.wordlist

    def read_words_url(self, url):
        try:
            with urlopen(url) as words:
                for word in words:
                    word = word.decode('UTF-8')
                    word = word.lower()
                    word = word.rstrip('\n')
                    for subword in word.split():
                        if len(subword) > 2:
                            self.wordlist.append(subword)

        except Exception:
            # TODO
            print ("Error opening URL")

        # eliminate any dulicates
        word_set = set(self.wordlist)
        self.wordlist = list(word_set)

    def get_max_word_len(self, word_list=wordlist):
        """
        Gets the length of the largest word in the words list

        :param
            word_list: list of words

        :return:
            integer: Length of the largest word in the list
        """

        self.max_word_length = 0

        for word in word_list:
            if len(word) > self.max_word_length:
                self.max_word_length = len(word)

        return self.max_word_length