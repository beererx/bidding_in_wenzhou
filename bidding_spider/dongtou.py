import requests
import time
import traceback
import mysql_con
import random
from bs4 import BeautifulSoup

def get_keyword(i):
    if i == 0:
        keyword = '闲置资金'
    else:
        keyword = '竞争性存放'
    return keyword


user_agent = ['Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)'
              ' Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3870.400 QQBrowser/10.8.4405.400',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
              'Chrome/92.0.4515.131 Safari/537.36',
              'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko)'
              ' Chrome/92.0.4515.131 Safari/537.36 Edg/92.0.902.67',
              'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; WOW64; Trident/5.0)',
              'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/535.1 (KHTML, like Gecko) ',
              'Chrome/13.0.782.41 Safari/535.1 QQBrowser/6.9.11079.201',
              "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) "
              "Chrome/68.0.3440.106 Safari/537.36"
              ]

def get_res_in_dongtouzy():
    #print(f'{time.asctime()}开始插入洞头区公共资源交易网采购数据')
    for x in range(2):
        keyword = get_keyword(x)
        for y in range(3):
            if y == 0:
                url = "http://ztb.dongtou.gov.cn/dtcms/search.jspx"
            else:
                url = "http://ztb.dongtou.gov.cn/dtcms/search_"+str(y+1)+".jspx"
            params = {"q": keyword
                      }
            headers = {
                "User-Agent": random.choice(user_agent)
                       }
            #time.sleep(5)
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
                    time.sleep(5)
                    url2 = "http://ztb.dongtou.gov.cn/dtcms/"+noteid+".htm"
                    res2 = requests.get(url2, headers=headers)
                    html2 = res2.text
                    bs2 = BeautifulSoup(html2, "html.parser")
                    t_list2 = bs2.find_all(name='div', attrs={"class": "Main-p"})
                    noticeContent = t_list2[0]
                    #print(noticeContent)
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
    #print(f"{time.asctime()}插入洞头区公共资源交易网采购数据完毕")

if __name__ == '__main__':
    get_res_in_dongtouzy()