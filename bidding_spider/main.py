import dongtou
##import yj
import zjzy
import zjzy2
import time

if __name__ == '__main__':
    print(f'{time.asctime()} 开始爬取招标数据[-------]')
    zjzy.insert_res_in_zfcg_n()
    print(f'{time.asctime()} 开始爬取招标数据[*------]')
    zjzy.insert_res_in_zfcg_g()
    print(f'{time.asctime()} 开始爬取招标数据[**-----]')
    zjzy2.insert_res_in_zfcg_n()
    print(f'{time.asctime()} 开始爬取招标数据[***----]')
    zjzy2.insert_res_in_zfcg_g()
    print(f'{time.asctime()} 开始爬取招标数据[****---]')
    dongtou.get_res_in_dongtouzy()
    print(f'{time.asctime()} 开始爬取招标数据[*****--]')
