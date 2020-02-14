##############################
import numpy as np
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
##############################
# A python script to analyse rumor-mill information. https://sites.google.com/site/postdocrumor/
##############################
# Read in data
dates      = [2020,2019,2018,2017,2016,2015,2014,2013]
accep_hist = {}
offer_hist = {}
decl_hist  = {}
def get_data(date):
    date_string             = str(date)
    accep_hist[date_string] = np.loadtxt('Rumor_Mill_Data/Rumnor_Mill_Acceptance_%s' %(date_string))
    offer_hist[date_string] = np.loadtxt('Rumor_Mill_Data/Rumnor_Mill_Offers_%s' %(date_string))
    decl_hist[date_string]  = np.loadtxt('Rumor_Mill_Data/Rumnor_Mill_Declines_%s' %(date_string))
def plot_comb_hist():   
    ##############################
    # Combine all histograms
    for date in dates:
        get_data(date)
    accep_hist_tot = np.concatenate(accep_hist.values(),axis=0)
    offer_hist_tot = np.concatenate(offer_hist.values(),axis=0) 
    decl_hist_tot  = np.concatenate(decl_hist.values(),axis=0)
    ##############################
    # Plot total distribution  
    plt.rcParams["font.family"] = 'serif'
    fig, ax = plt.subplots(figsize=(10,8), dpi=100)
    nBins=40
    ax.hist(accep_hist_tot, bins=nBins,color='red',alpha=0.3,label=r'Accepted', normed=True)
    ax.hist(decl_hist_tot, bins=nBins,color='green',alpha=0.3,label=r'Declined', normed=True)
    ax.hist(offer_hist_tot, bins=nBins,color='blue',alpha=0.3,label=r'Offered', normed=True)
    ax.set_xlabel(r"Date",fontsize=35)
 
    ax.xaxis.set_major_locator(mdates.MonthLocator())
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%d/%m'))
    plt.tight_layout() 
    ax.legend(loc=1,frameon=True, prop={'size':20})
    plt.show()
##############################
# Excecute analysis! 
plot_comb_hist()