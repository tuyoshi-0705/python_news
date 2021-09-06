

from bs4 import BeautifulSoup
import requests as req
import pandas as pd
import re

# 処理をクラスにまとめる   
class List:
    
    #コンストラクタにURL+ページの数を呼べるようにする
    def __init__(self, page):
        self.url = "https://news.yahoo.co.jp/topics/top-picks?page="+str(page)
    
    #以下処理メソッドをまとめる
    def yahoo_s(self):
        
        #ヤフーニュースの情報を取得する
        res = req.get(self.url)
        #print(res)
        
        #BeautifulSoupにヤフーニュースのページ内容を読み込ませる
        yahoo_html = BeautifulSoup(res.text,'html.parser')
        #ヤフーニュースのタイトルとURLの情報を取得する
        news_list = []
        url_list = []
        data_list = yahoo_html.find_all(href=re.compile("news.yahoo.co.jp/pickup"))
    
        #ヤフーニューズのタイトルをリストに格納
        for yahoo_data in yahoo_html.select('.newsFeed_item_title'):
            news_list.append(yahoo_data.string)
        # print(news_list)
        
        #ヤフーニュースのURLをリストに格納する
        for kaka in data_list:
            url_list.append(kaka.attrs['href'])
        # print(url_list)
        return news_list


#二次元内包表記にてリストに格納
all_list = []
all_coronalist = []
for i in range(10):
    page = List(page=i+1)
    plist = page.yahoo_s()
    all_list.append(plist)
    
    #リスト内の,コロナに関係するワードのみを格納
    l_in = [s for s in plist if 'コロナ' in s or '感染' in s]

    all_coronalist.append(l_in)

#print(allcoronalist)

#二次元リストを一次元にして格納
all_corona_news = sum(all_coronalist, [])

title_list_corona = pd.DataFrame({'Title':all_corona_news})

title_list_corona.to_csv('corona_csv')


#必要な変数を設定
#取得したトークン
TOKEN = 'afUaL44902wfil2Xshx4bd53sYpb47CSygCAuISpjc4'
#APIのURL
api_url ='https://notify-api.line.me/api/notify'
#通知内容
send_contents = all_corona_news


#情報を辞書型にする
TOKEN_dic = {'Authorization':'Bearer' + ' ' + TOKEN}
send_dic = {'message': send_contents}
print(TOKEN_dic)
print(send_dic)

#LINE通知を送る(200: 成功時、400: リクエストが不正、401: アクセストークンが無効: 公式より)
#()内は、アクセスするWEB APIのURL、認証情報、送りたい内容
req.post(api_url, headers=TOKEN_dic, data=send_dic)





















