import sys
import cPickle
import re
from random import randint
import glob
from pybloomfilter import BloomFilter

book_dir    = sys.argv[1]
bloom_dir   = sys.argv[1]

#Grab all book filepaths
candidatebook_paths =   glob.glob(book_dir+'/*.txt')
bloom_paths =   glob.glob(book_dir+'/*.bf')

print candidatebook_paths
print bloom_paths
def mutate(first_sentence,bloom_paths,bias=3):
    #Mutates first_sentence at a random word by splicing with another sentence container that same randomly selected word-- the word will not be selected from the first (1/bias) of the sentence.
    first_sentence_words =   first_sentence.split()
    #print first_sentence_words
    #Pick a random word in the target sentence as the splice point
    word_index  =   randint(randint(0,(len(first_sentence_words)-1)),(len(first_sentence_words)-1))
 
    target_word =   first_sentence_words[word_index].strip('"')
    return mutateAtWord(first_sentence,target_word,bloom_paths)
def makeQuote(splices = 1):
    #Pick a random book to grab the first sentence piece from
    firstbook_index = randint(0,len(candidatebook_paths)-1)
    firstbook = open(candidatebook_paths[firstbook_index]).read()
    #Split the book into sentences
    sentences = re.split('\.+|\?+|\!+',firstbook)
    #Pick a random sentence in the book to start with
    sentence_index  =   randint(0,(len(sentences)-1))
    sentence =   sentences[sentence_index]
    lastsentence = sentence
    for i in range(splices):
        mutate_count = 0
        while sentence == lastsentence and mutate_count < 10:
            sentence = mutate(sentence,bloom_paths)
            mutate_count+=1
        lastsentence = sentence
        print str(i)+':'+sentence
    return sentence
def mutateAtWord(first_sentence,word,bloom_paths):    
   #Mutate first_sentence at point word by splicing with another sentence containing word pulled from a file in bloom_paths.
    #print first_sentence
    #print word
    tried_indices = []
    second_sentence = ''
    while second_sentence == '' and len(tried_indices) < len(bloom_paths):
        #Pick a random bloom filter to check for our word
        bloom_index =   randint(0,(len(bloom_paths)-1))
        if not bloom_index in tried_indices:
            #print bloom_paths[bloom_index]
            bf = BloomFilter.open(bloom_paths[bloom_index])
            tried_indices.append(bloom_index)
        else:
            continue
        #Check if the bloom filter we picked has seen the word we're looking for
        if word in bf:
            #print 'got a match!'
            #If it has, open the book and pick a sentence to splice with
            target_book             =   open(bloom_paths[bloom_index][:-3]).read()
            target_book_sentences   =   re.split('\.+|\?+|\!+',target_book)            
            #Pick a random index to start scanning at
            target_book_sentence_index  =   randint(0,(len(target_book_sentences)-1))
            
            #Scan until we find the word we wanted
            while target_book_sentence_index < len(target_book_sentences):
                #print target_book_sentence_index
                if word in target_book_sentences[target_book_sentence_index].split() and target_book_sentences[target_book_sentence_index] !=first_sentence:
                    second_sentence = target_book_sentences[target_book_sentence_index]
                    break
                target_book_sentence_index+=1
    #print '______'
    if second_sentence == '':
        #We should probably just try a new word if we couldnt find a match
        print 'couldn\'t generate'
        return first_sentence
    else:
        new_sentence = ''
        #print 'First:'+first_sentence
        #print 'Second:'+second_sentence
        #print 'First,cut:'+first_sentence[:first_sentence.find(' '+word+' ')+1]
        #print 'Second,cut:'+second_sentence[second_sentence.find(word):]

        new_sentence +=first_sentence[:first_sentence.find(' '+word+' ')+1]
        new_sentence +=second_sentence[second_sentence.find(' '+word+' '):]
        if '"' in new_sentence.strip() and new_sentence.strip().count('"') %2 != 0:
            new_sentence+='"'
        #print new_sentence
        #print '______'
        return new_sentence
for i in range(100):
    print '{'
    makeQuote(3)
    print '}'




