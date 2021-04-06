import requests
from lxml import html
from bs4 import BeautifulSoup
import os

from datetime import date, datetime

from ValidationTools import validateday
from Database_Connections import InsertData, Insert_Logging



def validateday(day):
    today = date.today()

    # dd/mm/YY
    #d1 = today.strftime("%d/%m/%Y")
    #print("d1 =", d1)

    # Textual month, day and year	
    d2 = today.strftime("%B %d, %Y")
    print("d2 =", d2)

    # mm/dd/y
    d3 = today.strftime("%m/%d/%y")
    print("d3 =", d3)

    # Month abbreviation, day and year	
    d4 = today.strftime("%b-%d-%Y")
    print("d4 =", d4)

    # mm dd yyyyy
    d5 = today.strftime("%d %b %Y")
    print("d5 =", d5)

    # mm dd yyyyy
    d6 = today.strftime("%b %d %Y")
    print("d6 =", d6)

    if(day == d2 or day == d3 or day == d4 or day == d5 or day == d6):
        return True

    return False

def main(id_control):
    print("Entra copy")
    #database = r"C:\sqlite\db\pythonsqlite.db"
    #/Users/andregama/Documents/WebScraping/TESTE

    try:
        url = 'https://investor.sppirx.com/index.php/press-releases' 

        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
        result = requests.get(url, headers=headers)
        #print(result.content.decode())
        html_content = result.content.decode()
        soup = BeautifulSoup(html_content, 'html.parser')
        #print(soup)

        table = soup.find('table', attrs={'class':'nirtable collapse-table news-table'})
        #print(table)
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')

        columns = rows[0].find_all('td')
        v_article_date = columns[0].text.lstrip().rstrip()

        #if the process find any article with the today date
        if(validateday(v_article_date)):
            article_desc = columns[1].find('div', attrs={'class':'nir-widget--field nir-widget--news--headline'})
            print("URL: " + article_desc.a.get('href'))
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
