fr = open('/Users/liyuwen/Desktop/272/review.txt', 'r')
fw = open('/Users/liyuwen/Desktop/272/rev_done.txt', 'w')
import pymysql

def update_database(review_id, user_id, star, date, text):
    db = pymysql.connect('localhost', user='root', password='2574256', db="cmpe272", charset="utf8")
    try:
        cursor = db.cursor()
        sql = 'INSERT INTO restaurant_review (review_id, user_id, star, date, text) VALUES ("%s", "%s", "%s", "%s", "%s")' \
              % (review_id, user_id, star, date, text)

        print(sql)
        cursor.execute(sql)
        db.commit()
    except:
        db.rollback()
        print('error')

if __name__ == '__main__':
    id = 1
    for line in fr:
        line = line.strip("\n")
        if line == '':
            continue

        list_all = line.split('\":')

        review_id = list_all[1].split(',\"')[0].strip('\"')
        usr_id = list_all[2].split(',\"')[0].strip('\"')
        star = list_all[4].split(',\"')[0].strip('\"')
        date = list_all[5].split(',\"')[0].strip('\"')
        text = list_all[6].split(',\"')[0].strip('\"')
        text = text.replace('\n', '')

        #update_database(review_id, usr_id, star, date, text)
        table = 'restaurant_review'
        col = 'id,review_id,user_id,star,date,text'

        w = table + '^^' + col + '^^' + str(id) + '>>' + review_id + '>>' + usr_id + '>>' + star + '>>' + date + '>>' + text + '\n'
        fw.write(w)

        id = id + 1

    fw.close()
    fr.close()