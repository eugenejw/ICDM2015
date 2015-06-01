__author__      = "Weihan Jiang"
__copyright__   = "Copyright 2015, UWT"

from os.path import join, dirname, realpath
import itertools, enchant
import csv
from pyngram import calc_ngram
import logging
import time
import re
from wordsegment import segment


def timeit(f):
    def timed(*args, **kw):

        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        print 'func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts)
        with open('enchant_version_performance_result_for_func:%r.txt'%(f.__name__), 'a') as file:
            file.write('%2.4f \n'%(te-ts))
        return result
    return timed

def timeit2(f):
    def timed(*args, **kw):

        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        print 'func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts)
        with open('enchant_version_performance_result_for_func:%r.txt'%(f.__name__), 'a') as file:
            file.write('%2.4f \n'%(te-ts))
        return result
    return timed

def timeit3(f):
    def timed(*args, **kw):

        ts = time.time()
        result = f(*args, **kw)
        te = time.time()

        print 'func:%r args:[%r, %r] took: %2.4f sec' % \
          (f.__name__, args, kw, te-ts)
        with open('enchant_version_performance_result_for_func:%r.txt'%(f.__name__), 'a') as file:
            file.write('%2.4f \n'%(te-ts))
        return result
    return timed


def calculate_3gram_normality():

    dic_3gram = {}
    with open('count_3l.txt') as f:
        for line in f:
            pattern = re.search(r'(\w+).(.*)', line)
            gram = pattern.group(1)
            count = pattern.group(2)
            dic_3gram[gram] = count

    return dic_3gram

def calculate_2gram_normality():
    dic_2gram = {}
    with open('count_2l.txt') as f:
        for line in f:
            pattern = re.search(r'(\w+).(.*)', line)
            gram = pattern.group(1)
            count = pattern.group(2)
            dic_2gram[gram] = count
    return dic_2gram


@timeit2
def get_2_gram_result(input_domain):
    input_domain = input_domain
    if input_domain == '':
        return 0
#    print 'input domain is: %s'%input_domain
    
    dic = {}
    dic_good = {}

    tmp_sum = 0
    bi_gram_list = []
    bi_gram_list = calc_ngram(input_domain, 2)

    count = 0 #count how many time this n-gram appears in domain
    for each in bi_gram_list:
        count = count + each[1]

#    print 'bi_gram_list is: %s'%bi_gram_list
    for item in bi_gram_list:    # each[4] is bi-gram list
            if item[0] in dic_2gram:    #item[0] is bi-gram letters
                tmp_2gram_count = dic_2gram[item[0]] 
            else:
                tmp_2gram_count = 0
            tmp_sum = float(tmp_sum) + float(tmp_2gram_count)
#    print 'tmp_sum is now: %s'%tmp_sum
    if len(bi_gram_list) == 0:
            tmp_2gram_nor_score = 0
    else:
            tmp_2gram_nor_score = float(tmp_sum)/count
            print 'float(tmp_sum) is: %s'%float(tmp_sum)
            print 'count is: %s'%count
#    print 'tmp_2gram_nor_score_ratio is: %s'%(tmp_2gram_nor_score/1024908267229.0)
    return (tmp_2gram_nor_score/1024908267229.0)



@timeit3
def get_3_gram_result(input_domain):
    input_domain = input_domain
    if input_domain == '':
        return 0
#    print 'input domain is: %s'%input_domain
    
    dic = {}
    dic_good = {}

    tmp_sum = 0
    tri_gram_list = []
    tri_gram_list = calc_ngram(input_domain, 3)

    count = 0 #count how many time this n-gram appears in domain
    for each in tri_gram_list:
        count = count + each[1]

#    print 'tri_gram_list is: %s'%tri_gram_list
    for item in tri_gram_list:    # each[4] is bi-gram list
            if item[0] in dic_3gram:    #item[0] is bi-gram letters
                tmp_3gram_count = dic_3gram[item[0]] 
            else:
                tmp_3gram_count = 0
            tmp_sum = float(tmp_sum) + float(tmp_3gram_count)
#    print 'tmp_sum is now: %s'%tmp_sum
    if len(tri_gram_list) == 0:
            tmp_3gram_nor_score = 0
    else:
            tmp_3gram_nor_score = float(tmp_sum)/count
 #           print 'float(tmp_sum) is: %s'%float(tmp_sum)
 #           print 'count is: %s'%count
 #   print 'tmp_3gram_nor_score_ratio is: %s'%(tmp_3gram_nor_score/1024908267229.0)
    return (tmp_3gram_nor_score/1024908267229.0)


#*************Meaningful_scoring*****************#

dictionary = enchant.Dict("en_US")
#with open ("unigrams.txt", "r") as myfile:
#    dictionary=myfile.read().replace('\n', ' ')

#split the string in all possible places
def break_down(text):
    words = text.split()
    ns = range(1, len(words))
    for n in ns:
        for idxs in itertools.combinations(ns, n):
            yield [' '.join(words[i:j]) for i, j in zip((0,) + idxs, idxs + (None,))]

#compute the maximum meaningful characters ratio
@timeit
def meaningful_characters(domain):
    if domain == '' or domain == ' '  or len(domain) == 0:

        return (0,0,-100.0)
#    domain_length = float(len(domain))
#    domain = ''.join([i for i in domain if not i.isdigit()])
    char_count = 0
    ratio = 0.0
    pairwise_score = -100.0
#    bigram_counts = bigram_counts
#    breakdowns = break_down(" ".join(domain))
    breakdowns = []
    breakdowns = segment(domain)
#    tri_gram_results = calc_ngram(domain, 3)
#    four_gram_results = calc_ngram(domain, 4)
#    five_gram_results = calc_ngram(domain, 5)
#    six_gram_results = calc_ngram(domain, 6)
#    for item in tri_gram_results:
#        breakdowns.append(item[0])
#    for item in four_gram_results:
#        breakdowns.append(item[0])
#    for item in five_gram_results:
#        breakdowns.append(item[0])
#    for item in six_gram_results:
#        breakdowns.append(item[0])


    for word in breakdowns:
#        if word in dictionary:
#            char_count = char_count + 1
        if dictionary.check(word):
            char_count = char_count + 1
    ratio = float(char_count)/len(breakdowns)
    pairwise_score = meaningful_pairwise(breakdowns, ratio)

#    print '[info]:domain %s has been broken into %s words:%s. The meaningful score is %s. The pairwise meaningful score is %s\n' %(domain,str(len(breakdowns)),breakdowns, str(ratio), str(pairwise_score))

    return (ratio,len(breakdowns), float(pairwise_score))



def _ngrams(input, n):
  input = input.split(' ')
  output = []
  for i in range(len(input)-n+1):
    output.append(input[i:i+n])
  return output

#compute the emaningful pairwise score
def meaningful_pairwise(input_list,ratio):
    ratio = ratio
    pair_string = ' '.join(input_list) 
    pair_string1 = ''.join(input_list)
    pair_list = []
    pair_list = _ngrams(pair_string,2)
    count_meaningful_pair = 0
    count_pair = len(input_list) - 1
    result = 0.0

    if count_pair == 0:
        return result
    
    for each in pair_list:
        prev = each[0]
        word = each[1]
        bigram = '{0} {1}'.format(prev, word)
        if bigram in bigram_counts:
            count_meaningful_pair = count_meaningful_pair + 1

    if count_meaningful_pair == 0:
#        result = -(count_pair+1)**(count_pair+1)
        result = (len(pair_string1)*ratio)
        return result
    else:
#        result = (count_meaningful_pair/float(count_pair))**-2
        return 100.0






#domain_list = []
#file_out = open('','w')
def parse_file(filename):
    """Read `filename` and parse tab-separated file of (word, count) pairs."""
    with open(filename) as fptr:
        lines = (line.split('\t') for line in fptr)

        return dict((word, float(number)) for word, number in lines)

#unigram_counts = parse_file(join(dirname(realpath(__file__)), 'wordsegment_data', 'unigrams.txt'))
bigram_counts = parse_file(join(dirname(realpath(__file__)), 'wordsegment_data', 'bigrams.txt'))


#create ngram dic 
dic_2gram = {}
dic_3gram = {}
dic_2gram = calculate_2gram_normality()
dic_3gram = calculate_3gram_normality()


counter = 0
data = ''
with open('james_features.csv','rb') as csvfile:
    with open('./dummy_for_performance_test.csv', 'w') as csvoutput:
        writer = csv.writer(csvoutput, lineterminator='\n')
        reader = csv.reader(csvfile)

        all = []
        for row in reader:
            
            counter = counter +1
            col=row[4] #domain
            col1 = row[3] #subdomain
            print 'working on URL: %s'%row[2]

            print 'its 2nd_domain: %s'%col

            print 'its 3rd_domain: %s'%col1

            score = 0
            score1 = 0
            word_c = 0
            word_c1 = 0
            pairwise_core = -100.0
            bigram_nor_score = 0
            trigram_nor_score = 0

            if counter == 1:
                score = 'domain_meaningful_score'
                word_c = 'domain_word_brokendown_count'
                pairwise_score = 'pairwise_score'
                bigram_nor_score = '2nd_domain_2gram_nor_score'
                trigram_nor_score = '2nd_domain_3gram_nor_score'
            else:
                if len(col1) >= len(col):
                    col = col1
                meaningful_result = []
                meaningful_result = meaningful_characters(col)
                score = meaningful_result[0]

                word_c = meaningful_result[1]

                pairwise_score = meaningful_result[2]
                bigram_nor_score = get_2_gram_result(col)
                trigram_nor_score = get_3_gram_result(col)


            row.append(score)
            row.append(word_c)
            row.append(pairwise_score)
            row.append(bigram_nor_score)
            row.append(trigram_nor_score)
            all.append(row)
        writer.writerows(all)
