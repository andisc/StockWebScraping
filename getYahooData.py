import requests
from lxml import html
from bs4 import BeautifulSoup
import re
from Database_Connections import Insert_PreMarketData, Update_PreMarketData

def getPreMarketStockValue(i_stock_ticker, var_type):
    
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

        

        stock_value_panel = headerInfo_panel.find('div', attrs={'data-reactid':'29'})

        premarket_value_panel = stock_value_panel.find('p', attrs={'data-reactid':'36'})


        
        #caso exista a secção do pre market 
        if (premarket_value_panel != None):

            #get tag of last price stock
            stock_last_price = headerInfo_panel.find('span', attrs={'data-reactid':'37'}).text

            premarket_grow = premarket_value_panel.find('span', attrs={'data-reactid':'39'})

            stock_name_desc = stock_name.text.split(' (')[0]

            growPrice = premarket_grow.text.split(' ')[0][1:]
            growPriceSinal = premarket_grow.text.split(' ')[0][0:1]

            percentage = premarket_grow.text.split(' ')[1]
            growPricePercentage = percentage.replace("(", "").replace(")", "")[1:-1]
            
            #print(stock_name_desc)
            #print(stock_last_price)
            #print(growPrice)
            #print(growPriceSinal)
            #print(growPricePercentage)

            #if grow is different than zero
            if (float(growPrice) != 0.0 and float(growPricePercentage) != 0.0):

                if (var_type == 'INSERT_PREMARKET'):
                    Insert_PreMarketData(i_stock_ticker, stock_name_desc, stock_last_price, growPrice, growPriceSinal,  growPricePercentage)
                else:
                    Update_PreMarketData(i_stock_ticker, stock_name_desc, stock_last_price, growPrice, growPriceSinal, growPricePercentage)


    except Exception:
        print("Entrou na excepção getPreMarketStockValue para o " + i_stock_ticker + " ...")
        pass


def main():
    getPreMarketStockValue('ALXN', 'INSERT_PREMARKET')

if __name__ == "__main__":
    main()