import requests
from lxml import html
from bs4 import BeautifulSoup
import os

from datetime import date, datetime

from ValidationTools import validateday
from Database_Connections import InsertData, Insert_Logging


def main(id_control):

    try:
        url = 'https://www.pdsbiotech.com/investors/news-center/press-releases/' 

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        result = requests.get(url, headers=headers)
        #print(result.content.decode())
        html_content = result.content.decode()
        soup = BeautifulSoup(html_content, 'html.parser')
        #print(soup)

        table_panel = soup.find('div', attrs={'itemprop':'articleBody'})
        table = table_panel.find('table')
        #print(table)
        #table_body = table.find('tbody')
        rows = table.find_all('tr')

        
        FIRST_ROW_columns = rows[0].find_all('td')
        article_date_day = FIRST_ROW_columns[0].find('p', attrs={'class':'dia'}).text.lstrip().rstrip()
        article_date_month = FIRST_ROW_columns[0].find('p', attrs={'class':'mes'}).text.lstrip().rstrip()
        v_article_date = (article_date_day + ' ' + article_date_month + ' ' + str(datetime.now().year))
        article_desc = FIRST_ROW_columns[1]

        #if the process find any article with the today date
        istoday, v_art_date = validateday(v_article_date)
        if (istoday == True):
            v_ticker = os.path.basename(__file__).replace(".py", "")
            v_url = article_desc.a.get('href')
            v_description = article_desc.a.text.lstrip().rstrip()
            now = datetime.now()
            
            print("URL: " + v_url)
            print("DESCRIPTION: " + v_description)
            print("ARTICLE_DATE: " + str(now))

            # Insert articles 
            if "https://" in v_url:
                InsertData(v_ticker, v_description, v_url, v_art_date)
            else:
                InsertData(v_ticker, v_description, url, v_art_date)

    except Exception:
            error_message = "Entrou na excepção ao tratar " + os.path.basename(__file__) + "..."
            print(error_message)
            Insert_Logging(id_control, 'Detail', error_message)
            pass
    
        
 
if __name__ == "__main__":
    main()