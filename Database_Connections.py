import sqlite3
from datetime import date, datetime
import pytz
from pathlib import Path


def get_DB_Connection():
    #path = '../CatalystRepository/db.sqlite3'
    path = '../CatalystRepository/CatalystRepository/db.sqlite3'
    return path


def InsertData(i_ticker, i_description, i_url, i_art_date):

    TODAY_DATE = i_art_date
    #NOW = str(datetime.now())
    NOW = str(datetime.now(pytz.timezone('US/Eastern')))

    article_existance = verify_article_existance(i_ticker, i_description, TODAY_DATE)

    if article_existance == True:
        try:
            sqliteConnection = sqlite3.connect(get_DB_Connection())
            cursor = sqliteConnection.cursor()
            
            #sqlite_insert_query = """INSERT INTO "teste" (id, nome,  descricao) VALUES (3, 'nome 3 xxyy', 'descricao nome')"""
            sqlite_insert_query = """INSERT INTO Stocks_Articles (article_text, article_link, article_date, creation_datetime, stock_ticker_id) VALUES ('""" + i_description + """', '""" + i_url + """', '""" + TODAY_DATE + """', '""" + NOW + """', '""" + i_ticker + """')"""

            count = cursor.execute(sqlite_insert_query)
            sqliteConnection.commit()
            print("Record inserted successfully into Stocks_Articles table ", cursor.rowcount)
            cursor.close()

        except sqlite3.Error as error:
            print("Failed to insert data into Stocks_Articles table", error)
        finally:
            if sqliteConnection:
                sqliteConnection.close()
    else:
        print("sai")


def select_ticker_name():
   
    try:
        sqliteConnection = sqlite3.connect(get_DB_Connection())
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT * FROM stocks WHERE active=1")

        rows = cursor.fetchall()
        cursor.close()
        return rows

    except sqlite3.Error as error:
        print("Failed to retrieve data from sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def verify_article_existance(i_ticker, i_description, i_today_date):
       

    try:
        sqliteConnection = sqlite3.connect(get_DB_Connection())
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT article_text FROM Stocks_Articles WHERE stock_ticker_id='" + i_ticker + "' AND article_date = '" + i_today_date + "'")

        rows = cursor.fetchall()

        for row in rows:
            if(row[0] in i_description):
                cursor.close()
                return False

        cursor.close()
        return True

    except sqlite3.Error as error:
        print("Failed to get data into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()



def Insert_ProcessingControl():
    #database = r"C:\sqlite\db\pythonsqlite.db"
    #/Users/andregama/Documents/WebScraping/TESTE

    #NOW = str(datetime.now())
    NOW = str(datetime.now(pytz.timezone('US/Eastern')))

    try:
        sqliteConnection = sqlite3.connect(get_DB_Connection())
        cursor = sqliteConnection.cursor()

        
        sqlite_insert_query = """INSERT INTO Processing_Control (initial_creation_datetime, final_creation_datetime) VALUES ('""" + NOW + """', 'NULL')"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Record inserted successfully into Processing_Control table ", cursor.rowcount)
        cursor.close()

        max_id_Control = select_max_Processing_Control()
        return max_id_Control

    except sqlite3.Error as error:
        print("Failed to insert data into Processing_Control table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def Update_ProcessingControl(id_control):
    #database = r"C:\sqlite\db\pythonsqlite.db"
    #/Users/andregama/Documents/WebScraping/TESTE

    #NOW = str(datetime.now())
    NOW = str(datetime.now(pytz.timezone('US/Eastern')))

    try:
        sqliteConnection = sqlite3.connect(get_DB_Connection())
        cursor = sqliteConnection.cursor()

        #sqlite_insert_query = """INSERT INTO Processing_Control (initial_creation_datetime, final_creation_datetime) VALUES ('""" + NOW + """', 'NULL')"""
        sqlite_insert_query = """UPDATE Processing_Control SET final_creation_datetime = '""" + NOW + """' WHERE id_control = '""" + str(id_control) + """'"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Record updated successfully into Processing_Control table ", cursor.rowcount)
        cursor.close()


    except sqlite3.Error as error:
        print("Failed to update data into Processing_Control table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def select_max_Processing_Control():
   
    try:
        sqliteConnection = sqlite3.connect(get_DB_Connection())
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT MAX(id_Control) FROM Processing_Control")

        rows = cursor.fetchone()
        max_id_Control = rows[0]
        cursor.close()
        
        return max_id_Control

    except sqlite3.Error as error:
        print("Failed to get data from Processing_Control", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()



def Insert_Logging(id_control, state, message):

    #NOW = str(datetime.now())
    NOW = str(datetime.now(pytz.timezone('US/Eastern')))

    try:
        sqliteConnection = sqlite3.connect(get_DB_Connection())
        cursor = sqliteConnection.cursor()

        
        sqlite_insert_query = """INSERT INTO Logging (log_state, log_message, creation_datetime, id_control_id) VALUES ('""" + state + """', '""" + message + """', '""" + NOW + """', '""" + str(id_control) + """')"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Record inserted successfully into Logging table ", cursor.rowcount)
        cursor.close()


    except sqlite3.Error as error:
        print("Failed to insert data into Logging table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()



def Update_StockData(i_ticker, i_lastPrice, i_lastVolume):
    #database = r"C:\sqlite\db\pythonsqlite.db"
    #/Users/andregama/Documents/WebScraping/TESTE

    #NOW = str(datetime.now())
    NOW = str(datetime.now(pytz.timezone('US/Eastern')))

    try:
        sqliteConnection = sqlite3.connect(get_DB_Connection())
        cursor = sqliteConnection.cursor()

        sqlite_update_query = """UPDATE Stocks SET last_price = '""" + i_lastPrice + """', volume = '""" + i_lastVolume + """' WHERE stock_ticker = '""" + i_ticker + """'"""

        count = cursor.execute(sqlite_update_query)
        sqliteConnection.commit()
        print("Record updated successfully into Stocks table ", cursor.rowcount)
        cursor.close()


    except sqlite3.Error as error:
        print("Failed to update data into Stocks table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def select_max_PreMarketData():
       
    try:
        sqliteConnection = sqlite3.connect(get_DB_Connection())
        cursor = sqliteConnection.cursor()
        cursor.execute("SELECT MAX(updated_datetime) FROM PreMarketStocks")

        rows = cursor.fetchone()
        max_updated_datetime = rows[0]
        cursor.close()
        
        return max_updated_datetime

    except sqlite3.Error as error:
        print("Failed to get data from PreMarketStocks", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def delete_PreMarketData():
       
    try:
        sqliteConnection = sqlite3.connect(get_DB_Connection())
        cursor = sqliteConnection.cursor()

        
        sqlite_delete_query = "DELETE FROM PreMarketStocks"

        count = cursor.execute(sqlite_delete_query)
        sqliteConnection.commit()
        print("Record deleted successfully into PreMarketStocks table ", cursor.rowcount)
        cursor.close()

    except sqlite3.Error as error:
        print("Failed to get data from PreMarketStocks", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()


def Insert_PreMarketData(i_ticker, i_tickerName, i_Price, i_growPrice, i_growPriceSinal, i_growPricePercentage):
    
    #NOW = str(datetime.now())
    NOW = str(datetime.now(pytz.timezone('US/Eastern')))

    try:
        sqliteConnection = sqlite3.connect(get_DB_Connection())
        cursor = sqliteConnection.cursor()

        
        sqlite_insert_query = """INSERT INTO PreMarketStocks (stock_ticker, stock_name, last_price, grow_price, grow_price_sinal, grow_percentage, active, updated_datetime )  VALUES ('""" + i_ticker + """', '""" + i_tickerName + """', '""" + i_Price + """', '""" + i_growPrice + """', '""" + i_growPriceSinal + """', '""" + i_growPricePercentage + """', '1', '""" + NOW + """')"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Record inserted successfully into PreMarketStocks table ", cursor.rowcount)
        cursor.close()


    except sqlite3.Error as error:
        print("Failed to insert data into PreMarketStocks table", error)

    finally:
        if sqliteConnection:
            sqliteConnection.close()



def Update_PreMarketData(i_ticker, i_tickerName, i_Price, i_growPrice, i_growPriceSinal, i_growPricePercentage):

    #NOW = str(datetime.now())
    NOW = str(datetime.now(pytz.timezone('US/Eastern')))

    try:
        sqliteConnection = sqlite3.connect(get_DB_Connection())
        cursor = sqliteConnection.cursor()

        #sqlite_insert_query = """INSERT INTO Processing_Control (initial_creation_datetime, final_creation_datetime) VALUES ('""" + NOW + """', 'NULL')"""
        sqlite_insert_query = """UPDATE PreMarketStocks SET last_price = '""" + i_Price + """', grow_price = '""" + i_growPrice + """', grow_price_sinal = '""" + i_growPriceSinal + """', grow_percentage = '""" + i_growPricePercentage + """', updated_datetime = '""" + NOW + """' WHERE stock_ticker = '""" + i_ticker + """'"""

        count = cursor.execute(sqlite_insert_query)
        sqliteConnection.commit()
        print("Record updated successfully into PreMarketStocks table ", cursor.rowcount)
        cursor.close()

        if sqliteConnection:
            sqliteConnection.close()
        #if no one row was affected the systems will go insert a new record
        if(cursor.rowcount == 0):
            Insert_PreMarketData(i_ticker, i_tickerName, i_Price, i_growPrice, i_growPriceSinal, i_growPricePercentage)


    except sqlite3.Error as error:
        print("Failed to update data into PreMarketStocks table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()

