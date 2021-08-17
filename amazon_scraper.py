import requests
from bs4 import BeautifulSoup
import csv
import os
HEADER = {
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
    'cookie': 'session-id=257-8877454-3506601; i18n-prefs=GBP; ubid-acbuk=258-6364388-6293226; lc-acbuk=en_GB; s_cc=true; s_sq=[[B]]; s_ppv=100; s_nr=1628823321252-Repeat; s_vnum=2060705960986&vn=5; s_dslv=1628823321256; session-token=OGLdUE8LbzLdbjDTPLJlWwZiw02+tbhnDtdfKrjsxD453pnE0YpFbTS8Vd+87axPNzSmdmxxJDZd6xlLCudF8m2/Iy7mVGobRvYilzEpMA6U8zFZo+wycrP16moFogLOaF4DezlTQeetBGAopG/w5/rOlMM1Bwe60wtAcp41Jdkt2ZhDo8v+Hv27st5xY7h2; csm-hit=tb:s-DS2K6T89DSPW6HN9DZV6|1629168650814&t:1629168652117&adb:adblk_yes; session-id-time=2082758401l'
}

def get_links():
    page = 1
    data = list()
    while page <= 7:
        source = requests.get(f'https://www.amazon.co.uk/s?k=Toys%2C+Children+%26+Baby&page={page}', headers=HEADER)
        soup = BeautifulSoup(source.text, 'lxml')

        PRODUCTS = soup.find_all(
            'div', {'data-component-type': 's-search-result'})

        for product in PRODUCTS:
            link = product.find('a', class_='a-link-normal a-text-normal')['href']
            prime = ''
            try:
                prime = product.find(
                    'i', {'class': 'a-icon a-icon-prime a-icon-medium'})['aria-label']
            except:
                prime = 'No'
            else:
                if prime == 'Amazon Prime':
                    prime = 'Prime'

            data.append(('https://www.amazon.co.uk' + link, prime))

        page = page + 1

    return data


def proceed_link(link, prime):
    source = requests.get(link, headers=HEADER)
    soup = BeautifulSoup(source.text, 'lxml')
    # Link
    LINK = ''
    try:
        LINK = soup.find('link',{'rel':'canonical'})['href']
    except:
        LINK = 'Not Found'


    splited_url = LINK.split('/')[4:6]

    # Page Url
    try:
        PAGE_URL = 'https://www.amazon.co.uk' + '/' + splited_url[0] + '/' + splited_url[1]
    except:
        PAGE_URL = 'None'


    # ASIN
    try:
        ASIN = splited_url[1]
    except:
        ASIN = 'None'

    # Title
    
    TITLE = ''
    try:
        layers = soup.find_all('div', {'class': 'a-section a-spacing-none'})
        for layer in layers:
            if layer.find('h1', {'id': 'title'}) != None:
                TITLE = layer.find('h1', {'id': 'title'}).find('span', {'id': 'productTitle'}).text.strip()
    except:
        TITLE = 'None'

    # Brand
    BRAND = 'NEW'

    # Condition
    CONDITION = ''
    try:
        CONDITION = soup.find(
            'div', {'id': 'bylineInfo_feature_div'}).div.a.text.strip('Brand:').strip()
    except:
        CONDITION = 'None'

    # Category
    CATEGORY = ''
    try:
        rows = soup.find('ul', {'class': 'a-unordered-list a-horizontal a-size-small'}).find_all('li')
        for row in rows:
            try:
                CATEGORY = CATEGORY + row.find('span').a.text.strip() + '/'
            except:
                pass
        CATEGORY = CATEGORY.rstrip('/')
    except:
        try:
            CATEGORY = soup.find('div', {'id': 'nav-subnav'})['data-category']
        except:
            CATEGORY = 'Not Given'


    # Availability
    AVAILABILITY = ''
    A = ''
    try:
        A = soup.find('div', {'id': ['outOfStock','unqualifiedBuyBox','partialStateBuybox']})['id']
    except:
        A = 'None'
    else:
        if (A == 'outOfStock') or (A == 'unqualifiedBuyBox'):
            A = 'Currently unavailable.'
        elif A == 'partialStateBuybox':
            A = 'To buy, select Size Name'

    B = ''
    try:
        B = soup.find('div', {'id': 'availability'}).span.text.strip()
    except:
        B = 'None'
    else:
        AVAILABILITY = B

    if A == 'Currently unavailable.':
        AVAILABILITY = A
    elif A == 'To buy, select Size Name':
        AVAILABILITY = A


    # DELIVERY DATE:
    DELIVERY_DATE = ''
    if AVAILABILITY == 'Currently unavailable.':
        DELIVERY_DATE = 'None'
    else:
        try:
            DELIVERY_DATE = soup.find('div', {'id': ['deliveryBlockContainer','usedDeliveryBlockContainer']}).find('div', {'id': 'mir-layout-DELIVERY_BLOCK'}).text.strip()
        except:
            DELIVERY_DATE = 'None'
        else:
            if DELIVERY_DATE == '' or DELIVERY_DATE == None:
                DELIVERY_DATE = 'None'
            else:
                collect = ''
                DELIVERY_DATE = DELIVERY_DATE.split()
                for delivery in DELIVERY_DATE:
                    collect = collect + delivery + ' '
                DELIVERY_DATE = collect.strip()

    # Product Description
    PRODUCT_DESCP = ''
    PD_1 = ''
    try:
        PD_1 = soup.find('div',{'id':'productDescription'}).text.strip()
    except:
        PD_1 = 'Not Given'
    else:
        if PD_1 == '':
            PD_1 = 'Not Given'

    PD_2 = ''
    try:
        PD_2 = soup.find('div',{'class':'a-section a-spacing-small a-padding-small'}).text.strip()
    except:
        PD_2 = 'Not Given'
    else:
        if PD_2 == '':
            PD_2 == 'Not Given'
        
    if PD_1 == 'Not Given' and PD_2 == 'Not GIven':
        PRODUCT_DESCP = 'Not Given'
    elif PD_1 == 'Not Given' and PD_2 != 'Not Given':
        PRODUCT_DESCP = PD_2
    elif PD_1 != 'Not Given' and PD_2 == 'Not Given':
        PRODUCT_DESCP = PD_1
    else:
        PRODUCT_DESCP = 'Not Given'

    # Product Summary
    PRODUCT_SUMMARY = ''
    PS_1 = ''
    try:
        rows = soup.find('div',{'id':'featurebullets_feature_div'}).find_all('span')
        for row in rows:
            PS_1 = PS_1 + row.text.strip() + ' '
    except:
        PS_1 = 'Not Given'
    else:
        if PS_1 == '' or PS_1 == ' ':
            PS_1 = 'Not Given'

    PS_2 = ''
    try:
        rows = soup.find_all('noscript')
        for row in rows:
            if row.find('p') != None:
                PS_2 = PS_2 + row.find('p').text.strip()
    except:
        PS_2 = 'Not Given'
    else:
        if PS_2 == '' or PS_2 == ' ':
            PS_2 = 'Not Given'


    if PS_1 == 'Not Given' and PS_2 == 'Not Given':
        PRODUCT_SUMMARY = 'Not Given'
    elif PS_1 == 'Not Given' and PS_2 != 'Not Given':
        PRODUCT_SUMMARY = PS_2
    elif PS_1 != 'Not Given' and PS_2 == 'Not Given':
        PRODUCT_SUMMARY = PS_1



    # Product Information
    PRODUCT_INFORMATION = ''
    PI_1= ''
    try:
        bucket = list()
        rows = soup.find('div',{'id':'prodDetails'}).find('table',{'id':'productDetails_techSpec_section_1'}).find_all('tr')
        for row in rows:
            bucket.append(tuple(row.text.strip().split('\n\n\n\u200e')))
        PI_1 = bucket
    except:
        PI_1 = 'Not Given'


    PI_2 = ''
    try:
        bucket = ''
        rows = soup.find('div',{'id':'detailBulletsWrapper_feature_div'}).find('div',{'id':'detailBullets_feature_div'}).ul.find_all('li')
        for row in rows:
            var = row.text.strip().split()
            var.remove('\u200e')
            var.remove('\u200f')
            temp = ''
            for c in var:
                temp = temp + c + ' '
            bucket = bucket + temp + ' , '
            PI_2 = bucket
    except:
        PI_2 = 'Not Given'

    if (PI_1 == 'Not Given') and (PI_2 == 'Not Given'):
        PRODUCT_INFORMATION = 'Not Given'
    elif (PI_1 == 'Not Given') and (PI_2 != 'Not Given'):
        PRODUCT_INFORMATION = PI_2
    elif (PI_1 != 'Not Given') and (PI_2 == 'Not Given'):
        PRODUCT_INFORMATION = PI_1
    else:
        PRODUCT_INFORMATION = 'Not Given'

    # SELLER INFO
    SELLER_INFO = ''
    SI_1 = ''
    try:
        rows = soup.find('div',{'id':'productDetails_db_sections'}).find_all('tr')
        for row in rows:
            if 'Best Sellers Rank' in row.text.strip():
                SI_1 = ' '.join(row.text.strip().lstrip('Best Sellers Rank').split())
                break
    except:
        SI_1 = 'Not Given'

    SI_2 = ''
    try:
        rows = soup.find('div',{'id':'detailBulletsWrapper_feature_div'}).find_all('ul')
        for row in rows:
            if 'Best Sellers Rank' in row.text.strip():
                SI_2 = ' '.join(row.text.strip().lstrip('Best Sellers Rank:').split())
                break
    except:
        SI_2 = 'Not Given'

    if SI_1 == 'Not Given' and SI_2 == 'Not Given':
        SELLER_INFO = 'Not Given'
    elif (SI_1 == 'Not Given') and (SI_2 != 'Not Given'):
        SELLER_INFO = SI_2
    elif (SI_1 != 'Not Given') and (SI_2 == 'Not Given'):
        SELLER_INFO = SI_1
    else:
        SELLER_INFO = 'Not Given'

    # Image
    IMAGES = ''
    IM_1 = list()
    try:
        rows = soup.find('div',{'id':'altImages'}).ul.find_all('li',{'class':'a-spacing-small item'})
        for row in rows:
            IM_1.append(row.find('img')['src'])
    except:
        IM_1 = 'Not Found'

    IM_2 = list()
    try:
        rows = soup.find('div',{'id':'imageBlockThumbs'}).find_all('img')
        for row in rows:
            IM_2.append(row['src'])
    except:
        IM_2 = 'Not Found'

    if IM_1 == 'Not Found':
        IMAGES = IM_2
    elif IM_2 == 'Not Found':
        IMAGES = IM_1
    elif (IM_1 == 'Not Found') and (IM_2 == 'Not Found'):
        IMAGES = 'Not Found'
    else:
        IMAGES = 'Not Found'
    
    # Seperate Images
    img1,img2,img3,img4,img5,img6,img7 = '','','','','','',''
    #img1
    try:
        img1 = IMAGES[0]
        if img1 == '':
            img1 = 'Not Found'
    except:
        img1 = 'Not Found'
    #img2
    try:
        img2 = IMAGES[1]
        if img2 == '':
            img2 = 'Not Found'
    except:
        img2 = 'Not Found'
    #img3
    try:
        img3 = IMAGES[2]
        if img3 == '':
            img3 = 'Not Found'
    except:
        img3 = 'Not Found'
    #img4
    try:
        img4 = IMAGES[3]
        if img4 == '':
            img4 = 'Not Found'
    except:
        img4 = 'Not Found'
    #img5
    try:
        img5 = IMAGES[4]
        if img5 == '':
            img5 = 'Not Found'
    except:
        img5 = 'Not Found'
    #img6
    try:
        img6 = IMAGES[5]
        if img6 == '':
            img6 = 'Not Found'
    except:
        img6 = 'Not Found'
    #img7
    try:
        img7 = IMAGES[6]
        if img7 == '':
            img7 = 'Not Found'
    except:
        img7 = 'Not Found'
    

    # RRP
    RRP = ''
    PRICE = ''
    try:
        RRP = soup.find('div',{'id':'price', 'class':'a-section a-spacing-small'})
        RRP = RRP.text.strip().split()
    except:
        RRP = 'Not Given'
    else:
        PRICE = RRP
        if ('RRP:' in RRP) or ('RRP' in RRP):
            RRP = RRP[RRP.index('RRP:')+1]
        else:
            RRP = 'Not Given'

    # PRICE
    try:
        if 'Price:' in PRICE:
            PRICE = PRICE[PRICE.index('Price:')+1]
        else:
            PRICE = 'Not Given'
    except:
        PRICE = 'Not Given'


    return {
        'PAGE_URL': PAGE_URL,
        'ASIN': ASIN,
        'TITLE': TITLE,
        'BRAND': BRAND,
        'CONDITION': CONDITION,
        'CATEGORY': CATEGORY,
        'PRIME': prime,
        'AVAILABILITY': AVAILABILITY,
        'DELIVERY_DATE': DELIVERY_DATE,
        'PRODUCT_DESCP': PRODUCT_DESCP,
        'PRODUCT_SUMMARY': PRODUCT_SUMMARY,
        'PRODUCT_INFORMATION': PRODUCT_INFORMATION,
        'SELLER_INFO':SELLER_INFO,
        'Image1':img1,
        'Image2':img2,
        'Image3':img3,
        'Image4':img4,
        'Image5':img5,
        'Image6':img6,
        'Image7':img7,
        'RRP': RRP,
        'PRICE':PRICE
    }

def store_data(data):
    fieldnames = ['PAGE_URL', 'ASIN', 'TITLE', 'BRAND', 'CONDITION', 'CATEGORY', 'PRIME', 'AVAILABILITY',
                  'DELIVERY_DATE','PRODUCT_DESCP', 'PRODUCT_SUMMARY', 'PRODUCT_INFORMATION', 'SELLER_INFO',
                  'Image1','Image2','Image3','Image4','Image5','Image6','Image7', 'RRP', 'PRICE']
    with open('/home/ahsan/Desktop/amazon.csv','w') as f:
        csv_writer = csv.writer(f, fieldnames=fieldnames)
        csv_writer.writerow([data.get('PAGE_URL'),data.get('ASIN'),data.get('TITLE'),data.get('BRAND'),data.get('CONDITION'),data.get('CATEGORY'),
        data.get('PRIME'),data.get('AVAILABILITY'),data.get('DELIVERY_DATE'),data.get('PRODUCT_DESCP'),data.get('PRODUCT_SUMMARY'),
        data.get('PRODUCT_INFORMATION'), data.get('SELLER_INFO'), data.get('Image1'), data.get('Image2'), data.get('Image3'), data.get('Image4'),
        data.get('Image5'), data.get('Image6'), data.get('Image7'), data.get('RRP'), data.get('PRICE')])



def display_data(data):
    print('PAGE_URL: ', data.get('PAGE_URL'))
    print('ASIN: ', data.get('ASIN'))
    print('TITLE: ', data.get('TITLE'))
    print('BRAND: ', data.get('BRAND'))
    print('CONDITION: ', data.get('CONDITION'))
    print('CATEGORY: ', data.get('CATEGORY'))
    print('PRIME: ', data.get('PRIME'))
    print('AVAILABILITY: ', data.get('AVAILABILITY'))
    print('DELIVERY_DATE: ', data.get('DELIVERY_DATE'))
    print('PRODUCT_DESCP: ', data.get('PRODUCT_DESCP'))
    print('PRODUCT_SUMMARY: ', data.get('PRODUCT_SUMMARY'))
    print('PRODUCT_INFORMATION: ', data.get('PRODUCT_INFORMATION'))
    print('SELLER_INFO: ', data.get('SELLER_INFO'))
    print('IMAGE1: ', data.get('Image1'))
    print('IMAGE2: ', data.get('Image2'))
    print('IMAGE3: ', data.get('Image3'))
    print('IMAGE4: ', data.get('Image4'))
    print('IMAGE5: ', data.get('Image5'))
    print('IMAGE6: ', data.get('Image6'))
    print('IMAGE7: ', data.get('Image7'))
    print('RRP: ', data.get('RRP'))
    print('PRICE: ', data.get('PRICE'))





def main():
    data = get_links()
    result = dict()
    for link, prime in data:
        result = proceed_link(link, prime)
        display_data(result)
        store_data(result)

if __name__ == "__main__":
    main()
