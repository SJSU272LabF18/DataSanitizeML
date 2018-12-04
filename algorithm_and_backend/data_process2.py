fr = open('/Users/liyuwen/Desktop/272/rev.txt', 'r')
fw = open('/Users/liyuwen/Desktop/272/rev_done.txt', 'w')

if __name__ == '__main__':
    for line in fr:
        line = line.strip("\n")
        if line == '':
            continue

        list_all = line.split('\t')

        id = list_all[0]
        review_id = list_all[1]
        user_id = list_all[2]
        star = list_all[3]
        date = list_all[4]
        text =list_all[5]

        table = 'restaurant_review'
        col = 'id,review_id,user_id.star,date,text'

        w = table + '^^' + col + '^^' + id + '>>' + review_id + '>>' + user_id + '>>' + star + '>>' + date + '>>' + text + '\n'

        fw.write(w)

    fr.close()
    fw.close()