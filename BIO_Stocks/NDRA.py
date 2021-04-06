import requests
from lxml import html
from bs4 import BeautifulSoup
import os

from datetime import date, datetime

from ValidationTools import validateday
from Database_Connections import InsertData, Insert_Logging


def main(id_control):
    try:
        url = 'https://investors.endrainc.com/NDRA/press_releases?template=pr_ndra' 

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        result = requests.get(url, headers=headers)
        #print(result.content.decode())
        html_content = result.content.decode()
        soup = BeautifulSoup(html_content, 'html.parser')
        #print(soup)
        articles_panel = soup.find('ul', attrs={'class':'js-list list-news ir_releases'})
        articles = articles_panel.findAll('li', attrs={'class':'item group ir_release'})
        
        # get first article
        FIRST_ARTICLE = articles[0]

        article_date = FIRST_ARTICLE.find('p', attrs={'class':'perex'})
        all_a = FIRST_ARTICLE.findAll('a')
        article_desc = all_a[0]
        
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

    #InsertData()
    
        
 
if __name__ == "__main__":
    main()