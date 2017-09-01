#!/usr/bin/env python3

"""
crossword

Usage:
    Python3 crossword
"""
from words import Words
from engine import RenderEngine
import sys

def main(location):
    # read the words from a file
    word_object = Words()
    word_object.set_case("UPPER")
    word_object.read_words_file(location)
    # word_object.read_words_url("https://gist.githubusercontent.com/atduskgreg/3cf8ef48cb0d29cf151bedad81553a54/raw/82f142562cf50b0f6fb8010f890b2f934093553e/animals.txt")

    # render a grid with the words
    engine = RenderEngine(word_object)
    engine.generate_grid(16)

    engine.print_letter_matrix()
    print("-" * word_object.max_word_length)

    #print (len(engine.missed_words))
    #engine.print_words_not_in_grid()

    engine.print_words_in_grid()

location = r"c:\temp\words.txt"
if __name__ == "__main__":
    if (len(sys.argv) > 1):
        # Being invoked as an application (rather than an import)
        location = sys.argv[1] # use arg 1 as 0 is the filename

main(location)
