import requests
import json
import traceback
import jsonpath
import mysql_con
from bs4 import BeautifulSoup
content_id_list = []


#获取中标数据
def get_res_in_zfcg_g():
    url = "https://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results"
    params ={"pageSize": 15,
             "pageNo": 1,
             "sourceAnnouncementType": "3004,4005,4006",
             "isGov": "true",
             "isExact": 1,
             "district": 330300,
             "url": "notice"
             }
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'}
    res = requests.get(url, params=params, headers=headers)
    d = json.loads(res.text)
    noteid = jsonpath.jsonpath(d, "$..id")   #公告ID
    projectName = jsonpath.jsonpath(d, "$..projectName")  #项目名称
    projectCode = jsonpath.jsonpath(d, "$..projectCode")  #项目编号
    districtName = jsonpath.jsonpath(d, "$..districtName")  #行政区
    link = jsonpath.jsonpath(d, "$..url") #网站
    data_list = list(zip(noteid, projectName, projectCode, districtName, link))
    global content_id_list
    content_id_list = []
    content_id_list = [x[0] for x in data_list]
    return data_list


def insert_res_in_zfcg_g():
    cursor = None
    conn = None
    try:
        list = get_res_in_zfcg_g()
        #print(f'{time.asctime()}开始插入省政府采购网政府采购数据')
        conn, cursor = mysql_con.get_conn()
        sql = "INSERT INTO sub_bid_infos(noteid,projectName,projectCode,districtName,link)" \
              "VALUES(%s,%s,%s,%s,%s)"
        sql_query = "SELECT noteid FROM sub_bid_infos WHERE noteid = %s"
        for i in list:
            if not cursor.execute(sql_query, i[0]):
                cursor.execute(sql, [(i[0]), (i[1]), (i[2]), (i[3]), (i[4])])
        conn.commit()
        #print(f"{time.asctime()}插入省政府采购网政府采购数据完毕")
    except:
        traceback.print_exc()
    finally:
        mysql_con.close_conn(conn, cursor)
    insert_res_in_zfcg_g_content()

def insert_res_in_zfcg_g_content(key):
    for i in content_id_list:
        key = i
        url = "https://zfcgmanager.czt.zj.gov.cn/cms/api/cors/remote/results"
        params = {"noticeId": key,
                  "url": "noticeDetail"
                  }
        headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                                 ' Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'}
        res = requests.get(url, params=params, headers=headers)
        d = json.loads(res.text)
        noticePubDate = jsonpath.jsonpath(d, "$..noticePubDate")[0] #发布时间
        noticeContent = jsonpath.jsonpath(d, "$..noticeContent")[0] #HTML网页内容
        relevantArticles = jsonpath.jsonpath(d, "$..relevantArticles")[0]
        a = 0
        for i in relevantArticles:
            a += 1
            if a == 4:
                contract = i['id']
        bs = BeautifulSoup(noticeContent, "html.parser")
        money_data = bs.find_all(name='td', attrs={"class": "code-summaryPrice"})
        for i in money_data:
            money = i.get_text()
        supplier_data = bs.find_all(name='td', attrs={"class": "code-winningSupplierName"})
        for i in supplier_data:
            supplier = i.get_text()
        supplierAddr_data = bs.find_all(name='td', attrs={"class": "code-winningSupplierAddr"})
        for i in supplierAddr_data:
            supplierAddr = i.get_text()
        purchaser_data = bs.find_all(name='span', attrs={"class": "bookmark-item uuid-1596004663203 code-00014 "
                                                                  "editDisable interval-text-box-cls readonly"})
        for i in purchaser_data :
            purchaser = i.get_text()
        cursor = None
        conn = None
        try:
            conn, cursor = mysql_con.get_conn()
            sql = "UPDATE sub_bid_infos SET purchaser = %s , supplier = %s , supplierAddr = %s ," \
                  " money = %s , noticePubDate = %s WHERE noteid = %s "
            cursor.execute(sql, [purchaser, supplier, supplierAddr, money, noticePubDate, key])
            conn.commit()
        except:
            traceback.print_exc()
        finally:
            mysql_con.close_conn(conn, cursor)
        if contract != None:
            print(111)

if __name__ == '__main__':
    #print(get_res_in_zfcg_g())
    insert_res_in_zfcg_g()
    #insert_res_in_zfcg_g_content(8185567)
    #insert_res_in_zfcg_g_content()
