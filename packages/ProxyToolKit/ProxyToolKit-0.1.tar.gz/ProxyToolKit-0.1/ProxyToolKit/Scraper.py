import requests as rqs
from bs4 import BeautifulSoup
from .utlis.agents import user_agents
from .Exceptions import *
import random,os
from datetime import datetime as dt
from concurrent.futures import ThreadPoolExecutor
from .Exceptions import *
from PyQt5.QtWidgets import QApplication, QMessageBox

class Scraper():
    def __init__(
        self,
        proxy_type='',
        is_web:bool=False
        ):
        # global data
        self.proxy_type = proxy_type
        # self.proxy_data = ''
        self.session = rqs.session()
        self.session.headers.update({("User-Agent", random.choice(user_agents))})
        self.all=['http','https','socks4','socks5']
        self.is_web = is_web
        self.ct =dt.now().isoformat()
        if not self.is_web:
            self.app = QApplication([])

    def main(self,proxy_type:str):
        proxy_data =''
        url = f"https://api.proxyscrape.com/v2/?request=getproxies&protocol={proxy_type}&timeout=all&country=all"
        r = self.session.get(url)
        proxies = r.text  
        # print(proxies)
        proxy_data+=proxies
        response = self.session.get(f"https://api.proxyscrape.com/?request=getproxies&proxytype={proxy_type}&timeout=all&country=all")
        p = response.text
        
        proxy_data+=p
        html = self.session.get(f"https://www.proxy-list.download/api/v1/get?type={proxy_type}&anon=elite").text
        for line in html.split("\n"):
            if len(line) > 0:
                proxy_data+=line
                
        if proxy_type =='http':
            page = self.session.get("http://us-proxy.org")
            soup = BeautifulSoup(page.text, "html.parser")
            proxies = set()
            table = soup.find("table", attrs={"class": "table table-striped table-bordered"})
            for row in table.findAll("tr"):
                count = 0
                proxy = ""
                for cell in row.findAll("td"):
                    if count == 1:
                        proxy += ":" + cell.text.replace("&nbsp;", "")
                        proxies.add(proxy)
                        break
                    proxy += cell.text.replace("&nbsp;", "")
                    count += 1
                    
            for line in proxies:
                proxy_data += f'{line}\r\n'
        
        
        return proxy_data
    
    def save_data(self,data):
        path = os.getcwd()
        fp= os.path.join(path,'Proxys')
        if not os.path.exists(fp):
            os.makedirs(fp)
        with open(f'{fp}/Scraped_proxy_{self.ct}.txt','w') as f:
            f.write(data)
        if not self.is_web:
            QMessageBox.information(None,'Message',f'Scraping "{self.proxy_type}" Proxy Saved SuccesFully, Path : {fp}')
            pass

    def scrape(self):
        if self.proxy_type:
            
            if self.proxy_type =='all':               
                if not self.is_web:
                    QMessageBox.information(None,'Message',f'Start Scraping "{self.proxy_type}" Proxy')
                    pass
                with ThreadPoolExecutor(max_workers=4) as exc:
                    arg1 ='http'
                    arg2 ='https'
                    arg3 = 'socks4'
                    arg4 = 'socks5'
                    http = exc.submit(self.main,arg1)
                    https = exc.submit(self.main,arg2)
                    socks4 = exc.submit(self.main,arg3)
                    socks5 = exc.submit(self.main,arg4)

                    r = http.result()
                    r1 = https.result()
                    r2 = socks4.result()
                    r3 = socks5.result()
                    
                    res = r+r1+r2+r3
                    
                    # return r+r1+r2+r3
            else:
                if not self.is_web:
                    QMessageBox.information(None,'Message',f'Start Scraping "{self.proxy_type}" Proxy')
                    pass
                with ThreadPoolExecutor(max_workers=1) as exc:
                    arg =self.proxy_type
                    proxy = exc.submit(self.main,arg)
                    res  = proxy.result()
                    # return res
                
        else:
            if not self.is_web:
                QMessageBox.information(None,'Message',f'Start Checking Proxy Using "HTTPS" protocols, Due to no mension of protocol or inavlid Protocol ')
                pass 
            with ThreadPoolExecutor(max_workers=4) as exc:
                arg = 'https'
                proxy = exc.submit(self.main,arg)
                res  = proxy.result()
                
        if self.is_web:
            return res
        else:
            self.save_data(res)