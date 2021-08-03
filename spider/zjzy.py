import requests
import json
import time
import pymysql
import traceback
import jsonpath

content_id_list = []

def get_conn():
    conn = pymysql.connect( #连接数据库
        host="1.117.231.72",
        user="beerer",
        password="QWEqwe123",
        db="bidding",
        charset="utf8",
        port=3306,
    )
    # 创建游标：
    cursor = conn.cursor()
    return conn, cursor

def close_conn(conn, cursor): #关闭数据库连接
    if cursor:
        cursor.close()
    if conn:
        conn.close()

def get_keyword(i):
    if i == 0:
        keyword = '竞争性存放'
    else:
        keyword = '账户'
    return keyword

#省政府采购网政府采购数据
def get_res_in_zfcg_g(keyword):
    url = "https://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results"
    params ={"pageSize": 15,
             "pageNo": 1,
             "sourceAnnouncementType": "10016%2C3012%2C1002%2C1003%2C3014%2C3013%2C3009%2C4004%2C3008%2C2001%2C3001%2C3"
                                       "020%2C3003%2C3002%2C3011%2C3017%2C3018%2C3005%2C3006%2C3004%2C4005%2C4006%2C300"
                                       "7%2C3015%2C3010%2C3016%2C6003%2C4002%2C4001%2C4003%2C8006%2C1995%2C1996%2C1997%"
                                       "2C8008%2C8009%2C8013%2C8014%2C9002%2C9003%2C808030100%2C7003%2C7004%2C7005%2C70"
                                       "06%2C7007%2C7008%2C7009",
             "isGov": "true",
             "keyword": keyword,
             "isExact": 1,
             "district": 330300,
             "url": "notice"
             }
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'}
    res = requests.get(url, params=params, headers=headers)
    d = json.loads(res.text)  # 是将json格式数据转换为字典
    noteid = jsonpath.jsonpath(d, "$..id")  # JsonPath是一种简单的方法来提取给定JSON文档的部分内容
    title = jsonpath.jsonpath(d, "$..title")
    ch = 0 #去掉[]
    for i in title:
        cut = i.find('[')
        if cut != -1:
            title[ch] = i[:cut:]
        ch += 1
    districtName = jsonpath.jsonpath(d, "$..districtName")
    link = jsonpath.jsonpath(d, "$..url")
    data_list = list(zip(noteid, title, districtName, link))  # 将对象中对应的元素打包成一个个元组
    dnum = 0
    count = 0
    cha = [0] * 15
    for i in data_list:
        num = 0
        str = {"招标", "邀标", "询价", "竞谈", "单一", "竞价", "变更", "更正"}
        for j in str:
            num = num + i[1].find(j)
        cha[count] = num
        count += 1
    for i in cha:
        if i == -8:
            del data_list[dnum]
            dnum -= 1
        dnum += 1
    global content_id_list
    content_id_list = []
    content_id_list = [x[0] for x in data_list]
    return data_list

def insert_res_in_zfcg_g():
    for x in range(2):
        keyword = get_keyword(x)
        cursor = None
        conn = None
        try:
            list = get_res_in_zfcg_g(keyword)
            print(f'{time.asctime()}开始插入省政府采购网政府采购数据')
            conn, cursor = get_conn()
            sql = "INSERT INTO General_info(noteid, title, district_name, link, category) VALUES(%s, %s, %s, %s, %s)"
            sql_query = "SELECT id FROM General_info WHERE noteid = %s"
            for i in list:
                if not cursor.execute(sql_query, i[0]):
                    cursor.execute(sql, [(i[0]), (i[1]), (i[2]), (i[3]), 1])
            conn.commit()
            print(f"{time.asctime()}插入省政府采购网政府采购数据完毕")
        except:
            traceback.print_exc()
        finally:
            close_conn(conn, cursor)
        insert_res_in_zfcg_g_content()

def insert_res_in_zfcg_g_content():
    for i in content_id_list:
        key = i
        url = "https://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results"
        params = {"noticeId": key,
                  "url": "noticeDetail"
                  }
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'}
        res = requests.get(url, params=params, headers=headers)
        d = json.loads(res.text)  # 是将json格式数据转换为字典
        noticePubDate = jsonpath.jsonpath(d, "$..noticePubDate")[0]
        noticeTitle = "<h1>"+jsonpath.jsonpath(d, "$..noticeTitle")[0]+"</h1>"
        noticeContent = noticeTitle+jsonpath.jsonpath(d, "$..noticeContent")[0]
        cursor = None
        conn = None
        try:
            conn, cursor = get_conn()
            sql = "UPDATE General_info SET date = %s WHERE noteid = %s"
            cursor.execute(sql, [noticePubDate, key])
            conn.commit()
            sql_2= "INSERT INTO Specific_info(noteid,information) VALUES(%s,%s)"
            sql_query = "SELECT id FROM Specific_info WHERE noteid = %s"
            if not cursor.execute(sql_query, key):
                cursor.execute(sql_2, [key, noticeContent])
            conn.commit()
        except:
            traceback.print_exc()
        finally:
            close_conn(conn, cursor)


#省政府采购网非政府采购数据
def get_res_in_zfcg_n(keyword):
    url = "https://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results"
    params ={"pageSize": 15,
             "pageNo": 1,
             "sourceAnnouncementType": "10001,10002,10012,10003,10014,10004,10013,10006,10007,10008,10009,10010,10011",
             "includeGovDistrict": 1,
             "keyword": keyword,
             "isExact": 1,
             "district": 330300,
             "url": "notice"
             }
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'}
    res = requests.get(url, params=params, headers=headers)
    d = json.loads(res.text)  # 是将json格式数据转换为字典
    noteid = jsonpath.jsonpath(d, "$..id")  # JsonPath是一种简单的方法来提取给定JSON文档的部分内容
    title = jsonpath.jsonpath(d, "$..title")
    ch = 0
    for i in title:
        cut = i.find('[')
        if cut != -1:
            title[ch] = i[:cut:]
        ch += 1
    districtName = jsonpath.jsonpath(d, "$..districtName")
    link = jsonpath.jsonpath(d, "$..url")
    data_list = list(zip(noteid, title, districtName, link))  # 将对象中对应的元素打包成一个个元组
    dnum = 0
    count = 0
    cha = [0] * 15
    for i in data_list:
        num = 0
        str = {"招标", "邀标", "询价", "竞谈", "单一", "竞价", "变更", "更正"}
        for j in str:
            num = num + i[1].find(j)
        cha[count] = num
        count += 1
    for i in cha:
        if i == -8:
            del data_list[dnum]
            dnum -= 1
        dnum += 1
    global content_id_list
    content_id_list = []
    content_id_list = [x[0] for x in data_list]
    return data_list

def insert_res_in_zfcg_n():
    for x in range(2):
        keyword = get_keyword(x)
        cursor = None
        conn = None
        try:
            list = get_res_in_zfcg_n(keyword)
            print(f'{time.asctime()}开始插入省政府采购网非政府采购数据')
            conn, cursor = get_conn()
            sql = "INSERT INTO General_info(noteid, title, district_name, link, category) VALUES(%s, %s, %s, %s, %s)"
            sql_query = "SELECT id FROM General_info WHERE noteid = %s"
            for i in list:
                if not cursor.execute(sql_query, i[0]):
                    cursor.execute(sql, [(i[0]), (i[1]), (i[2]), (i[3]), 1])
            conn.commit()
            print(f"{time.asctime()}插入省政府采购网非政府采购数据完毕")
        except:
            traceback.print_exc()
        finally:
            close_conn(conn, cursor)
        insert_res_in_zfcg_n_content()

def insert_res_in_zfcg_n_content():
    for i in content_id_list:
        key = i
        url = "https://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results"
        params = {"noticeId": key,
                  "url": "noticeDetail"
                  }
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'}
        res = requests.get(url, params=params, headers=headers)
        d = json.loads(res.text)  # 是将json格式数据转换为字典
        noticePubDate = jsonpath.jsonpath(d, "$..noticePubDate")[0]
        noticeTitle = "<h1>"+jsonpath.jsonpath(d, "$..noticeTitle")[0]+"</h1>"
        noticeContent = noticeTitle+jsonpath.jsonpath(d, "$..noticeContent")[0]
        cursor = None
        conn = None
        try:
            conn, cursor = get_conn()
            sql = "UPDATE General_info SET date = %s WHERE noteid = %s"
            cursor.execute(sql, [noticePubDate, key])
            conn.commit()
            sql_2= "INSERT INTO Specific_info(noteid,information) VALUES(%s,%s)"
            sql_query = "SELECT id FROM Specific_info WHERE noteid = %s"
            if not cursor.execute(sql_query, key):
                cursor.execute(sql_2, [key, noticeContent])
            conn.commit()
        except:
            traceback.print_exc()
        finally:
            close_conn(conn, cursor)

if __name__ == '__main__':
    #print(get_res_in_zfcg_g("竞争性存放"))
    insert_res_in_zfcg_g()
    insert_res_in_zfcg_n()