
import importlib
from Database_Connections import select_ticker_name, Insert_ProcessingControl, Update_ProcessingControl, Insert_Logging
import threading
import os
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import concurrent.futures
import multiprocessing
from concurrent.futures import ProcessPoolExecutor 
from multiprocessing import cpu_count 


def getdata(ticker):

    # Inicia o processamento com a data de inicio
    id_control = Insert_ProcessingControl()

    #print(ticker)
    try:
        module = importlib.import_module('BIO_Stocks.' + ticker)
        my_class = getattr(module, "main")(id_control)
        #_ = my_class()
    except:
        print("Failed to get stock data from " + ticker)
        Insert_Logging(id_control, 'Geral', "Failed to get stock data from " + ticker)

    # Fecha o processamento com a data de conclusão
    Update_ProcessingControl(id_control)



def main():
    print("Entra")
#    os.chdir('/webapps/StockWebScraping')
 
 
     # Inicia o processamento com a data de inicio
#    id_control = Insert_ProcessingControl()
# 
#    thread_list = []
# 
    rows = select_ticker_name()
#     #rows = [('ABIO', 'ABEO Therapeutics Inc. Common Stock', 2.36, 'NULL', 'NASDAQ', 'Health Care', 'Major Pharmaceuticals', None)]
#     #('ACAD', 'ACAD Therapeutics Inc. Common Stock', 2.36, 'NULL', 'NASDAQ', 'Health Care', 'Major Pharmaceuticals', None)]
#
#    for row in rows:
#        #print(row[0])
#
#        try:
#            thread = threading.Thread(target=getdata, args=(row[0],)) 
#            thread_list.append(thread)
#
#        except:
#            print("Failed to get stock data")
#
#
#    for thread in thread_list:
#        thread.start()
#    for thread in thread_list:
#        thread.join(timeout=3)


    #print(len(rows))
#    for x in range(0, len(rows), 1):
#        print(rows[x][0])
#        getdata(rows[x][0])
        #print(rows[x+1][0])
        #print(rows[x+2][0])
        #print(rows[x+4][0])
        #t1 = threading.Thread(target=getdata, args=(rows[x][0],)) 
        #t2 = threading.Thread(target=getdata, args=(rows[x+1][0],)) 
        #t3 = threading.Thread(target=getdata, args=(rows[x+2][0],)) 
        #t4 = threading.Thread(target=getdata, args=(rows[x+3][0],)) 

        #t1.start()
        #t2.start()
        #t3.start()
        #t4.start()

        #t1.join()
        #t2.join()
        #t3.join()
        #t4.join()


#################
    executor = ProcessPoolExecutor(max_workers=cpu_count()) 
    tasks = [ 
        executor.submit(getdata, row[0]) 
        for row in rows
    ] 
    doneTasks, _ = concurrent.futures.wait(tasks) 

    results = [ 
        item.result() 
        for item in doneTasks 
    ] 

 
 
    # Fecha o processamento com a data de conclusão
#    Update_ProcessingControl(id_control)
 
    os.system("pkill -f 'start.py'")


#-------------------------------------

#    id_control = Insert_ProcessingControl()
#    module = importlib.import_module('BIO_Stocks.AADI')
#    my_class = getattr(module, "main")
#    instance = my_class(id_control)
#    Update_ProcessingControl(id_control)



if __name__ == "__main__":
    main()