import numpy as np
import collections
import pymysql
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import time

class scan_result:
    def __init__(self, time_consumed, num_of_good_table, num_of_bad_table, num_of_good_row, num_of_bad_row, table_list):
        self.time = time_consumed
        self.num_of_good_table = num_of_good_table
        self.num_of_bad_table = num_of_bad_table
        self.num_of_good_row = num_of_good_row
        self.num_of_bad_row = num_of_bad_row
        self.table_list = table_list

class table_item:
    def __init__(self, table_name, col_name, data_list):
        self.table_name = table_name
        self.col_name = col_name
        self.data_list = data_list

def data_nlp_process(file_path):
    path = file_path
    fr = open(path, encoding='utf-8')
    data = []
    trans_list =[]
    data_processed = []
    for line1 in fr:
        data.append(line1)

    temp_list = []
    for i in range(len(data)):
        line_all = str(data[i]).split('^^')
        detail = line_all[2]
        produce = word_tokenize(detail)
        re = line_all[0] + '^^' + line_all[1] + '^^'
        for x in produce:
            re = re + x + '/'
        temp_list.append(re + '\n')

    for i in temp_list:
        if len(i) < 10:
            continue
        line_all = i.split('^^')
        detail = line_all[2]
        detail = detail.replace('/>', '>')
        produce = detail.replace(',', '').replace('.', '').replace('?', ''). \
            replace('//', ' ').replace('/', ' ')

        data_processed.append(line_all[0].replace('/', '') + '^^' + line_all[1] + '^^' + produce)

    total_raw = len(data)
    fr.close()
    return total_raw, data_processed


def trans_into_class(string, name_list, table_list):
    data_all = string.split('^^')
    t_name = data_all[0].strip()
    t_col = []
    t_detial = []
    for i in data_all[1].split(','):
        t_col.append(i)
    for j in data_all[2].split('>>'):
        j = j.strip()
        t_detial.append(j)

    if t_name not in name_list:
        name_list.append(t_name)
        new_tb = table_item(t_name, t_col, [t_detial])
        table_list.append(new_tb)
    else:
        for tb in table_list:
            if tb.table_name == t_name:
                tb.data_list.append(t_detial)

def TF_IDF(key_words, data_list):
    vectorizer = CountVectorizer()  # Convert a collection of text documents to a matrix of token counts
    transformer = TfidfTransformer()  # conunt every word's tf-idf value


    #test word count matrix
    clean_data = data_list
    feed_data = []
    for i in range(len(clean_data)):
        feed_data.append(str(clean_data[i]).split('^^')[2])

    test_count = vectorizer.fit_transform(feed_data)
    #print(test_count.toarray())  # count matrix
    #print(vectorizer.get_feature_names())  # put into vectorizer
    #test end

    #test tf-idf matrix
    test_tfidf = transformer.fit_transform(test_count)
    #print(test_tfidf.toarray())  # get count matrix's IF-IDF value
    #print(test_tfidf.toarray().shape)
    #test end

    #process the key words, get the matrix of its word count
    keywords_nlp = word_tokenize(key_words)
    coll = collections.Counter(keywords_nlp)
    new_vectorizer = []

    for word in vectorizer.get_feature_names():  # originial word count
        new_vectorizer.append(coll[word])
    #print(new_vectorizer)

    '''original TF-IDF matrix process'''
    new_tfidf = np.array(test_tfidf.toarray()).T
    # print(new_tfidf)
    # print(new_tfidf.shape)

    '''matrix * matrix'''
    new_vectorizer = np.array(new_vectorizer).reshape(1, len(new_vectorizer))
    # print(new_vectorizer)
    scores = np.dot(new_vectorizer, new_tfidf)

    # print(type(scores))
    new_scores = list(scores[0])  # matrix to list

    max_location = sorted(enumerate(new_scores), key=lambda x: x[1])  # sort and reverse
    max_location.reverse()
    final_location = []
    for i in range(len(max_location)):  # find the max location
        #print(max_location[i][0]) id
        #print(max_location[i][1]) score
        if max_location[i][1] > 0:
            final_location.append(max_location[i][0])
    print("resluts are:")
    result = []
    for i in range(len(final_location)):
        result.append(clean_data[final_location[i]])
        print(clean_data[final_location[i]])

    return result



def delete_data(table_item):
    table_name = table_item.table_name
    data_list = table_item.data_list
    id_list = []
    for i in range(len(data_list)):
        id_list.append(data_list[i][0])

    db = pymysql.connect("localhost", "root", "2574256", "test")
    cursor = db.cursor()
    for id in id_list:

        sql = 'DELETE FROM ' + table_name + ' WHERE id = ' + id
        print(sql)

        try:
            cursor.execute(sql)
            db.commit()
            print('done')
        except:
            print('error')
            db.rollback()

    db.close()

if __name__ == '__main__':
    name_list = []
    table_list = []
    raw_result = []
    path = '/Users/liyuwen/Desktop/272/Project-Team-29/data/data_all.txt'

    print('please input key words:')
    key_words = input()
    start = time.time()

    data_list = data_nlp_process(path)[1]
    raw_result = TF_IDF(key_words, data_list)

    end = time.time()
    for i in raw_result:
        trans_into_class(i, name_list, table_list)
    time_consumed = end - start

    for tb in table_list:
        print(tb.table_name)
        print(tb.col_name)
        print(tb.data_list)

    all_table = 2
    good_table = all_table - len(table_list)
    total_raw = data_nlp_process(path)[0]
    good_raw = total_raw - len(raw_result)

    scan_result = scan_result(time_consumed, good_table, len(table_list), good_raw,len(raw_result), table_list)
    print(scan_result.time)
    print(scan_result.num_of_good_table)
    print(scan_result.num_of_bad_table )
    print(scan_result.num_of_good_row)
    print(scan_result.num_of_bad_row)
