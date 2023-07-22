
import importlib
from Database_Connections import select_ticker_name, Insert_ProcessingControl, Update_ProcessingControl, Insert_Logging
import threading
import os


def getdata(ticker, id_control):
    try:
        module = importlib.import_module('BIO_Stocks.' + ticker)
        my_class = getattr(module, "main")(id_control)
        #instance = my_class()
    except:
        print("Failed to get stock data from " + ticker)
        Insert_Logging(id_control, 'Geral', "Failed to get stock data from " + ticker)


def main():
    print("Entra")
    os.chdir('/webapps/StockWebScraping')


    # Inicia o processamento com a data de inicio
    id_control = Insert_ProcessingControl()

    thread_list = []

    rows = select_ticker_name()
    #rows = [('ABEO', 'ABEO Therapeutics Inc. Common Stock', 2.36, 'NULL', 'NASDAQ', 'Health Care', 'Major Pharmaceuticals', None),
    #('ACAD', 'ACAD Therapeutics Inc. Common Stock', 2.36, 'NULL', 'NASDAQ', 'Health Care', 'Major Pharmaceuticals', None)]

    for row in rows:
        print(row[0])

        try:
            thread = threading.Thread(target=getdata, args=(row[0], id_control,)) 
            thread_list.append(thread)

        except:
            print("Failed to get stock data")


    for thread in thread_list:
        thread.start()
    for thread in thread_list:
        thread.join()


    # Fecha o processamento com a data de conclusão
    Update_ProcessingControl(id_control)

    os.system("pkill -f 'start.py'")


#module = importlib.import_module('BIO_Stocks.template_table')
#
#
#my_class = getattr(module, "main")
#instance = my_class()

#-------------------------------------

##module = __import__("BIO_Stocks.RVNC")
#module = importlib.import_module('BIO_Stocks.RVNC')
#
#my_class = getattr(module, "main")
#instance = my_class()
#
##-------------------------------------
#
#module = importlib.import_module('Microsoft_teste')
#
#my_class = getattr(module, "main")
#instance = my_class()


if __name__ == "__main__":
    main()