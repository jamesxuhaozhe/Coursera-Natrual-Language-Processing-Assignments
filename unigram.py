import sys

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

    def __init__(self, train_file):
        self.train_file = train_file

    def process_train(self):
        try:
            with open(self.train_file, 'r') as f:
                for line in f:
                    t = line.strip().split()
                    count = int(t[0])
                    key = tuple(t[2:])
                    tag = t[1]
                    if tag == '1-GRAM':
                        self.ngrams[1][key[0]] = count
                        print key[0], count
                    elif tag == '2-GRAM':
                        self.ngrams[2][key] = count
                        print ' '.join(key), count
                    elif tag == '3-GRAM':
                        self.ngrams[3][key] = count
                        print ' '.join(key), count
                    elif tag == 'WORDTAG':
                        self.word[key] = count
                        self.word_counts.setdefault(key[1], 0)
                        self.word_counts[key[1]] += count
                        print ' '.join(key), count

        except IOError:
            print 'IOError: Something has happened and you are fucked!!!!!!'

if __name__ == '__main__':
    check_argv()
    obj = Hmm(sys.argv[1])
    obj.process_train()
