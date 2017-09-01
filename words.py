"""
Reads words from a URL or file for use in creating a crossword puzzle
"""
from urllib.request import urlopen

class Words:
    wordlist = []  # list of words
    max_word_length = 0
    cases = {"lower":1, "UPPER":2, "Capital":3}
    case = "lower"

    def set_case(self, case=None):
        if case == None:
            self.case = self.cases["lower"]
            return

        if case not in self.cases:
            return
        else:
            self.case = case

        return

    def read_words_file(self, file_name):
        """
        Read words into a list from a file, converting to set case(default: lowercase)

        :param
            file_name: Name of file containing strings of words (one per line)

        :return:
            list: A list containing all words from the given file
        """

        try:
            f = open(file_name, "r")

            # File format is assumed to be strings (one per line)
            for line in f:
                line = line.rstrip('\n')
                if self.case == "lower":
                    line = line.lower()
                elif self.case == "UPPER":
                    line = line.upper()
                elif self.case == "Capital":
                    line = line.capitalize()

                self.wordlist.append(line)

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
        """
        Read words into a list from an URL, making the words lowercase

        :param
            url: url containing UTF-8 encoded words (one per line)

        :return:
            list: A list containing all words from the given url as lowercase strings
        :param url:
        :return:
        """
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

        # eliminate any duplicates
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