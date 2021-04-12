import requests
from lxml import html
from bs4 import BeautifulSoup
import os

from datetime import date, datetime

from ValidationTools import validateday
from Database_Connections import InsertData, Insert_Logging


def main(id_control):

    try:
        url = 'https://www.vandapharma.com/investors/#news' 

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        result = requests.get(url, headers=headers)
        #print(result.content.decode())
        html_content = result.content.decode()
        soup = BeautifulSoup(html_content, 'html.parser')
        #print(soup)
        articles_panel = soup.find('section', attrs={'id':'recentNews'})
        
        articles_panel_intern = articles_panel.find('div', attrs={'class':'col-md-8 col-lg-8 col-xl-8'})
        articles = articles_panel_intern.findAll('div')
        
        # get first article
        FIRST_ARTICLE = articles[2]
        
        article_date = FIRST_ARTICLE.find('h6')
        article_desc = FIRST_ARTICLE.find('a')
        
        v_article_date = article_date.text.lstrip().rstrip()

        #if the process find any article with the today date
        istoday, v_art_date = validateday(v_article_date)

        if (istoday == True):
            v_ticker = os.path.basename(__file__).replace(".py", "")
            v_url = article_desc.get('href')
            v_description = article_desc.text.lstrip().rstrip()
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
