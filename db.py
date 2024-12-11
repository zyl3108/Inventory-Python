import pymysql.cursors
def getConnection():
    try:
        conn = pymysql.connect(host="127.0.0.1",user="root",password="123@dat",db="ims",cursorclass=pymysql.cursors.DictCursor)
        print("Connection")
        return conn
    except:
        print("Can't")
getConnection()
