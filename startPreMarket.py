
import importlib
from Database_Connections import select_ticker_name, select_max_PreMarketData, delete_PreMarketData
import getYahooData
import threading
import os
from datetime import date, datetime


def getdata(ticker, var_type):
    try:
        #module = importlib.import_module('BIO_Stocks.' + ticker)
        #my_class = getattr(module, "main")(ticker)
        #instance = my_class()
        getYahooData.getPreMarketStockValue(ticker, var_type)
    except:
        print("Failed to get stock data from " + ticker)


def main():
    #os.chdir('/webapps/StockWebScraping')

    thread_list = []

    rows = select_ticker_name()
    #rows = [('ABEO', 'ABEO Therapeutics Inc. Common Stock', 2.36, 'NULL', 'NASDAQ', 'Health Care', 'Major Pharmaceuticals', None)]
    #('ACAD', 'ACAD Therapeutics Inc. Common Stock', 2.36, 'NULL', 'NASDAQ', 'Health Care', 'Major Pharmaceuticals', None)]
    
    max_date_PreMarket = select_max_PreMarketData()


    var_type = 'INSERT_PREMARKET'

    if(max_date_PreMarket != None):
        max_date_PreMarket = str(max_date_PreMarket)[0:26]
        max_date = datetime.strptime(max_date_PreMarket, '%Y-%m-%d %H:%M:%S.%f').date()
        var_type = 'UPDATE_PREMARKET'

        #if date is different of today
        if(max_date < date.today()):
            delete_PreMarketData()
            var_type = 'INSERT_PREMARKET'

    print(var_type)


    for row in rows:
        print(row[0])

        try:
            thread = threading.Thread(target=getdata, args=(row[0], var_type,)) 
            thread_list.append(thread)

        except:
            print("Failed to get stock data")


    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()


    os.system("pkill -f 'startPreMarket.py'")


if __name__ == "__main__":
    main()