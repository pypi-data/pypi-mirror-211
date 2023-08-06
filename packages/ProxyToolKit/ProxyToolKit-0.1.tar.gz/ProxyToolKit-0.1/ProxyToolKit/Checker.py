from PyQt5.QtWidgets import QApplication, QMessageBox
import random,requests as rqs,os,threading
from .utlis.agents import user_agents
from .Exceptions import *
import queue as Queue
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime as dt



class checker():
    url = 'https://api.ipify.org/'
    def __init__(
        self,
        proxys,
        proxy_type='',
        is_path:bool=False,
        is_web:bool=False,
        ):
        
        self.session = rqs.session()
        self.session.headers.update({("User-Agent", random.choice(user_agents))})
        self.proxy_list = proxys
        self.proxy_type = proxy_type.lower()
        self.proxy_list_type = None
        self.all = ['http','https','socks4','socks5']
        self.is_web = is_web
        if not self.is_web:
            self.app = QApplication([])
        self.ct =dt.now().isoformat()
        
        if proxys and is_path:
            
            if os.path.exists(proxys):
                with open(proxys,'r') as f:
                    self.proxy_list = f.readlines()
                    self.proxy_list_type = list
                    # print(self.proxy_list)
            else:
                if '\\ ' or '/' not  in proxys:
                    raise PathError()
            
        else:
            if proxys:
                self.proxy_list_type = self.det_type(proxys)
                if self.proxy_list_type == str:
                    self.proxy_list = self.convert_text_to_list(self.proxy_list)
                elif self.proxy_list_type ==tuple:
                    self.proxy_list =proxys
                else: 
                    raise InavalidProxyData()

            
    
    def convert_text_to_list(self,string:str):
        proxys = string.replace('\r','')
        proxys = proxys.split('\n')
        for proxy in proxys:
            if len(proxy) <5 :
                proxys.remove(proxy)
        return proxys       
    
    
    def det_type(self,proxy):  
        return type(proxy)
    
    def create_connector(self,proxy_type):
        
        if proxy_type == 'http' or 'https':
            pt  = {
                'http': 'http://{}',
                'https': 'http://{}'}
        
        elif proxy_type == 'socks4':
            pt = {
                'http' : 'socks4://{}' ,
                'https' : 'socks4://{}'}
        elif proxy_type == 'socks5':
            pt = {
                'http' : 'socks5://{}' ,
                'https' : 'socks5://{}' }
            
        self.proxy_type_connector = pt
        
    def save_data(self,data,mode='w'):
        path = os.getcwd()
        fp= os.path.join(path,'Proxys')
        if not os.path.exists(fp):
            os.makedirs(fp)
        # print(f'{fp}/Checked_proxys_{self.ct}.txt')
        with open(f'{fp}/Checked_proxys_{self.ct}.txt',mode) as f:
            f.write(data+'\n')
            
    def check(self):

        if self.proxy_list_type == list and len(self.proxy_list) > 0:
            path = os.getcwd()
            fp= os.path.join(path,'Proxys')
            
            # print('hello')
            if self.proxy_type and self.proxy_type in self.all:
                # print('hey')
                if not self.is_web:
                    QMessageBox.information(None,'Message',f'Start Checking Proxy Using "{self.proxy_type}" protocol, Note: Checked Proxys Auto save to the path : {fp}')
                    pass
                with  ThreadPoolExecutor(max_workers=1) as executer:
                    proxy_type = self.proxy_type
                    self.create_connector(proxy_type)
                    arg  = self.proxy_list
                    proxy_res = executer.submit(self.threader,arg)
                    res = proxy_res.result()
                    if self.is_web:
                        return res
                    
            else:
                if not self.is_web:
                    QMessageBox.information(None,'Message',f'Start Checking Proxy Using "HTTPS" protocols, Due to no mension of protocol or inavlid Protocol,, Note: Checked Proxys Auto save to the path : {fp}') 
                    pass
                
                
                proxy_type ='https'
                with  ThreadPoolExecutor(max_workers=1) as executer:
                    print('trying to create typer')
                    self.create_connector(proxy_type)
                    print(self.proxy_type_connector)
                    arg  = self.proxy_list
                    proxy_res = executer.submit(self.threader,arg)
                    res = proxy_res.result()
                    if self.is_web:
                        return res
                    
        else:
            raise InavalidProxyData()
            
        
        
            
            
        
                
            
    def threader(self,proxys):
        queue = Queue.Queue()
        queuelock = threading.Lock()
        threads = []
        global proxy_data
        proxy_data =[]
        for proxy in proxys:
            queue.put(proxy)

        while not queue.empty():
            queuelock.acquire()
            for workers in range(len(proxys)//4):
                t = threading.Thread(target=self.main, args=(queue,))
                t.setDaemon(True)
                t.start()
                threads.append(t)
            for t in threads:
                t.join()
            queuelock.release()       
        return proxy_data
    
    
    def main(self,q):
        if not q.empty():
            proxy = q.get(False)
            proxy = proxy.replace("\r", "").replace("\n", "")
            
            key = [i for i in self.proxy_type_connector]
            value = [self.proxy_type_connector[i].format(proxy) for i in self.proxy_type_connector ]
            
            proxy_type = {
                key[0]: value[0],
                key[1]: value[1]
            }
            session = self.session
            session.proxies.update(proxy_type)
            session.headers.update({("User-Agent", random.choice(user_agents))})
            try:
                res = session.get(self.url,timeout=120)
                
                if res.ok:
                    
                    proxy_data.append(proxy)
                    if not self.is_web:
                        print( "\033[1;32m --[+] ", proxy, " | PASS \n" )
                        self.save_data(data=proxy,mode='a')
                else:
                    if not self.is_web:
                        print("\033[1;31m --[!] ", proxy, " | FAILED\n")
            except Exception as e:
                if not self.is_web:
                    print("\033[1;31m --[!] ", proxy, " | FAILED\n")
                    pass
                return
            
            

