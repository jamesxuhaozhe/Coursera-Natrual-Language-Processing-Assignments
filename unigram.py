from __future__ import division
import sys
from math import *

# Should be 'new_gene.counts'
new_gene_counts = sys.argv[1]

# Should be 'rare_words.txt'
rare_words_file = sys.argv[2]

# Should be 'gene.dev'
unlabled_dev_file = sys.argv[3]

# Should be 'gene_dev.p1.out'
labled_dev_file = sys.argv[4]

def check_argv():
    """Checks the script arguments passed in"""
    if len(sys.argv) != 5:
        print 'Asshole , you should at least pass in two arguments'
        print '''Command should be this:
        python unigram.py new_gene.counts rare_words.txt gene.dev gene_dev.p1.out'''
    else:
        pass

class Hmm(object):
    # word dicitonary that hold count(y -> x) counts key is TAG WORD
    # and the value is the count(y -> x)
    word = {}

    # Dictionary that key -> value, key is the WORD and the value is the
    # frequency of the word
    word_counts = {}

    # Ngram information
    ngrams = {1:{}, 2:{}, 3:{}}

    # Rare_words
    rare_words = set()

    # UnRare_words
    unrare_words = set()

    def __init__(self, train_file):
        self.train_file = train_file

    def process_train(self):
        """Process new_gene.counts file"""
        print 'Processing training file...'
        try:
            with open(self.train_file, 'r') as f:
                for line in f:
                    t = line.strip().split()
                    count = int(t[0])
                    key = tuple(t[2:])
                    tag = t[1]
                    if tag == '1-GRAM':
                        self.ngrams[1][key[0]] = count
                    elif tag == '2-GRAM':
                        self.ngrams[2][key] = count
                    elif tag == '3-GRAM':
                        self.ngrams[3][key] = count
                    elif tag == 'WORDTAG':
                        self.word[key] = count
                        if key[1] != '_RARE_':
                            self.unrare_words.add(key[1])
                        self.word_counts.setdefault(key[1], 0)
                        self.word_counts[key[1]] += count
        except IOError:
            print 'IOError: Something has happened and you are fucked!!!'
        print 'Finish processing training file!!!'

    def populate_rare_words(self, rare_words_file):
        """Process rare_words.txt and store the rare words in the self.rare_words"""
        print 'Populating rare words...'
        try:
            with open(rare_words_file, 'r') as f:
                for line in f:
                    if line:
                        self.rare_words.add(line)
        except IOError:
            print 'IOError: Somgthing is wrong!! you better fix it!'
        print 'Finish populating the rare words!!!'

    def get_tags(self):
        """Gets all the tags in the model"""
        return self.ngrams[1].keys()

    def get_emmision(self, word, tag):
        """Calculate the emission for word, tag pair"""
        if tag in ['*', 'STOP']:
            return 0.0
        new_word = self.replace_word(word)
        return self.word.get((tag, new_word), 0.0) / self.ngrams[1][tag]

    def replace_word(self, word):
        """Word replacement, if a word belongs to rare_words or unseen, should
        be replaced with _RARE_"""
        if word in self.rare_words:
            return '_RARE_'
        elif word not in self.unrare_words:
            return '_RARE_'
        else:
            return word

class UnigramDecoder(object):
    def __init__(self, hmm, test_data_file, output_file):
        self.hmm = hmm
        self.test_data_file = test_data_file
        self.output_file = output_file

    def write(self):
        print 'Writing the result to file....'
        try:
            with open(self.test_data_file, 'r') as f:
                with open(self.output_file, 'w') as w:
                    sentences = []
                    for line in f:
                        line = line.strip()
                        if line:
                            exp_tag = self.get_exp_tag(line)
                            w.write(' '.join([line, exp_tag]) + '\n')
                        else:
                            w.write('\n')
        except IOError:
            print 'IOError: Something is going wrong!!'
        print 'Finish writing the result!!!'

    def get_exp_tag(self, x):
        all_tags = self.hmm.get_tags()
        return self.argmax([(y, self.e(x, y)) for y in all_tags])

    def e(self, x, y):
        return self.hmm.get_emmision(x, y)

    def argmax(self, ls):
        return max(ls, key = lambda item : item[1])[0]


if __name__ == '__main__':
    check_argv()
    hmm = Hmm(new_gene_counts)
    hmm.process_train()
    hmm.populate_rare_words(rare_words_file)
    decoder = UnigramDecoder(hmm, unlabled_dev_file, labled_dev_file)
    decoder.write()

