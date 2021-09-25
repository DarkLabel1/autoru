import requests
import json
from bs4 import BeautifulSoup as bs


class auto:

    def __init__(self):
        self.headers = [
            {
                'accept': '*/*', 
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36'
            },
            {
                'accept': '*/*',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.131 Safari/537.36',
                'cookie': 'suid=6f7dd7867261146e492a8e4e7509ddab.fb215959e7940d0354eaa2e31eca848f; _ym_uid=1615216201866918173; _ga=GA1.2.1155361267.1615934277; autoruuid=g60463e452st3aldlqlm0cgvunfk1hg8.df0e1e355ab68fb1f9bf77bd824981d0; gids=11; counter_ga_all7=1; yandexuid=9476882891553578318; my=YycCAAEA; autoru_sid=65808656%7C1623710403014.7776000.oEYYR-EVfvLMdX0MfmxkNA.jYi2ToVQ009r6f7h8OqMoOhD2_n0593jNLQ6-VE5z7k; _csrf_token=b61d62577b7d89b4434dd4bc67218403fc7cbbcc96166717; from=google-search; X-Vertis-DC=vla; yuidlt=1; salon_phone_utms=utm_medium%3Dcpc%26utm_source%3Dgoogle_adwords%26utm_campaign%3Did-_place-gsearch_geo-rus-r225_type-history-vin-knk-avtoru%26utm_content%3Didgr-_cat-history-vin-avtoru_obshie-z--proverka-vin_geo-rus-r225; _gid=GA1.2.1394062166.1628430047; _gac_UA-11391377-1=1.1628430047.CjwKCAjwgb6IBhAREiwAgMYKRtRepexXa3SvwxZJuMrrhx3Vj-gT72F_W89dPbWuGeFMVyaP0RQjpBoCdeAQAvD_BwE; hide-proauto-pimple=1; notification_offer_stat_fetched=true; gdpr=0; from_lifetime=1628430192537; _ym_d=1628430192; from=google-search; from_lifetime=1628430566018; Secure,X-Vertis-DC=vla; _ym_d=1628430566; _ym_uid=1615216201866918173; from=direct; from_lifetime=1629043570487; Secure,X-Vertis-DC=vla; _ym_d=1629043570; _ym_uid=1615216201866918173',
                'x-csrf-token': 'b61d62577b7d89b4434dd4bc67218403fc7cbbcc96166717',
                'content-type': 'text/plain;charset=UTF-8'
            }
        ]
        self.urls = {
            'hidemy': 'https://hidemy.name/ru/proxy-list/', 
            'myip': 'https://api.myip.com/', 
            'listingAuto': 'https://auto.ru/-/ajax/desktop/listing/'
        }
        self.params = [
            {'country': 'AFALADARAMAUATBDBYBEBZBOBABRBGBIKHCMCACLCNCOCGCDCRCIHRCYCZDOECEGFIFRGEDEGHGRGTGNHNHKHUINIDIRIQIEITJPKZKEKRKGLVLBLSLTMKMGMWMYMTMUMXMDMNMZMMNPNLNZNINGNOPKPSPAPYPEPHPLPTRORURWSARSSCSGSKSIZAESSESYTWTJTZTHTNTRUGUAAEGBUSVEVNVGZW','maxtime': 150,'type': 45,'anon': 34},
            {"catalog_filter":[{"mark":"MERCEDES"},{"mark":"BMW"}],"page": 1,"section":"all","category":"cars","output_type":"list","geo_id":[225]}
        ]
        self.offers = []
        self.session_browser = requests.Session()
        self.session_browser_auto = requests.Session()
        self.session_browser.headers = self.headers[0]
        self.session_browser_auto.headers = self.headers[1]

    def proxy(self):
        r = self.session_browser.get(self.urls['hidemy'], params=self.params[0])
        s = bs(r.content, 'html.parser')
        table = s.find('table').find('tbody')
        for tr in table.find_all('tr'):
            ip = tr.find_all('td')[0].text
            port = tr.find_all('td')[1].text
            protocol = tr.find_all('td')[4].text.lower()

            proxyDict = {
                'http': f'{protocol}://' + str(ip) + ':' + str(port),
                'https': f'{protocol}://' + str(ip) + ':' + str(port)
            }

            try:
                myip = self.session_browser.get(self.urls['myip'], proxies=proxyDict).json()['ip']
                if (myip == ip):
                    return proxyDict
            except:
                pass
    
    def parser(self):
        i = 1
        p = {"catalog_filter":[{"mark":"MERCEDES"},{"mark":"BMW"}],"page": i,"section":"all","category":"cars","output_type":"list","geo_id":[225]}
        r = self.session_browser_auto.post(self.urls['listingAuto'], data=self.params[1]).json()
        offers = r['offers']
        r = self.session_browser_auto.post(self.urls['listingAuto'], data=p).json()
        count_page = r['pagination']['total_page_count']
        while i <= count_page:
            r = self.session_browser_auto.post(self.urls['listingAuto'], data=p).json()
            self.offers.append(r['offers'])
            i+=1
        with open('im.json', 'w') as f:
            f.write(json.dumps(offers)) 
        return self.offers


if __name__ == '__main__':
    obj = auto()
    obj.parser()
    print('Выполненно')