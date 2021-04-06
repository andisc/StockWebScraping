import requests
from lxml import html
from bs4 import BeautifulSoup
import os

from datetime import date, datetime

from ValidationTools import validateday
from Database_Connections import InsertData, Insert_Logging


def main(id_control):
    try:
        url = 'https://atos.net/en/press-releases' 

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        result = requests.get(url, headers=headers)
        #print(result.content.decode())
        html_content = result.content.decode()
        soup = BeautifulSoup(html_content, 'html.parser')
        #print(soup)
        articles = soup.findAll('div', attrs={'class':'pl_grid-item pl_col-sm-3'})
        
        # get first article
        FIRST_ARTICLE = articles[0]
        
        article_date_panel = FIRST_ARTICLE.find('div', attrs={'class':'blog-text clamp-me'})
        all_div = article_date_panel.findAll('div')
        article_date = all_div[0]
        article_desc = FIRST_ARTICLE.find('h2')
        
        v_article_date = article_date.text.lstrip().rstrip()

        #if the process find any article with the today date
        istoday, v_art_date = validateday(v_article_date)

        
        print("URL: " )
        print("DESCRIPTION: " + article_desc.text.lstrip().rstrip())
        now = datetime.now()
        print("ARTICLE_DATE: " + str(now))

    except Exception:
            error_message = "Entrou na excepção ao tratar " + os.path.basename(__file__) + "..."
            print(error_message)
            Insert_Logging(id_control, 'Detail', error_message)
            pass

    #InsertData()
    
        
 
if __name__ == "__main__":
    main()
