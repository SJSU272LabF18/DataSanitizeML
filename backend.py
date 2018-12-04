import threading
import time
import algorithm_and_backend as algo

# class scan_result:
#     def __init__(self, num_of_good_table, num_of_bad_table, num_of_good_row, num_of_bad_row, table_list, time='00:00:05'):
#         self.num_of_good_table = num_of_good_table
#         self.num_of_bad_table = num_of_bad_table
#         self.num_of_good_row = num_of_good_row
#         self.num_of_bad_row = num_of_bad_row
#         self.table_list = table_list
#         self.time = time
#
# class table_item:
#     def __init__(self, db_name, col_name, data_list):
#         self.db_name = db_name
#         self.col_name = col_name
#         self.data_list = data_list


result = algo.Scan_Result(0, 0, 0, 0, 0, [])
abort = False
finish = False


def strip(data_list):
    new_data_list = []
    for l in data_list:
        new_list = []
        for ele in l:
            new_list.append(str.strip(ele))
        new_data_list.append(new_list)
    return new_data_list;

def connectToDB(IP, port, database, username, pswd):
    return algo.connectToDB(IP, port, database, username, pswd);

def startScan(key_words):
    global abort
    abort = False
    global finish
    finish = False

    # x = 0
    # while abort is False and x < 2:
    #     time.sleep(1)
    #     x+=1
    #
    # tb1 = algo.Table_Item('table1', ['1col1', '1col2', '1col3', '1col4', '1col5'],
    #                  [['data11', 'd12', 'd13', 'd14', 'd15'], ['data21', 'd22', 'd23', 'd24', 'dd5'],
    #                   ['data31', 'd32', 'd33', '3d4', '3d5'], ['d41', 'd42', 'd43', 'd44', 'd45'],
    #                   ['data51', 'd52', 'd53', 'd54', 'd55']])
    # tb2 = algo.Table_Item('table2', ['2col1', '2col2', '2col3'],
    #                  [['2data11', '2data12', '2data13'], ['2data21', '2data22', '2data23']])
    # #
    # table_list = [tb1, tb2]
    # sr = algo.Scan_Result(1,2,3,4,5,table_list)
    sr = algo.startScan(key_words)

    if abort is False:
        global result
        result = sr
        for table in result.table_list:
            newList = strip( table.data_list)
            table.data_list = newList

        finish = True


def deleteDataRow(table_item):
    pass
    algo.delete_data(table_item)

class Scan(threading.Thread):
    def __init__(self, key_word):
        threading.Thread.__init__(self)
        self.key_word = key_word

    def run(self):
        startScan(self.key_word)




