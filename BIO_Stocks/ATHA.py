from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import os
import gzip

from datetime import date, datetime

from ValidationTools import validateday
from Database_Connections import InsertData, Insert_Logging


def main(id_control):
    try:
        url = 'https://investors.athira.com/news-and-events/press-releases/' 

        
        req = Request(
            url=url, 
            headers={'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Mobile Safari/537.36'}
        )
        req.add_header('Accept-Language', 'pt-PT,pt;q=0.9,en-US;q=0.8,en;q=0.7')
        req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7')
        req.add_header('Referer', 'https://www.google.com/')

        page = urlopen(req, timeout=4)
        html_bytes = page.read()
        #print(result.content.decode())
        html_content = html_bytes.decode('utf-8')
        soup = BeautifulSoup(html_content, 'html.parser')
        #print(soup)
        articles = soup.findAll('article', attrs={'role':'article'})
        
        # get first article
        FIRST_ARTICLE = articles[0]

        article_date = FIRST_ARTICLE.find('div', attrs={'class':'nir-widget--field nir-widget--news--date-time'})
        article_desc = FIRST_ARTICLE.find('div', attrs={'class':'nir-widget--field nir-widget--news--headline'})
        
        v_article_date = article_date.text.lstrip().rstrip()

        #if the process find any article with the today date
        istoday, v_art_date = validateday(v_article_date)

        
        if (istoday == True):
            v_ticker = os.path.basename(__file__).replace(".py", "")
            v_url = article_desc.a.get('href')
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
