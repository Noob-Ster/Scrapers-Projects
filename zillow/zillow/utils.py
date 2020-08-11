from http.cookies import SimpleCookie
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse,ParseResult
import json


URL = 'https://www.zillow.com/search/GetSearchPageState.htm?searchQueryState=%7B%22pagination%22%3A%7B%7D%2C%22usersSearchTerm%22%3A%22Miami%2C%20FL%22%2C%22mapBounds%22%3A%7B%22west%22%3A-85.35202814585946%2C%22east%22%3A-78.58445002085946%2C%22south%22%3A22.820246322488956%2C%22north%22%3A27.511689467148578%7D%2C%22regionSelection%22%3A%5B%7B%22regionId%22%3A12700%2C%22regionType%22%3A6%7D%5D%2C%22mapZoom%22%3A7%2C%22filterState%22%3A%7B%22pmf%22%3A%7B%22value%22%3Afalse%7D%2C%22fore%22%3A%7B%22value%22%3Afalse%7D%2C%22auc%22%3A%7B%22value%22%3Afalse%7D%2C%22nc%22%3A%7B%22value%22%3Afalse%7D%2C%22fr%22%3A%7B%22value%22%3Atrue%7D%2C%22fsbo%22%3A%7B%22value%22%3Afalse%7D%2C%22cmsn%22%3A%7B%22value%22%3Afalse%7D%2C%22pf%22%3A%7B%22value%22%3Afalse%7D%2C%22fsba%22%3A%7B%22value%22%3Afalse%7D%7D%2C%22isListVisible%22%3Atrue%2C%22isMapVisible%22%3Afalse%7D&includeMap=false&includeList=true'


def cookies_parser():
    raw_cookies = 'zguid=23|%24a08860b1-beb6-4bb8-a684-71c7fd221063; zgsession=1|3365f18b-3179-41f7-8250-e19a7776bc0f; _ga=GA1.2.1232624877.1596578712; _gid=GA1.2.1846558012.1596578712; zjs_user_id=null; zjs_anonymous_id=%22a08860b1-beb6-4bb8-a684-71c7fd221063%22; _gcl_au=1.1.727302175.1596578713; KruxPixel=true; DoubleClickSession=true; _pxvid=b3dbcd77-d69e-11ea-9c92-0242ac120003; _fbp=fb.1.1596578714782.40736752; _pin_unauth=dWlkPU9UTmpOelExWldRdE9XVTRZUzAwWkRoaExXRTROREV0TlRVMFpEWmpaRFl3T0dRMQ; KruxAddition=true; g_state={"i_p":1596586377663,"i_l":1}; _uetsid=01f13cbf4feb91355ca40d83d02e26b1; _uetvid=1f67bf2e2c771d9ca09589d945fa8398; ki_r=; ki_s=; _px3=187a561cae12e693337016c3c94b085310fff6016b3338090068086e46ab2dd2:FxjS5YAsKwQiY9NAt8frRRYn6gAqSlww6Ors76A8oMRLw+eOLJQcJQFSwNO9f7GyU9O69P0LP2v1Np0g+iA4QA==:1000:fWAfVberbAxwwwSWWsMVMdv9bnAv5wGbWqVBTiGW9O2TwrgsNngTE8gf2P1yA6Cti2jzR1Xi/GDRfpA7tbDuDIg2UVDYSi/FcgnNE2lbBi6h2M9G2jZUKVPiqQtHsPfAH7azj5MQOsIkvF5Ma2rha8gy11Ra19G0Vd+K1WfDmV8=; _gat=1; AWSALB=G/OK8vZ0/qtAnuQws67AI4OJFX/UR2XP/VxjV8er1zsk1sSnb6mq6tldKxFJaek2ZeV5ZptmjPy2qM8ifJeI8mkv3Yovl7dl48khZp2Xc23n5DkrDa8bwnCh/SPX; AWSALBCORS=G/OK8vZ0/qtAnuQws67AI4OJFX/UR2XP/VxjV8er1zsk1sSnb6mq6tldKxFJaek2ZeV5ZptmjPy2qM8ifJeI8mkv3Yovl7dl48khZp2Xc23n5DkrDa8bwnCh/SPX; JSESSIONID=6230D8F43C386F24599F483D5FF0FB0F; search=6|1599173492871%7Crect%3D25.855607%252C-80.142305%252C25.689672%252C-80.352373%26rid%3D12700%26disp%3Dmap%26mdm%3Dauto%26p%3D1%26sort%3Ddays%26z%3D1%26fs%3D0%26fr%3D1%26mmm%3D0%26rs%3D0%26ah%3D0%26singlestory%3D0%26housing-connector%3D0%26abo%3D0%26garage%3D0%26pool%3D0%26ac%3D0%26waterfront%3D0%26finished%3D0%26unfinished%3D0%26cityview%3D0%26mountainview%3D0%26parkview%3D0%26waterview%3D0%26hoadata%3D1%26zillow-owned%3D0%263dhome%3D0%09%0912700%09%09%09%09%09%09; ki_t=1596579293782%3B1596579293782%3B1596581437520%3B1%3B7'
    simpleCookie = SimpleCookie()
    simpleCookie.load(raw_cookies)
    cookies = {}
    for key, morsel in simpleCookie.items():
        cookies[key] = morsel.value
    return cookies


def parse_new_url(url, pageNumber):
    parsed_url = urlparse(url=url)
    queryString = parse_qs(parsed_url.query)
    search_query_state = queryString.get('searchQueryState')[0]
    queryState = json.loads(search_query_state)
    queryState['pagination'] = {'currentPage':pageNumber}
    search_query_state = queryState
    queryString['searchQueryState'][0] = search_query_state
    new_queryString = urlencode(queryString,doseq=1)
    new_url = f'www.zillow.com/search/GetSearchPageState.htm?{new_queryString}'
    print(new_url)
    

    


parse_new_url(url=URL, pageNumber=3)
