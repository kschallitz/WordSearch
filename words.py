"""
Reads words from a URL or file for use in creating a crossword puzzle
"""
from urllib.request import urlopen
import re

class Words:
    _max_word_length = 0
    _cases = {"lower":1, "UPPER":2, "Capital":3}

    case = "lower"
    wordlist = []  # list of words

    def set_case(self, case=None):
        """ Sets the case to use when displaying the word grid. Default is lowercase. """
        if case == None:
            self.case = self._cases["lower"]
            return

        if case not in self._cases:
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
            with open(file_name, "r") as f:
                # File format is assumed to be strings (one per line)
                # Use a set comprehension to eliminate duplicates
                word_set = {self.clean_word(word) for word in f}

            self.wordlist = list(word_set)

            # Put larger words first as the small ones are easier to fit
            self.wordlist.sort(key = len, reverse=True)

        except Exception as error:
            print("TODO: Clarify exceptions for file read failure: " + str(error))

        # debug: Show list of words we just read in
        #if (__debug__):
        #    for word in words:
        #        print(word)

        return self.wordlist

    def read_words_url(self, url):
        """
        Read words into a list from an URL, making the words lowercase
        NOTE: Calling this method does NOT remove existing words in the list. This is by design to allow
        for the ability to load words from both a URL and a file.

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
                    word = self.clean_word(word)

                    for subword in word.split():
                        if len(subword) > 2: # Exclude any two letter words
                            self.wordlist.append(subword)

        except Exception:
            # TODO
            print ("Error opening URL")

        # eliminate any duplicates
        word_set = set(self.wordlist)
        self.wordlist = list(word_set)

        # Put larger words first as the small ones are easier to fit
        self.wordlist.sort(key=len, reverse=True)

    def clean_word(self, word):
        word = word.rstrip('\n')

        if self.case == "lower":
            word = word.lower()
        elif self.case == "UPPER":
            word = word.upper()
        elif self.case == "Capital":
            word = word.capitalize()

        # Eliminate any non-alpha character
        thisword = re.sub('[^a-zA-Z]', '', word)

        return thisword

    def get_max_word_len(self, word_list=wordlist):
        """
        Gets the length of the largest word in the words list

        :param
            word_list: list of words

        :return:
            integer: Length of the largest word in the list
        """
        if word_list is None or word_list == []:
            if self.wordlist is not None and self.wordlist != []:
                word_list = self.wordlist
            else:
                raise ValueError("wordlist must contain a valid list.")

        return len(max(word_list, key=len))