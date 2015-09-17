import sys

"""
This file take in the original gene.train that my have some low frequent words.
The purpose of this file is to find out the word whose frequency is less than 5
and replace them in the original gene.train with RARE then ran counts_freq.py again
"""
# Original gene.counts file, should be 'gene.counts'
gene_counts = sys.argv[1]

# Original gene.train file, should be 'gene.train'
gene_train = sys.argv[2]

# New output new_gene.train file should be 'new_gene.train'
new_gene_train = sys.argv[3]

# File where we what to store all the identified rare words
rare_words = sys.argv[4]

def check_argv():
    if len(sys.argv) != 5:
        print 'Hey man, you need to pass in four arguments!!!!!!!!'
        print 'please format your argument in the following way: \
        python update_train_data.py gene.counts gene.train new_gene.train rare_words.txt'
    else:
        pass

class Counts(object):

    words_count = {}
    rare_words = set()

    def __init__(self, input_file, original_train_file, new_train_file, rare_words_file):
        self.input_file = input_file
        self.original_train_file = original_train_file
        self.new_train_file = new_train_file
        self.rare_words_file = rare_words_file

    def calculate_freq(self):
        """ Counts the frequency for each word ana store them in the words_count
        in a key-value pair form
        """
        try:
            with open(self.input_file, 'r') as f:
                for line in f:
                    t = line.strip().split()
                    count = int(t[0])
                    key = tuple(t[2:])
                    if t[1] == 'WORDTAG':
                        self.words_count.setdefault(key[1], 0)
                        self.words_count[key[1]] += count
        except IOError:
            print 'IOError: Something wrong with file reading'

    def generate_train(self):
        """ Reads in the original file gene.train, replace the low frequency
        word(frequency < 5) with _RARE_ And generate the new train file called
        new_gene.train so that the original gene.train file is intact
        """
        try:
            with open(self.original_train_file, 'r') as f:
                with open(self.new_train_file, 'w') as w:
                    for line in f:
                        line = line.strip()
                        if line:
                            words = line.split()
                            word = words[0]
                            self.words_count.setdefault(word, 0)
                            if self.words_count[word] < 5:
                                self.rare_words.add(word)
                                words[0] = '_RARE_'
                                w.write(' '.join(words) + '\n')
                            else:
                                w.write(' '.join(words) + '\n')
                        else:
                            w.write('\n')
        except IOError:
            print 'IOError: Something wrong with file reading and writing'

    def populate_rare_words(self):
        try:
            with open(self.rare_words_file, 'w') as r:
                for word in self.rare_words:
                    r.write(word + '\n')
        except IOError:
            print 'IOError: Something happend, you better fix it!!!'

if __name__ == '__main__':
    # Checks the argument of the program
    check_argv()
    # Creates the helper object which is an instance of the Counts
    obj = Counts(gene_counts, gene_train, new_gene_train, rare_words)
    obj.calculate_freq()
    obj.generate_train()
    obj.populate_rare_words()
