# ProxyToolKit 
***This Module is used to scrape and check porxies without any limitations, Users can retrive data or save data according to there choice,Saving Data Stored in currently working Dictonary Retrive data is usefull when the module is using in a webapp or projects***

<br>

## Latest version : V.01 <br>

Saving Data Stored in currently working Dictonary Retrive data is usefull when the module is using in a webapp or projects### Features : <br>
#####    [+]  User can scrape 3k+ proxies<br>
#####    [+]  No Proxy Checking limitations<br>
#####    [+]  High Speed <br>
#####    [+]  Saving Files by creating folder and named by using type & Current time including sec & millisec <br>
#####    [+]  Returning Response or Saving Feature Available<br>
#####    [+]  completely Free <br>

### [+] Examples <br>

##### Scraping: 

```
#Import Module
from ProxyToolKit.Scraper import Scraper

#Call Class 
scraper = Scraper(
    proxy_type='https', #Type of the proxy you want 
    is_web=False, #is_web True this class will retun responce else Save Scraped Proxys
)
scraper.scrape() #Run 

``` 

##### Checking: 
```
#Import Module
from ProxyToolKit.Checker import checker

#these are the three types of valid proxy checker input

proxy = ['proxy:port','proxy:port','proxy:port','proxy:port'] 

proxy = '''
proxy:port
proxy:port
proxy:port
proxy:port
proxy:port
proxy:port
'''

proxy = '/home/user/somewhere/proxt.txt'

#Call Class 
scraper = checker(
    proxys=proxy, #here You define  proxy if You are providing a path then turn "is_path = True" ,If you are giving a  list or string "is_path=False"
    proxy_type='https', #Type of the proxy you want 
    is_web=False, #is_web True this class will retun responce else Save Scraped Proxys
    is_path=True,#Turn to true if ur using a path to proxy
    )
scraper.check() #Run 

```
##### Returning Response: 
```
from ProxyToolKit.Scraper import Scraper

scraper = Scraper(
    proxy_type='https',
    is_web=True, 
)
proxys = scraper.scrape() # Run 

print(proxys)

```

### [+] Support :-

<a href="https://t.me/https://t.me/CodingWithDevil_yt"><img src="https://img.shields.io/badge/telegram-D14836?color=2CA5E0&style=for-the-badge&logo=telegram&logoColor=white"></a>
<a href="https://www.instagram.com/codingwithdevil"><img src="https://img.shields.io/badge/instagram-%23E4405F.svg?&style=for-the-badge&logo=instagram&logoColor=white"></a>
<a href="https://www.youtube.com/c/codingwithdevil"><img src="https://img.shields.io/youtube/channel/subscribers/UCnKlznTEohj_PCw9cuxy8Zg?style=social"></a>
<a href="https://t.me/CodingWithDevil"><img src="https://img.shields.io/badge/Telegram-Group-blue"></a>
<a href="https://t.me/Codingwithdevil_group_chat"><img src="https://img.shields.io/badge/Telegram-Group%20Chat-blue"></a>


