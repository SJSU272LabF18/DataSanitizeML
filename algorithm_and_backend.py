import numpy as np
import collections
import pymysql
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import time

class Scan_Result:
    def __init__(self, time_consumed, num_of_good_table, num_of_bad_table, num_of_good_row, num_of_bad_row, table_list):
        self.time = time_consumed
        self.num_of_good_table = num_of_good_table
        self.num_of_bad_table = num_of_bad_table
        self.num_of_good_row = num_of_good_row
        self.num_of_bad_row = num_of_bad_row
        self.table_list = table_list

class Table_Item:
    def __init__(self, table_name, col_name, data_list):
        self.table_name = table_name
        self.col_name = col_name
        self.data_list = data_list

def data_nlp_process():
    path = 'E:\\Cod_Tools\\@CS_PROJECT\\PycharmProjects\\GDPR_DB_Sanitization\\data\\data_all.txt'
    fr = open(path, encoding='utf-8')
    data = []
    for line1 in fr:
        data.append(line1)

    temp_list = []
    for i in range(len(data)):
        line_all = str(data[i]).split('^^')
        detail = line_all[2]
        produce = word_tokenize(detail)
        temp_list.append(line_all[0] + '^^' + line_all[1] + '^^')
        for x in produce:
            temp_list.append(str(x))
        temp_list.append('\n')

    path = "E:\\Cod_Tools\\@CS_PROJECT\\PycharmProjects\\GDPR_DB_Sanitization\\data\\processed.txt"
    with open(path, 'w', encoding='utf-8') as fw:
        for i in temp_list:
            fw.write(str(i) + '/')
    fr.close()
    fw.close()

    total_raw = len(data)
    return total_raw

def data_cleaning():
    path = "E:\\Cod_Tools\\@CS_PROJECT\\PycharmProjects\\GDPR_DB_Sanitization\\data\\processed.txt"
    a = []
    with open(path, 'r', encoding='utf-8') as fr:
        for line in fr:
            if len(line) < 10:
                continue
            line_all = line.split('^^')
            detail = line_all[2]
            detail = detail.replace('/>', '>')
            produce = detail.replace(',', '').replace('.', '').replace('?', ''). \
                replace('//', ' ').replace('/', ' ')

            a.append(line_all[0].replace('/', '') + '^^' + line_all[1] + '^^' + produce)
    '''
    path1 = "/Users/liyuwen/Desktop/272/project/code/data_feed.txt"
    with open(path1, 'w', encoding='utf-8') as fw:
        for i in a:
            fw.write(str(i))
    fw.close()
    '''
    fr.close()
    return a

def trans_into_class(string, name_list, table_list):
    data_all = string.split('^^')
    t_name = data_all[0].strip()
    t_col = []
    t_detial = []
    for i in data_all[1].split(','):
        t_col.append(i)
    for j in data_all[2].split('>>'):
        t_detial.append(j)

    if t_name not in name_list:
        name_list.append(t_name)
        new_tb = Table_Item(t_name, t_col, [t_detial])
        table_list.append(new_tb)
    else:
        for tb in table_list:
            if tb.table_name == t_name:
                tb.data_list.append(t_detial)

def TF_IDF(key_words):
    vectorizer = CountVectorizer()  # Convert a collection of text documents to a matrix of token counts
    transformer = TfidfTransformer()  # conunt every word's tf-idf value


    #test word count matrix
    clean_data = data_cleaning()
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

    return result;

global_IP = 0
global_port = 0
global_database = 0
global_username = 0
global_pswd = 0

def connectToDB(IP, port, database, username, pswd):
    res = False
    try:
        db = pymysql.connect(IP, username, pswd, database)
        # cursor = db.cursor()
        # cursor.execute('INSERT INTO table1 VALUES(2,"name","detail")')
        # db.commit()
        res = db.open
        db.close()
    except:
        pass
    if res:
        global globalIP
        globalIP = IP
        global global_port
        global_port = port
        global global_database
        global_database = database
        global global_username
        global_username = username
        global global_pswd
        global_pswd = pswd

    return res;


def delete_data(table_item):
    table_name = table_item.table_name
    data_list = table_item.data_list
    id_list = []
    for i in range(len(data_list)):
        id_list.append(data_list[i][0])

    global globalIP
    global global_port
    global global_database
    global global_username
    global global_pswd

    db = pymysql.connect(global_IP, global_username, global_pswd, global_database)
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

def startScan(key_words):
    total_raw = data_nlp_process()

    name_list = []
    table_list = []
    raw_result = []
    start = time.time()

    raw_result = TF_IDF(key_words)

    end = time.time()
    for i in raw_result:
        trans_into_class(i, name_list, table_list)
    time_consumed = end - start

    for tb in table_list:
        print(tb.table_name)
        print(tb.col_name)
        print(tb.data_list)


    good_table = 2 - len(table_list)
    good_raw = total_raw - len(raw_result)

    scan_result = Scan_Result(time_consumed, good_table, len(table_list), good_raw,len(raw_result), table_list)
    print(scan_result.time)
    print('back end num of good table:',scan_result.num_of_good_table)
    print('back end num of bad table:',scan_result.num_of_bad_table )
    print('back end num of good row:',scan_result.num_of_good_row)
    print('back end num of bad row:',scan_result.num_of_bad_row)
    # print("one data list", scan_result.table_list[1].data_list[0])
    return scan_result
