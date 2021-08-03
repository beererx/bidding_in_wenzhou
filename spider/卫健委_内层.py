import requests
import re


url = "https://wsjkw.zj.gov.cn/art/2021/7/27/art_1229123471_4694545.html"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edg/91.0.864.67"
}

resp = requests.get(url, headers=headers)
resp.encoding='utf-8'
page_content = resp.text

#解析数据
obj = re.compile(r'<div id="zoom">(?P<text>.*?)</div>', re.S)
#开始匹配
result = obj.finditer(page_content)
for it in result:
    res = it.group("text")
print(res)


