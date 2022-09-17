import csv
import pymysql
import pymysql.cursors


def handle_uploaded_file(f):
    with open('app/static/upload/'+f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

def insertDB(file):
    db = pymysql.connect(host='localhost',
                             user='root',
                             password='123456')
    cursor = db.cursor()
    path = "app/static/upload/" + file
    csv_data = csv.reader(open(path, 'r', encoding='utf-8'), delimiter=";")
    for row in csv_data:
        cursor.execute('INSERT INTO TCC.cliente(nomec,cpf,mit_bal,sex,education,marriage,age,pay_1,pay_2,pay_3,pay_4,pay_5,pay_6,bill_amt_1,bill_amt_2,bill_amt_3,bill_amt_4,bill_amt_5,bill_amt_6,pay_amt_1,pay_amt_2,pay_amt_3,pay_amt_4,pay_amt_5,pay_amt_6,payment) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);',row)
    db.commit()
    cursor.close()
