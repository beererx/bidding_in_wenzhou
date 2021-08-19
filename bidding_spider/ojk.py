import requests
import re
import mysql_con
import json
import jsonpath
from bs4 import BeautifulSoup
import traceback
import time
import pymysql

url = "http://search.zj.gov.cn/jsearchfront/interfaces/cateSearch.do"
str1 = {"存款招标", "账户招标"}
for j in str1:
    for i in range(2):  # 翻页
        param = {
            "websiteid": "330355000000000",
            "pg": "10",
            "p": i,
            "tpl": "1569",
            "cateid": "370",
            "word": j,
            "checkError": "1",
            "isContains": "1",
            "q": j,
            "sortType": "2",
        }
        resp = requests.post(url, params=param)
        page_content = resp.text
        page_dic = json.loads(resp.text)
        result = page_dic['result']


        for i in result:
            bs = BeautifulSoup(i, "html.parser")
            bs_a = bs.select('a')

            pattern_noteid = re.compile(r'art_(?P<text>.*?).html', re.S)
            noteid = re.findall(pattern_noteid, str(bs_a[0]))
            #print(noteid)

            href = bs_a[0].get("href")
            href = "http://search.zj.gov.cn/jsearchfront/" + href
            #print(href)


            pattern_date = re.compile(r'gov.cn%2Fart%2F(?P<text>.*?)%2Fart', re.S)
            date = re.findall(pattern_date, str(bs_a[0]))
            date = str(date)
            date = date.replace('%2F', '/')
            #print(date)

            pattern_title = re.compile(r'target="_blank">(?P<text>.*?)</a>', re.S)
            title2_list = re.findall(pattern_title, str(bs_a[0]))
            title2 = str(title2_list)
            title = title2.replace("<em>", "").replace("</em>", "").replace("</em>", "")
            #print(title)



            str2 = {"招标", "邀标", "询价", "竞谈", "单一", "竞价", "变更", "更正"}

            for j in str2:
                # print(j)
                a = title.find(j)
                a = a + a
                # print(a)
            if a != -8:
                cursor = None
                conn = None
                try:
                    conn, cursor = mysql_con.get_conn()
                    sql = "INSERT INTO General_info(noteid, title, district_name, link, category, date) VALUES(%s, %s, %s, %s, %s, %s)"
                    sql_query = "SELECT id FROM General_info WHERE noteid = %s"
                    if not cursor.execute(sql_query, noteid):
                        cursor.execute(sql, [noteid, title, "瓯江口", href, 4, date])
                    conn.commit()
                except:
                    traceback.print_exc()
                finally:
                    mysql_con.close_conn(conn, cursor)

                print("General Successful!")
                # 内层
                headers = {
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62"
                }



                resp = requests.get(href, headers=headers)

                resp.encoding = 'utf-8'  # 解决中文乱码问题
                page_content = resp.text

                # 解析数据
                obj = re.compile(r'<div id="zoom".*?<span style="font-family: 宋体;">(?P<text>.*?)</p></div>', re.S)

                 # 开始匹配
                result = re.findall(obj, page_content)
                #print(result)
                for it in result:
                    #print(it)
                    title = title
                    # text = it.group("text")
                    title = "<h1>" + title + "</h1>"  # 字体设置为h1
                    content = title + it

                    cursor = None
                    conn = None
                    try:
                         conn, cursor = mysql_con.get_conn()
                         sql_2 = "INSERT INTO Specific_info(noteid,information) VALUES(%s,%s)"
                         sql_query = "SELECT id FROM Specific_info WHERE noteid = %s"
                         if not cursor.execute(sql_query, noteid):
                             cursor.execute(sql_2, [noteid, content])
                         conn.commit()
                    except:
                         traceback.print_exc()
                    finally:
                         mysql_con.close_conn(conn, cursor)
                    print("Specific Successful!")

