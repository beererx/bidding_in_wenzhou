import requests
import re
import mysql_con
import json
from bs4 import BeautifulSoup
import traceback


url = "http://search.zj.gov.cn/jrobotfront/interfaces/cateSearch.do"
str1 = {"存款招标", "账户招标"}
for j in str1:
    for i in range(3):#翻页
        param = {
            "websiteid": "330324000000000",
            "pg": "10",
            "p": i,
            "tpl": "2306",
            "cateid": "370",
            "word": j,
            "checkError": "1",
            "isContains": "1",
            "Municipal_webid": "330301000000000",
            "Municipal_name": "溫州市",
            "q": j,
            "sortType": "1",
        }
        resp = requests.post(url, params=param)
        page_content = resp.text
        page_dic = json.loads(resp.text)
        result = page_dic['result']

        for i in result:
            bs = BeautifulSoup(i, "html.parser")
            bs_a = bs.select('a')
            #print(type(str(bs_a[0])))
            pattern_noteid = re.compile(r'art_(?P<text>.*?).html', re.S)
            noteid = re.findall(pattern_noteid, str(bs_a[0]))

            href = bs_a[0].get("href")

            pattern_date = re.compile(r'art/(?P<text>.*?)/art_', re.S)
            date = re.findall(pattern_date, str(bs_a[0]))

            pattern_title = re.compile(r'<a class.*?>(?P<text>.*?)</a>', re.S)
            title2_list = re.findall(pattern_title, str(bs_a[0]))
            title2 = str(title2_list)
            title = title2.replace("<em>", "").replace("</em>", "").replace("</em>", "")[12:]
            if len(title) > 2:
                title = title
                href = href
                cut = title.find('\\r')
                title= title[:cut:]

                str2 = {"招标", "邀标", "询价", "竞谈", "单一", "竞价", "变更", "更正"}

                for j in str2:
                    a = title.find(j)
                    if a != -1:
                        cursor = None
                        conn = None
                        try:
                            conn, cursor = mysql_con.get_conn()
                            sql = "INSERT INTO General_info(noteid, title, district_name, link, category, date) VALUES(%s, %s, %s, %s, %s, %s)"
                            sql_query = "SELECT id FROM General_info WHERE noteid = %s"
                            if not cursor.execute(sql_query, noteid):
                                cursor.execute(sql, [noteid, title, "永嘉县", href, 3, date])
                            conn.commit()
                        except:
                            traceback.print_exc()
                        finally:
                            mysql_con.close_conn(conn, cursor)

                        print("General Successful!")
    #内层
                        headers = {
                            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67"
                        }

                        resp = requests.get(href, headers=headers)

                        resp.encoding = 'utf-8'  # 解决中文乱码问题
                        page_content = resp.text

                        # 解析数据
                        obj = re.compile(r'<div id="zoom".*? 2em;">(?P<text>.*?)</br>', re.S)

                        # 开始匹配
                        result = re.findall(obj, page_content)

                        for it in result:
                            title = title
                            # text = it.group("text")
                            title = "<h1>" + title + "</h1>"  # 字体设置为h1
                            content = title + it
                            print(content)

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

                #
                #
            #
