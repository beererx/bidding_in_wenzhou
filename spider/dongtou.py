import requests
import json
import time
import pymysql
import traceback
import jsonpath
import mysql_con
from bs4 import BeautifulSoup

def get_res_in_dongtouzy():
    print(f'{time.asctime()}开始插入洞头区公共资源交易网采购数据')
    url = "http://ztb.dongtou.gov.cn/dtcms/search.jspx"
    params = {"q": "闲置资金"
              }
    headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
                             ' Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3861.400 QQBrowser/10.7.4313.400'}
    res = requests.get(url, params=params, headers=headers)
    html = res.text
    bs = BeautifulSoup(html, "html.parser")
    t_list = bs.find_all(name='div', attrs={"class": "Selcet-Back FloatL"})
    for i in t_list:
        judge = i.select('a')[0]
        condition = judge.text
        item = i.select('a')[1]
        if condition.find("成交") == -1:
            detail_url = "http://ztb.dongtou.gov.cn"+item.get('href')
            noteid = detail_url[32::]
            cut = noteid.find(".")
            noteid = noteid[:cut:]
            detail_title = item.get('title')
            item2 = i.select('h6')[0]
            date = item2.text
            cut2 = date.find('发布时间：')
            date = date[cut2+6::]
            num = 0
            num += detail_title.find("中标")
            if num == -1:
                cursor = None
                conn = None
                try:
                    conn, cursor = mysql_con.get_conn()
                    sql = "INSERT INTO General_info(noteid, title, district_name, link, category, date) VALUES(%s, %s, %s, %s, %s, %s)"
                    sql_query = "SELECT id FROM General_info WHERE noteid = %s"
                    if not cursor.execute(sql_query, noteid):
                        cursor.execute(sql, [noteid, detail_title, "洞头区", detail_url, 2, date])
                    conn.commit()
                except:
                    traceback.print_exc()
                finally:
                    mysql_con.close_conn(conn, cursor)
            url2 = "http://ztb.dongtou.gov.cn/dtcms/"+noteid+".htm"
            res2 = requests.get(url2, headers=headers)
            html2 = res2.text
            bs2 = BeautifulSoup(html2, "html.parser")
            t_list2 = bs2.find_all(name='div', attrs={"class": "Main-p"})
            noticeContent = t_list2[0]
            print(noticeContent)
            cursor = None
            conn = None
            try:
                conn, cursor = mysql_con.get_conn()
                sql_2 = "INSERT INTO Specific_info(noteid,information) VALUES(%s,%s)"
                sql_query = "SELECT id FROM Specific_info WHERE noteid = %s"
                if not cursor.execute(sql_query, noteid):
                    cursor.execute(sql_2, [noteid, noticeContent])
                conn.commit()
            except:
                traceback.print_exc()
            finally:
                mysql_con.close_conn(conn, cursor)
    print(f"{time.asctime()}插入洞头区公共资源交易网采购数据完毕")

if __name__ == '__main__':
    get_res_in_dongtouzy()