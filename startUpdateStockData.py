
import importlib
from Database_Connections import select_ticker_name, Update_StockData
import getYahooData
import threading
import os
import requests
from lxml import html
from bs4 import BeautifulSoup

import simplejson as json
import copy
import base64

def value_to_float(x):
    if type(x) == float or type(x) == int:
        return x
    if 'K' in x:
        if len(x) > 1:
            return int(float(x.replace('K', '')) * 1000)
        return 1000
    if 'M' in x:
        if len(x) > 1:
            return int(float(x.replace('M', '')) * 1000000)
        return 1000000
    if 'B' in x:
        return int(float(x.replace('B', '')) * 1000000000)
    return 0

def main():
    os.chdir('/webapps/StockWebScraping')

    thread_list = []

    rows = select_ticker_name()
    #rows = [('ACER', 'ABEO Therapeutics Inc. Common Stock', 2.36, 'NULL', 'NASDAQ', 'Health Care', 'Major Pharmaceuticals', None)]
    #('ACAD', 'ACAD Therapeutics Inc. Common Stock', 2.36, 'NULL', 'NASDAQ', 'Health Care', 'Major Pharmaceuticals', None)]

    for row in rows:
        print(row[0])
        getPreMarketStockValue_marketwatch(row[0])



#def getPreMarketStockValue(i_stock_ticker):
#    
#    try:
#        url = 'https://finance.yahoo.com/quote/' + i_stock_ticker 
#
#        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
#        result = requests.get(url, headers=headers)
#        #print(result.content.decode())
#        html_content = result.content.decode()
#        soup = BeautifulSoup(html_content, 'html.parser')
#        #print(soup)
#
#        quote_header_panel = soup.find('div', attrs={'id':'quote-header-info'})
#
#        lastPrice_panel = quote_header_panel.find('span', attrs={'data-reactid':'31'})
#        #print(lastPrice_panel.text)
#
#        page = requests.get(url) 
#        tree = html.fromstring(page.content)  
#        stock_price = tree.xpath('/html/body/div[1]/div/div/div/div/div/div[2]/div/div/div/div[3]/div/div/div/div[3]/div[1]/span/text()') 
#        #stock_price = tree.xpath('/html/body/div[1]/div/div/div[1]/div/div[2]/div/div/div[4]/div/div/div/div[3]/div[1]/div/span[1]/text()') 
#        print(stock_price[0])
#        #
#
#        lastPrice = lastPrice_panel.text
#
#        quote_summary_panel = soup.find('div', attrs={'id':'quote-summary'})
#
#        # get tag of stock name
#        table_body = quote_summary_panel.find('tbody')
#
#    
#        rows = table_body.find_all('tr')
#
#        #last price
#        #FIRST_ROW_columns = rows[0].find_all('td')
#        #lastPrice = FIRST_ROW_columns[1].text
#
#        #last volume
#        FIRST_ROW_columns = rows[6].find_all('td')
#        lastVolume = FIRST_ROW_columns[1].text.replace(",", "")
#
#        print(lastPrice)
#        #Update_StockData(i_stock_ticker, lastPrice, lastVolume)
#
#
#    except Exception:
#        print("Entrou na excepção getPreMarketStockValue para o " + i_stock_ticker + " ...")
#        pass


def getVolume_marketwatch(i_stock_ticker):

    try:
        url = 'https://www.marketwatch.com/investing/stock/'+i_stock_ticker
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        result = requests.get(url, headers=headers)
        #print(result.content.decode())
        html_content = result.content.decode()
        soup = BeautifulSoup(html_content, 'html.parser')
        #print(soup)
        articles_volume = soup.find('div', attrs={'class':'column column--full supportive-data'})

        articles_all = articles_volume.findAll('span', attrs={'class':'primary'})
        volume = articles_all[0].text.replace("Volume: ", "")

        return value_to_float(volume)
        #print(value_to_float(volume))

    except Exception:
        print("Entrou na excepção getPreMarketStockValue para o " + i_stock_ticker + " ...")
        pass


def getPreMarketStockValue_marketwatch(i_stock_ticker):

    try:
        url = 'https://www.marketwatch.com/investing/stock/'+i_stock_ticker

        sess = requests.Session()

        headers = {
            'authority': 'www.skroutz.gr',
            'cache-control': 'max-age=0',
            'sec-ch-ua': '"Google Chrome"; v="83"',
            'sec-ch-ua-mobile': '?0',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
            'if-none-match': 'W/"e6fb8187391e99a90270c2351f9d17cd"'
        }

        params = (('o', '\u039C\u03C0\u03BF\u03C5\u03C1\u03BD\u03BF\u03CD\u03B6\u03B9 Guy Laroche Linda Red'),)

        response = sess.get(url, headers=headers, params=params)
        tree = html.fromstring(response.content)
        # hrefs = tree.xpath('//a[@class="js-product-link content-placeholder"]/@href')
        # ids = [x.split('/')[-1] for x in hrefs]
        # headers2 = copy.deepcopy(headers)
        # headers2['content-type'] = 'application/json'
        # ret = sess.post('https://www.skroutz.gr/personalization/product_prices.json', data=json.dumps({'product_ids': ids}), headers=headers2)
        details = tree.xpath('//script[@type="application/ld+json"]')[0]
        # details.text_content() contains the base64 encoded elements within HTML comments
        details_b64 = details.text_content()[4:-3] # strip off the html comments
        #print(details_b64)
        price = json.loads(details_b64)
        lastPrice = price["price"]

        lastVolume = getVolume_marketwatch(i_stock_ticker)

        #print(str(lastPrice))
        #print(str(lastVolume))

        Update_StockData(i_stock_ticker, str(lastPrice), str(lastVolume))

    except Exception:
        print("Entrou na excepção getPreMarketStockValue para o " + i_stock_ticker + " ...")
        pass


if __name__ == "__main__":
    main()