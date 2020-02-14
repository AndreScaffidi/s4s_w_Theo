##############################
import requests
from bs4 import BeautifulSoup
import numpy as np
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from selenium import webdriver
##############################
# A python script to scrape rumor-mill information. https://sites.google.com/site/postdocrumor/
##############################
# Choose dates to get data from! 
dates      = [2016,2015,2014,2013]
# Scrape data
s          = requests.Session()
data       = {}
accep_hist = {}
offer_hist = {}
decl_hist  = {}
def get_page(date):
        date_string       = str(date)
        data[date_string] = []
        r = s.get("https://sites.google.com/site/postdocrumor/%s-rumors" %(str(date)))
        soup    = BeautifulSoup(r.content, "html.parser")
        iframe  =  soup.find_all('iframe')
        iframe  =  str(soup.find_all('iframe')[0]['src'])
        driver  = webdriver.Firefox()
        driver.get(iframe)
        page    = driver.page_source
        driver.quit()
        soup1   = BeautifulSoup(page,"html5lib")
        url = str(soup1.find_all("iframe")[0]['src'])
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        table = soup.find('tbody')
        rows = table.find_all('tr')
        for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                cols.append(date)
                data[date_string].append([ele for ele in cols if ele]) # Get rid of empty values
        # Collect the relevant data
        # Just want status (accepted etc) and date.
        status     = [x[3].encode('utf-8') for x in data[date_string] if "Name" not in x[0] if "/17" not in x[4]]
        ED         = datetime(2020,1,1)
        date       = [datetime.strptime(x[4], "%m/%d/%Y %H:%M:%S")+timedelta(days=365*(2020-x[5])) for x in data[date_string] if "Name" not in x[0] if "/17" not in x[4]]
        accep_hist[date_string] = []
        offer_hist[date_string] = []
        decl_hist[date_string]  = []
        for ii, entry in enumerate (status):
                if "Accepted" in entry:
                        accep_hist[date_string].append(date[ii])
                if "Offered" in entry:
                        offer_hist[date_string].append(date[ii])
                if "Declined" in entry:
                        decl_hist[date_string].append(date[ii])
        accep_hist[date_string] = mdates.date2num(accep_hist[date_string])
        offer_hist[date_string] = mdates.date2num(offer_hist[date_string])
        decl_hist[date_string]  = mdates.date2num(decl_hist[date_string])
        np.savetxt('Rumnor_Mill_Acceptance_%s' %(date_string),accep_hist[date_string])
        np.savetxt('Rumnor_Mill_Offers_%s' %(date_string),offer_hist[date_string])
        np.savetxt('Rumnor_Mill_Declines_%s' %(date_string),decl_hist[date_string])

def get_page_pre2016(date):
        date_string       = str(date)
        data[date_string] = []
        r = s.get("https://sites.google.com/site/postdocrumor/%s-rumors" %(str(date)))
        soup    = BeautifulSoup(r.content, "html.parser")
        table = soup.find_all('table',{"id","goog-ws-list-table"})
        table = table[0].find('tbody')
        rows = table.find_all('tr')
        for row in rows:
                cols = row.find_all('td')
                cols = [ele.text.strip() for ele in cols]
                cols.append(date)
                data[date_string].append([ele for ele in cols if ele])

        status     = [x[2].encode('utf-8') for x in data[date_string] if "Name" not in x[0]]
        ED         = datetime(2020,1,1)
        date       = [datetime.strptime(x[3], "%B %d, %Y")+timedelta(days=365*(2020-x[4])) for x in data[date_string] if "Name" not in x[0]]
        accep_hist[date_string] = []
        offer_hist[date_string] = []
        decl_hist[date_string]  = []
        for ii, entry in enumerate (status):
                if "Accepted" in entry:
                        accep_hist[date_string].append(date[ii])
                if "Offered" in entry:
                        offer_hist[date_string].append(date[ii])
                if "Declined" in entry:
                        decl_hist[date_string].append(date[ii])
        accep_hist[date_string] = mdates.date2num(accep_hist[date_string])
        offer_hist[date_string] = mdates.date2num(offer_hist[date_string])
        decl_hist[date_string]  = mdates.date2num(decl_hist[date_string])
        np.savetxt('Rumor_Mill_Data/Rumnor_Mill_Acceptance_%s' %(date_string),accep_hist[date_string])
        np.savetxt('Rumor_Mill_Data/Rumnor_Mill_Offers_%s' %(date_string),offer_hist[date_string])
        np.savetxt('Rumor_Mill_Data/Rumnor_Mill_Declines_%s' %(date_string),decl_hist[date_string])
for date in dates:
        get_page_pre2016(date)
