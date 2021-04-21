
import importlib
from Database_Connections import select_ticker_name, Update_StockData
import getYahooData
import threading
import os
import requests
from lxml import html
from bs4 import BeautifulSoup



def main():
    os.chdir('/var/www/StockWebScraping')

    thread_list = []

    rows = select_ticker_name()
    #rows = [('ABEO', 'ABEO Therapeutics Inc. Common Stock', 2.36, 'NULL', 'NASDAQ', 'Health Care', 'Major Pharmaceuticals', None)]
    #('ACAD', 'ACAD Therapeutics Inc. Common Stock', 2.36, 'NULL', 'NASDAQ', 'Health Care', 'Major Pharmaceuticals', None)]

    for row in rows:
        print(row[0])
        getPreMarketStockValue(row[0])



def getPreMarketStockValue(i_stock_ticker):
    
    try:
        url = 'https://finance.yahoo.com/quote/' + i_stock_ticker 

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        result = requests.get(url, headers=headers)
        #print(result.content.decode())
        html_content = result.content.decode()
        soup = BeautifulSoup(html_content, 'html.parser')
        #print(soup)

        quote_summary_panel = soup.find('div', attrs={'id':'quote-summary'})

        # get tag of stock name
        table_body = quote_summary_panel.find('tbody')

    
        rows = table_body.find_all('tr')

        #last price
        FIRST_ROW_columns = rows[0].find_all('td')
        lastPrice = FIRST_ROW_columns[1].text

        #last volume
        FIRST_ROW_columns = rows[6].find_all('td')
        lastVolume = FIRST_ROW_columns[1].text.replace(",", "")

        Update_StockData(i_stock_ticker, lastPrice, lastVolume)


    except Exception:
        print("Entrou na excepção getPreMarketStockValue para o " + i_stock_ticker + " ...")
        pass





if __name__ == "__main__":
    main()