
import importlib
from Database_Connections import select_ticker_name, Insert_ProcessingControl, Update_ProcessingControl, Insert_Logging
import getYahooData
import threading
import os


def getdata(ticker):
    try:
        #module = importlib.import_module('BIO_Stocks.' + ticker)
        #my_class = getattr(module, "main")(ticker)
        #instance = my_class()
        getYahooData.getPreMarketStockValue(ticker)
    except:
        print("Failed to get stock data from " + ticker)


def main():
    #os.chdir('/var/www/StockWebScraping')

    thread_list = []

    rows = select_ticker_name()
    #rows = [('ABEO', 'ABEO Therapeutics Inc. Common Stock', 2.36, 'NULL', 'NASDAQ', 'Health Care', 'Major Pharmaceuticals', None)]
    #('ACAD', 'ACAD Therapeutics Inc. Common Stock', 2.36, 'NULL', 'NASDAQ', 'Health Care', 'Major Pharmaceuticals', None)]

    for row in rows:
        print(row[0])

        try:
            thread = threading.Thread(target=getdata, args=(row[0], )) 
            thread_list.append(thread)

        except:
            print("Failed to get stock data")


    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()



if __name__ == "__main__":
    main()