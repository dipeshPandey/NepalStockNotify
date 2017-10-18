import winBallon as wb
import requests,threading,time,sys
from bs4 import BeautifulSoup

class NepalStockServices:
##    global codeList;
##    global d;
    def __init__(self):
        print "Initilization"

def getMarketStatus():
    page = requests.get("http://www.nepalstock.com/")
    soup = BeautifulSoup(page.content, 'html.parser')
    market = soup.find_all('div', attrs={'id':'top-notice-bar'})
##    print market[0].get_text()
    marketStatus = market[0].get_text()
    return marketStatus
##    return "a"

def getUrlCode(stockCode):
    ad = loadAllStockCode();
    u = stockCode.upper()
    try:
        urlCode = ad[u]
    except KeyError:
        print "The code is incorrect"
        urlCode="0"
    return urlCode

def getRecentPrice(url_code):
    page = requests.get("http://www.nepalstock.com/marketdepthofcompany/"+url_code)
    soup = BeautifulSoup(page.content, 'html.parser')
    data = soup.find_all('label', attrs={'class':'livePrice'})
    recentPrice = data[0].get_text().strip()
    return recentPrice
    
    
def getMarketDepthSell(code,url_code,threshold):

    page = requests.get("http://www.nepalstock.com/marketdepthofcompany/"+url_code);
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table', attrs={'class':'table table-striped table-bordered orderTable'})
##    try:
##        rows = table[1].find_all('tr')
##        data_sell = rows[1].get_text()
##        data_sell_float = float(data_sell.replace(',',''))
##        print type(data_sell_float)
##    except:
##        print "Error Parsing"
        
    rows = table[1].find_all('tr')
    data_sell = rows[1].get_text()
    data_sell_float = float(data_sell.replace(',',''))
    threshold_f =float(threshold)
    data_sell_float = 2200; 
    while True:
        print data_sell_float
        if(data_sell_float <= threshold_f):
            wb.balloon_tip("Alert "+code.upper(),"Seller is available Below "+threshold,10)
            sys.exit()
        else:
            print "Running in background"

        data_sell_float-=2;
        time.sleep(5)

def getMarketDepthBuy(code,url_code,threshold):
    page = requests.get("http://www.nepalstock.com/marketdepthofcompany/"+url_code);
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table', attrs={'class':'table table-striped table-bordered orderTable'})
    rows = table[0].find_all('tr')
    data_buy = rows[1].get_text()
    data_buy_float = float(data_buy.replace(',',''))
    threshold_f =float(threshold)
##    data_buy_float = 2180; 
    while True:
        print data_sell_float
        if(data_sell_float >= threshold_f):
            wb.balloon_tip("Alert "+code.upper(),"Buyer is available Above "+threshold,10)
            sys.exit()
        else:
            print "Running in background"

        data_sell_float+=2;
        time.sleep(5)
    

def loadAllStockCode():
    page = requests.get("http://www.nepalstock.com/")
    soup = BeautifulSoup(page.content, 'html.parser')
    code = soup.find_all('select',{'id':'StockSymbol_Select'})
    options = code[0].find_all('option')
    d = {}
    for l in options:
        stockCode = l.text
        urlCode = l['value']
        d[stockCode] = urlCode
    return d


