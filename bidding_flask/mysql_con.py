from pymysql import connect
from pymysql.cursors import DictCursor
from settings import MYSQL_HOST,MYSQL_USER,MYSQL_PASS,MYSQL_DB,MYSQL_PORT
class Bidding(object):
    def __init__(self):
        self.conn = connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASS,
            db=MYSQL_DB,
            charset="utf8",
            port=MYSQL_PORT
        )
        self.cursor=self.conn.cursor(DictCursor)

    def __del__(self):
        self.cursor.close()
        self.conn.close()

    def get_all(self):
        sql = "SELECT noteid,title,district_name,date FROM General_info ORDER BY date DESC"
        self.cursor.execute(sql)
        data = []
        for temp in self.cursor.fetchall():
            data.append(temp)
        return data

    def get_appoint(self, city, content):
        if city == '':
            sql = "SELECT noteid,title,district_name,date FROM General_info WHERE " \
                  "title like '%{}%'  ORDER BY date DESC".format(content)
            self.cursor.execute(sql)
            data = []
            for temp in self.cursor.fetchall():
                data.append(temp)
            return data
        elif content == '':
            sql = "SELECT noteid,title,district_name,date FROM General_info WHERE district_name = '{}' " \
                  "ORDER BY date DESC".format(city)
            self.cursor.execute(sql)
            data = []
            for temp in self.cursor.fetchall():
                data.append(temp)
            return data
        else:
            sql = "SELECT noteid,title,district_name,date FROM General_info WHERE district_name = '{}' AND " \
                  "title like '%{}%'  ORDER BY date DESC".format(city, content)
            self.cursor.execute(sql)
            data = []
            for temp in self.cursor.fetchall():
                data.append(temp)
            return data

    def get_content(self, noteid):
        sql = "SELECT link , information FROM General_info , Specific_info WHERE General_info.noteid =" \
              " Specific_info.noteid AND General_info.noteid = '{}'".format(noteid)
        self.cursor.execute(sql)
        data = []
        for temp in self.cursor.fetchall():
            data.append(temp)
        return data
    def get_content2(self, dt, noteid):
        search = dt+'/'+noteid
        sql = "SELECT link , information FROM General_info , Specific_info WHERE General_info.noteid =" \
              " Specific_info.noteid AND General_info.noteid = '{}'".format(search)
        self.cursor.execute(sql)
        data = []
        for temp in self.cursor.fetchall():
            data.append(temp)
        return data

if __name__ == '__main__':
    bidding = Bidding()
    print(bidding.get_appoint('', '竞争性存放'))
    #print(bidding.get_content('cjzcjycrgg/15988'))
    #print(bidding.get_all())

