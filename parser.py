import sys
import glob
import cPickle
from pybloomfilter import BloomFilter

folderpath = sys.argv[1]

for book_filepath in glob.glob(folderpath+'/*.txt'):
    book = open(book_filepath).read()
    sentences  = book.split('.') 
    bf = BloomFilter(100000,0.01,'filter.bloom')
    for sentence in sentences:
        words = sentence.split()
        for word in words:
            bf.add(word.strip('"'))
    print 'the' in bf
    print 'wut' in bf
    print 'laughter' in bf
    BloomFilter.from_base64(book_filepath+'.bf',BloomFilter.to_base64(bf))


