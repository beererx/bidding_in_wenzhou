import requests
import re


url = "http://www.yj.gov.cn/art/2015/8/12/art_1229155880_1263613.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67"
}

resp = requests.get(url, headers=headers)
resp.encoding='utf-8' #解决中文乱码问题
page_content = resp.text

#解析数据
obj = re.compile(r'<title>(?P<title>.*?)</title>.*?<div id="zoom".*?<p>(?P<text>.*?)<br/></p><p><br/></p></div>', re.S)

#开始匹配
result = obj.finditer(page_content)
for it in result:
    title = it.group("title")
    text = it.group("text")
title = "<h1>"+title+"</h1>" #字体设置为h1
content = title + text
print(content)



