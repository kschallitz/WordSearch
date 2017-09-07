"""
    Generates a letter grid of the specified n x n size.
    Note: The grid will generate to be large enough to contain the maximum word length,
    even if the specified n is less than the maximum word length.

"""
import random

class RenderEngine():
    """
    Constructs an NxN matrix of letters and inserts words into the matrix.
    Contains helper functions to display the words that were inserted, words not inserted,
    display the grid, and display word orientations.
    """
    word_object = None
    grid_size = 0
    letters_lower = 'abcdefghijklmnopqrstuvwxyz'
    letters_UPPER = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    orientations = {1: "horizontal_forward", 2: "horizontal_backward",
                    3: "vertical_forward", 4: "vertical_backward",
                    5: "frontslash_forward", 6: "frontslash_backward",
                    7: "backslash_forward", 8: "backslash_backward"}
    word_orientation = {}
    letter_matrix = [[1 for x in range(1)] for y in range(1)]
    mutable_matrix = [[1 for x in range(1)] for y in range(1)]
    missed_words = []
    CONST_DIFFICULTY = 1 # multiples the grid size to make it harder to find words
    CONST_PLACEMENT_RETRY = 500 # Number of times to try to place a word that doesn't fit with current loc / orientation

    def __init__(self, word_object):
        """ constructor for render_engine - takes a word object """
        self.word_object = word_object

    def randomize_word_orientations(self):
        """
        Assigns random orientations to each word in the word list
        """

        #  randomize word orientation
        num_orientations = len(self.orientations)
        for word in self.word_object.wordlist:
            new_orientation = self.orientations[random.randint(1, num_orientations)] # use text as it's easier to read
            self.word_orientation.update({word: new_orientation})

    def print_words_in_grid(self):
        for word in [x for x in self.word_object.wordlist if x not in self.missed_words]:
            print (word)

    def print_words_not_in_grid(self):
        for word in self.missed_words:
            print (word)

    def print_word_orientations(self):
        """
        Debug: prints the words from the word list and their orientations
        """
        for word in self.word_orientation:
            print(word)

    def generate_grid(self, size=0):
        """
        Generates an n x n grid containing all the words in the word_object
        If specified size is too small to contain the largest word, the grid
        will automatically be resized to match the length of the largest word.

        :param size: (optional) size of grid as size x size matrix
        If size is not given, size of largest word will be used by default
        If size is too small to contain largest word, grid will be auto-resized

        :return:
        A matrix representing the crossword grid.
        """

        # If size is too small to contain largest word,
        # then, increase the grid size.
        max_word_len = self.word_object.get_max_word_len()

        if size < max_word_len:
            size = max_word_len

        size *= self.CONST_DIFFICULTY

        self.grid_size = size
        self.letter_matrix = [[0 for x in range(size)] for y in range(size)]
        self.mutable_matrix = [[0 for x in range(size)] for y in range(size)]

        # first create the grid with random letters
        for col in range (size):
            for row in range (size):
                # generate a random letter
                if (self.word_object.case == "lower") or (self.word_object.case == "Capital"):
                    self.letter_matrix[row][col] = random.choice(self.letters_lower)
                else:
                    self.letter_matrix[row][col] = random.choice(self.letters_UPPER)

                self.mutable_matrix[row][col] = True # Set each space in the grid to be mutable by default

        # Randomize word orientations
        self.randomize_word_orientations()

        # DEBUG
        # self.print_word_orientations()

        # Place words on matrix
        for word, orientation in self.word_orientation.items():
            self.place_word_in_grid(word, orientation)

    def print_letter_matrix(self, matrix=None):
        """ Display the n X n matrix of letters and words
         :param matrix: (optional) the matrix object to display. If none is given, the engine object's matrix will
         be used.

        """

        if matrix is None:
            matrix = self.letter_matrix

        size = len(matrix)

        # DEBUG
        # for i in range(size):
        #     print(str(i), end=' ')
        # print ('\r')

        for row in range(size):
            for col in range(size):
                print (matrix[row][col], end = ' ')

            # DEBUG
            # print (str(row), end = '')

            print ("\r")

    def place_word_in_grid(self, word, orientation):
        start_x = 0
        start_y = 0
        end_x = 0
        end_y = 0
        step_x = 1
        step_y = 1

        word_item = word
        word_length = len(word) - 1
        grid_length = self.grid_size - 1

        # DEBUG
        #if (orientation != 'backslash_backward'):
        #    return

        valid = False
        retry = 0

        # pick a random location in the grid
        while not(valid) and (retry < self.CONST_PLACEMENT_RETRY):
            # determine word orientation
            if (orientation == 'horizontal_forward') or (orientation == 'horizontal_backward'):
                if orientation == 'horizontal_backward':
                    word_item = word_item[::-1]

                start_x = random.randint(0, grid_length - word_length )
                end_x = start_x + word_length

                start_y = random.randint(0, grid_length)
                end_y = start_y + 1

                step_x = 1
                step_y = 0

            elif (orientation == 'vertical_forward') or (orientation == 'vertical_backward'):
                if orientation == 'vertical_backward':
                    word_item = word_item[::-1]

                start_x = random.randint(0, grid_length)
                end_x = start_x + 1

                start_y= random.randint(0, grid_length - word_length)
                end_y = start_y + word_length


                step_x = 0
                step_y = 1

            elif (orientation == 'frontslash_forward') or (orientation == 'frontslash_backward'):
                if orientation == 'frontslash_backward':
                    word_item = word_item[::-1]

                start_x = random.randint(0, grid_length - word_length)
                end_x = start_x + word_length

                end_y = random.randint(0, grid_length - word_length)
                start_y = end_y + word_length

                step_x = 1
                step_y = -1

            elif (orientation == 'backslash_forward') or (orientation == 'backslash_backward'):
                if orientation != 'backslash_backward':
                    word_item = word_item[::-1] # Because it's backslah, "forward" is actually reverse

                end_x = random.randint(0, grid_length - word_length)
                start_x = end_x + word_length

                end_y = random.randint(0, grid_length - word_length)
                start_y = end_y + word_length

                step_x = -1
                step_y = -1

            # Test word placement in the grid
            # NOTE: Thought about passing this info as a word_info tuple, but that seemed to be redundant as I'd still
            #       need to collect all the info and assemble it into the tuple. This way you see clearly what is passed
            valid = self.test_word_placement(word_item, start_x, end_x, start_y, end_y, step_x, step_y)
            if not(valid):
                # Try reversing the order of the word to see if it will fit that way
                word_item = word_item[::-1]
                valid = self.test_word_placement(word_item, start_x, end_x, start_y, end_y, step_x, step_y)

                if not valid:
                    orientation = self.orientations[random.randint(1, len(self.orientations))] # Try a new random orientation
                    retry += 1

        # place word in grid
        if valid:
            self.insert_word_on_grid(word_item, start_x, end_x, start_y, end_y, step_x, step_y)

            # DEBUG
            # print(word_item + " : " + orientation + " start_x: " + str(start_x) + " end_x: " + str(
            #    end_x) + " start_y: " + str(start_y) + " end_y: " + str(end_y))

            # show user the word to find in the matrix
            # print ('%*s: %s' % (self.word_object.get_max_word_len(), word,orientation))

        else:
           self.missed_words.append(word)

    def test_word_placement(self, word_item, start_x, end_x, start_y, end_y, step_x, step_y):
        """
            Determines if a given word can be placed in the grid at the specified location
        :param self:
        :param start_x:
        :param end_x:
        :param start_y:
        :param end_y:
        :param word_item:
        :return:
        """
        # Test placement
        letter_index = 0
        col = start_x
        row = start_y

        #DEBUG
        if False:
            word_item = 'mouse'
            start_x = 5
            end_x = 6

            start_y = 7
            end_y = 8

            col = start_x
            row = start_y

            step_x = 1
            step_y = 1

        while (col != end_x) and (row != end_y):
            if not (self.mutable_matrix[row][col]):
                # Determine if it is the same letter we are trying to place
                if self.letter_matrix[row][col].lower() == word_item[letter_index].lower():
                    # We're still okay - continue to try to place word
                    letter_index += 1
                    row += step_y
                    col += step_x
                    continue
                else:
                    return False

            row += step_y
            col += step_x
            letter_index += 1

        if not (self.mutable_matrix[row][col]):
            # Determine if it is the same letter we are trying to place
            if not(self.letter_matrix[row][col] == word_item[letter_index]):
                return False

        return True

    def insert_word_on_grid(self, word_item, start_x, end_x, start_y, end_y, step_x, step_y):
        letter_index = 0
        col = start_x
        row = start_y

        while (col != end_x) and (row != end_y):
            self.letter_matrix[row][col] = word_item[letter_index]
            self.mutable_matrix[row][col] = False
            letter_index += 1
            col += step_x
            row += step_y

        self.letter_matrix[row][col] = word_item[letter_index]
        self.mutable_matrix[row][col] = False