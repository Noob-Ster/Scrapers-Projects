from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import time
import mysql.connector


def chromeOptions():
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    return chrome_options

def chromeDriver(chrome_options):
    driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',options=chrome_options)
    page = 1
    while page < 86:
        driver.get(f'https://www.firmy.cz/?q=prodej+kol&page={page}')
        time.sleep(15)
        parser(driver=driver,page=page)
        page += 1
    
    driver.close()

def parser(driver,page):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    rows = soup.find_all('div',{'data-dot':'premise'})
    count = 0
    for row in rows:
        try:
            title = row.find('span',{'class':'title'}).text
        except Exception:
            title = None
        finally:
            print(f'title : {title}')

        try:
            phone = row.find('span',{'class':'premiseListPhone'}).text
        except Exception:
            phone = None
        finally:
            print(f'phone : {phone}')

        try:        
            email = row.find('div', {'class':'action actionUrl'}).find('span',{'class':'actionTitle-desktop'}).text
        except Exception:
            email = None
        finally:
            print(f'email : {email}')

        try:
            address = row.find_all('span',{'class':'addrPart'})
        except Exception:
            address = None
        finally:
            print(f'address : {address[0].text} {address[1].text}\n')
        
        count = count + 1

        store_in_db(title=title, phone=phone, email=email, address=f'{address[0].text}{address[1].text}')    # Storing in MYSQL DATABASE

    print(f"---------------------------------------------PAGE-{page}--Completed------Total Hotels ({count})----------------------------------")
        

def store_in_db(title,phone,email,address):
    mydb = mysql.connector.connect(
        host='localhost',
        user='root',
        passwd='ahsan',
        database='FirmzyWeb'
    )
    mycursor = mydb.cursor(buffered=True)
                                                        # Create Table
    mycursor.execute('''
        CREATE TABLE IF NOT EXISTS Hotel
        (   
            id INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
            title VARCHAR(100),
            phone VARCHAR(50),
            email VARCHAR(50),
            address VARCHAR(200)
        );
    ''')

    
    sql = 'INSERT INTO Hotel (title,phone,email,address) VALUES (%s,%s,%s,%s)'
    val = (title,phone,email,address)
    mycursor.execute(sql,val)
    mydb.commit()





def main():
    chrome_options = chromeOptions()
    chromeDriver(chrome_options=chrome_options)
    #store_in_db()


if __name__ == "__main__":
    main()
