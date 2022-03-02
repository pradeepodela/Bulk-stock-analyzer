import pandas as pd
import numpy as np
from stocks_toolkit import stocks_toolkit
from datetime import date , datetime
from nsetools import Nse 
from tradingview_ta import TA_Handler, Interval, Exchange
import pyrebase
import streamlit as st
import pandas as pd



coumpines_listed = []
stron_buy = []
weak_buy = []
sell = []
neutral = []
nse = Nse()
all_stock_codes = nse.get_stock_codes()
for i in all_stock_codes:
    coumpines_listed.append(i)
coumpines_listed.remove('SYMBOL')
# print(coumpines_listed)
# print(len(coumpines_listed))
for num , i in enumerate(coumpines_listed):
    
    print(num,i)
    if '-' in i:
        i = i.replace('-','_')
        coumpines_listed[num] = i

def get_predecation(stock_symbol,interval):
    """
    Get analysis for a given stock
    :param stock_symbol: symbol of the stock
    :param interval: interval of the stock
    :return:
    """
    data = TA_Handler(
        symbol=stock_symbol,
        screener="india",
        exchange="nse",
        interval=interval,
        proxies={'http': 'http://50.114.128.23:3128'} # Uncomment to enable proxy (replace the URL).
        )
    analysis = data.get_analysis().summary
    return analysis


st.title("Technical Analysis")
st.markdown(
	'''
	<style>
	[data-testid='sidebar'][aria-expanded='true'] > div:firstchild{width:400px}
	[data-testid='sidebar'][aria-expanded='false'] > div:firstchild{width:400px , margin-left: -400px}
	</style>
	''',
	unsafe_allow_html=True
)


st.markdown('---')
st.title("All Stock Analysis")
interval = st.selectbox('interval', ['1m', '5m', '15m', '30m', '1h', '4h', '1d', '1w', '1M'])
if interval == '1m':
    interval = Interval.INTERVAL_1_MINUTE
elif interval == '5m':
    interval = Interval.INTERVAL_5_MINUTES
elif interval == '15m':
    interval = Interval.INTERVAL_15_MINUTES
elif interval == '30m':
    interval = Interval.INTERVAL_30_MINUTES
elif interval == '1h':
    interval = Interval.INTERVAL_1_HOUR
elif interval == '4h':
    interval = Interval.INTERVAL_4_HOURS
elif interval == '1d':
    interval = Interval.INTERVAL_1_DAY
elif interval == '1w':
    interval = Interval.INTERVAL_1_WEEK
elif interval == '1M':
    interval = Interval.INTERVAL_1_MONTH
SUDMIT = st.button('UPLOAD DATA')
st.markdown('---')
if SUDMIT:
    for num , n in enumerate(coumpines_listed):
            try:
                p = get_predecation(n,interval)
                
                if p['RECOMMENDATION'] == 'STRONG_BUY':
                    stron_buy.append(n)
                    print(n,':',p['RECOMMENDATION'])
                    
                elif p['RECOMMENDATION'] == 'BUY':
                    weak_buy.append(n)
                    print(n,':',p['RECOMMENDATION'])
                    
                elif p['RECOMMENDATION'] == 'SELL':
                    sell.append(n)
                    print(n,':',p['RECOMMENDATION'])


                elif p['RECOMMENDATION'] == 'NEUTRAL':
                    neutral.append(n)
                    print(n,':',p['RECOMMENDATION'])
                
                
                else:
                    pass
            except:
                print(f'error processing {n}')
st.markdown('---')
btn = st.button('Show Analysis')
strongbuy = pd.DataFrame(stron_buy)
weakbuy = pd.DataFrame(weak_buy)
sell = pd.DataFrame(sell)
neutral = pd.DataFrame(neutral)
st.title("Strong Buy")
st.dataframe(strongbuy)
st.markdown('---')
st.title("Weak Buy")
st.dataframe(weakbuy)
st.markdown('---')
st.title("Sell")
st.dataframe(sell)
st.markdown('---')
st.title("Neutral")
st.dataframe(neutral)
st.markdown('---')