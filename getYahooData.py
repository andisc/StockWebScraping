import requests
from lxml import html
from bs4 import BeautifulSoup
import re

def getPreMarketStockValue(i_stock_ticker):
    
    try:
        url = 'https://finance.yahoo.com/quote/' + i_stock_ticker 

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        result = requests.get(url, headers=headers)
        #print(result.content.decode())
        html_content = result.content.decode()
        soup = BeautifulSoup(html_content, 'html.parser')
        #print(soup)

        headerInfo_panel = soup.find('div', attrs={'id':'quote-header-info'})

        # get tag of stock name
        stock_name = headerInfo_panel.find('h1', attrs={'data-reactid':'7'})

        #get tag of last price stock
        stock_last_price = headerInfo_panel.find('span', attrs={'data-reactid':'32'})

        stock_value_panel = headerInfo_panel.find('div', attrs={'data-reactid':'29'})

        premarket_value_panel = stock_value_panel.find('p', attrs={'data-reactid':'36'})

        premarket_grow = premarket_value_panel.find('span', attrs={'data-reactid':'39'})

        print(stock_name.text.split(' (')[0])
        print(stock_last_price.text)

        result1 = premarket_grow.text.split(' ')[0]
        print(result1)

        result2 = premarket_grow.text.split(' ')[1]
        print(result2.replace("(", "").replace(")", ""))

        #businessSummary = businessSummary_panel.find('p')
#
        #print(businessSummary.text)
#
        #obj = Stocks.objects.get(stock_ticker=i_stock_ticker)
        #obj.businessSummary = businessSummary.text.replace("'", "''")
        #obj.save()


    except Exception:
        print("Entrou na excepção getPreMarketStockValue para o " + i_stock_ticker + " ...")
        pass


def main():
    getPreMarketStockValue('gnpx')

if __name__ == "__main__":
    main()