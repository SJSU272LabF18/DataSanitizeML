import threading
import time


class my(threading.Thread):
    def __init__(self, kk):
        threading.Thread.__init__(self)

    def run(self):
        print(time.time()%60)


def strip(list):
    new_list = []
    for l in list:
        new_list.append( str.strip(l))
    return new_list;


l =[' 1','2',' 4', '123']
print( strip(l) )
