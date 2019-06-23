#!/usr/bin/env python
# coding: utf-8

# <h2> Import Requirements </h2>

# In[69]:


import pandas as pd
import numpy as np
import scipy as sp
import gc
import sklearn
import pickle


# In[71]:


classifcols = pd.read_pickle('../data/classifcols.pkl')
regrcols = pd.read_pickle('../data/regrcols.pkl')
labencdist = pd.read_pickle('../data/labencdist.pkl')
labencsector = pd.read_pickle('../data/labencsector.pkl')
onehotenc = pd.read_pickle('../data/onehotenc.pkl')
classifmdl = pd.read_pickle('../data/divclassifrf.pkl')
#Please ensure that the right regression model is loaded. GitHub denied loading of the full 50 MB file, and had to
#be externally added to this Jupyter notebook
regrmdl = pd.read_pickle('../data/divregrrf.pkl')


# <h2> Define Supplementary Functions to Aid Monte Carlo Simulations </h2>

# While it would be ideal to get inputs for all data values we undertake, it is in interest of user ease that we create a tradeoff of accuracy and convenience. Hence, using the notion of correlation, we take only five growth rate inputs and approximate model inputs accordingly.

# <b> STEP 1 - Define 5 Buckets for Model Variables </b>

# In[86]:


totcols = list(set(classifcols).union(set(regrcols)).union(set(['Div_Paid?'])))
liabcols = ['Short-term debt','Accounts payable', 'Taxes payable',
            'Accrued liabilities','Other current liabilities', 
            'Total current liabilities','Long-term debt','Average Payables',
            'Deferred taxes liabilities','Other long-term liabilities', 
            'Total non-current liabilities','Total liabilities',
            'Days Payables Outstanding','Payables Turnover']
assetcols = ['Total cash','Receivables','Inventories','Prepaid expenses', 
             'Other current assets','Total current assets','Goodwill',
             'Gross property, plant and equipment','Other long-term assets',
             'Net property, plant and equipment','Intangible assets', 
             'Total non-current assets','Total assets','Average Inventory',
             'Average Receivables',"Total liabilities and stockholders' equity",
             'Cash per Share','Days Sales Outstanding','Days of Inventory on Hand',
             'Inventory Turnover']
inccols = ['Gross profit','Research and development','Operating income', 
           'Sales, General and administrative','Interest Expense',
           'Total operating expenses', 'Other income (expense)', 
           'Income before taxes','Provision for income taxes', 'Net income', 
           'Basic_EPS','Diluted_EPS', 'EBITDA', 'Interest Coverage',
           'Net Income per Share'] 
equitycols = ['Common stock', 'Additional paid-in capital','Retained earnings', 
              'Treasury stock','Accumulated other comprehensive income',
              'Market Cap', 'Book Value per Share','Invested Capital',
              "Shareholders Equity per Share"]
entvcols = ['EV to Free cash flow','Enterprise Value','stockprc','mth12stockratio',
            'mth6stockratio', 'PFCF ratio']
revcols = ['Revenue', 'Revenue per Share']


# <b> STEP 2 - Define Model Input and Updating Methods </b>

# In[ ]:



def mdlinpt(comp):
    alldata = pd.read_pickle('../data/sp500finaldata.pkl')
    alldata.sort_values(by=['firm', 'Year'], ascending=[True, True], inplace=True)
    distenc = pd.DataFrame(labencdist.transform(alldata['DistanceFromLast']))
    sectenc = pd.DataFrame(labencsector.transform(alldata['Sector']))
    hotencoded = onehotenc.transform(pd.concat([sectenc, distenc], axis=1))
    namesdist = ['DistLast_'+i for i in labencdist.classes_]
    namessect = ['Sector_'+i for i in labencsector.classes_]
    names = np.append(namessect, namesdist)
    hotencoded = pd.DataFrame(hotencoded, columns=names)
    alldata.drop(['Sector', 'DistanceFromLast'], axis=1, inplace=True)
    alldata = pd.concat([alldata, hotencoded], axis=1)
    maxrec = alldata[(alldata.firm==comp) & (alldata.firm != alldata.firm.shift(-1))]
    maxrec = maxrec[totcols].reset_index(drop=True)
    return maxrec

def updater(maxrec, grrev, grinc, grasset, grliab, grentv):
    maxrec[assetcols] *= (1+ float(grasset)/100)
    maxrec[liabcols] *= (1 + grliab/100)
    maxrec[inccols] *= (1 + grinc/100)
    maxrec[revcols] *= (1 + grrev/100)
    maxrec['Cost of revenue'] = maxrec['Revenue'] - maxrec['Gross profit']
    if isinstance(maxrec["Total stockholders' equity"], pd.Series):
        oldeq = maxrec["Total stockholders' equity"].reset_index(drop=True)[0]
    else:
        oldeq = maxrec["Total stockholders' equity"]
    maxrec["Total stockholders' equity"] = maxrec['Total assets'] - maxrec['Total liabilities']
    if isinstance(maxrec["Total stockholders' equity"], pd.Series):
        oldeq = maxrec["Total stockholders' equity"].reset_index(drop=True)[0] / oldeq
    else:
        oldeq = maxrec["Total stockholders' equity"] / oldeq
    maxrec[equitycols] *= oldeq
    maxrec[entvcols] *= (1 + grentv/100)
    #Updated final ratios
    maxrec['Intangibles to Total Assets']  = maxrec['Intangible assets'] / maxrec['Total assets']
    maxrec['Debt to Assets'] = maxrec['Total liabilities'] / maxrec['Total assets']
    maxrec['EV to Sales'] = maxrec['Enterprise Value'] / maxrec['Revenue']
    maxrec['Enterprise Value over EBITDA'] = maxrec['Enterprise Value'] / maxrec['EBITDA']
    maxrec['R&D to Revenue'] = maxrec['Research and development'] / maxrec['Revenue']
    maxrec['SG&A to Revenue'] = maxrec['Sales, General and administrative'] / maxrec['Revenue']
    maxrec['Price to Sales Ratio'] *= grentv/grrev
    maxrec['Paid_LastYr?'] = maxrec['Div_Paid?']
    maxrec['Net Debt to EBITDA'] = maxrec['Total liabilities'] / maxrec['EBITDA']
    maxrec['currentRatio'] = maxrec['Total current assets'] / maxrec['Total current liabilities']
    maxrec['grossProfitMargin'] = maxrec['Gross profit'] / maxrec['Revenue']
    maxrec['operatingProfitMargin'] = maxrec['Operating income'] / maxrec['Revenue']
    maxrec['assetTurnover'] = maxrec['Revenue'] / maxrec['Total assets']
    maxrec['returnOnAssets'] = maxrec['Net income'] / maxrec['Total assets']
    maxrec['Net Current Asset Value'] = maxrec['Total current assets'] - maxrec['Total liabilities']
    maxrec['PB ratio'] = maxrec['stockprc'] / maxrec['Book Value per Share']
    return maxrec


# <h2> Perform 10-Year Monte Carlo Simulations </h2>

# In[87]:


def simulate(comp, grrev, grinc, grasset, grliab, grentv):
    firstfile = updater(mdlinpt(comp), grrev, grinc, grasset, grliab, grentv)
    firstfile = firstfile.loc[np.array([0]).repeat(1000)]
    firstfile.reset_index(drop=True, inplace=True)
    np.random.seed(1)
    rand = pd.DataFrame(np.random.random((1000, 10)))
    state = pd.DataFrame(np.zeros((1000, 11)))
    lossarr = np.zeros(10)
    state.iloc[:,0] = firstfile['Div_Paid?']
    divarr = np.zeros(10)
    for yr in range(0, 10):
        print(yr)
        probs = classifmdl.predict_proba(firstfile[classifcols])
        probdiv = pd.Series(probs.reshape(1,-1)[0][1::2])
        state[yr+1] = ((rand[yr] < probdiv) * 1)
        regrprobs = pd.Series(regrmdl.predict(firstfile[regrcols]))
        lossarr[yr] = sum(regrprobs[state[yr+1] == True])/1000
        #Update dynamic variables
        firstfile['Div_Paid?'] = state[yr+1]
        firstfile = firstfile.apply(lambda s: updater(s, grrev, grinc, grasset, grliab, grentv), axis=1)
    lossarr = [round(i, 4) for i in lossarr]
    return lossarr


# In[ ]:




