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
    marketStatus = market[0].get_text()
    return marketStatus

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
    while True:
        page = requests.get("http://www.nepalstock.com/marketdepthofcompany/"+url_code);
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find_all('table', attrs={'class':'table table-striped table-bordered orderTable'})        
        rows = table[1].find_all('tr')
        data_sell = rows[1].find_all('td')
        data_sell_float = float(data_sell[0].get_text().replace(',',''))
        threshold_f =float(threshold)
    
        print "Seller available at : "+data_sell_float
        if(data_sell_float <= threshold_f):
            wb.balloon_tip("Alert "+code.upper(),"Seller is available Below "+threshold,10)
            sys.exit()
        else:
            print "Running in background, refreshes every 10 sec "

        time.sleep(10)

def getMarketDepthBuy(code,url_code,threshold):    
    while True:
        
        page = requests.get("http://www.nepalstock.com/marketdepthofcompany/"+url_code);
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find_all('table', attrs={'class':'table table-striped table-bordered orderTable'})
        rows = table[0].find_all('tr')
        data_buy = rows[1].find_all('td')
##        print data_buy[2].get_text()
        data_buy_float = float(data_buy[2].get_text().replace(',',''))
        threshold_f =float(threshold)
        print "Buyer available at : "+str(data_buy_float)
##        print threshold_f
        if(data_buy_float >= threshold_f):
            wb.balloon_tip("Alert "+code.upper(),"Buyer is available Above "+threshold,10)
            sys.exit()
        else:
            print "Running in background, refreshes every 10 seconds"

        time.sleep(10)

    
    

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

def getMarketDepthBuyFirst(code,url_code):
    page = requests.get("http://www.nepalstock.com/marketdepthofcompany/"+url_code);
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table', attrs={'class':'table table-striped table-bordered orderTable'})	
    rows_buy = table[0].find_all('tr')
    data_buy = rows_buy[1].find_all('td')
    return data_buy[2].get_text()

def getMarketDepthSellFirst(code,url_code):
    page = requests.get("http://www.nepalstock.com/marketdepthofcompany/"+url_code);
    soup = BeautifulSoup(page.content, 'html.parser')
    table = soup.find_all('table', attrs={'class':'table table-striped table-bordered orderTable'})       
    rows_sell = table[1].find_all('tr')
    data_sell = rows_sell[1].find_all('td')
    return data_sell[0].get_text()

def f1():
    print "First Function"


     
    


