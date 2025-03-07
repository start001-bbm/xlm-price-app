import streamlit as st
import requests
import pandas as pd
import time

st.title("仮想通貨XLMリアルタイム価格比較")

# USD/JPYレート取得（5分キャッシュ）
@st.cache_data(ttl=300)
def get_usd_jpy():
    res = requests.get('https://open.er-api.com/v6/latest/USD').json()
    return res['rates']['JPY']

# 各取引所の価格取得関数
def get_prices():
    usd_jpy = get_usd_jpy()
    prices = {}

    # Bybit
    try:
        res = requests.get('https://api.bybit.com/v5/market/tickers?category=spot&symbol=XLMUSDT').json()
        prices['Bybit'] = round(float(res['result']['list'][0]['lastPrice']) * usd_jpy, 4)
    except:
        prices['Bybit'] = '取得失敗'

    # Binance Japan
    try:
        res = requests.get('https://api.binance.com/api/v3/ticker/price?symbol=XLMJPY').json()
        prices['Binance JP'] = round(float(res['price']), 4)
    except:
        prices['Binance JP'] = '取得失敗'

    # GMOコイン
    try:
        res = requests.get('https://api.coin.z.com/public/v1/ticker?symbol=XLM').json()
        prices['GMOコイン'] = round(float(res['data'][0]['last']), 4)
    except:
        prices['GMOコイン'] = '取得失敗'

    # bitbank追加
    try:
        res = requests.get('https://public.bitbank.cc/xlm_jpy/ticker').json()
        prices['bitbank'] = round(float(res['data']['last']), 4)
    except:
        prices['bitbank'] = '取得失敗'

    df = pd.DataFrame(prices.items(), columns=['取引所', 'XLM価格(JPY)'])
    return df

# リアルタイム表示 (5秒間隔)
placeholder = st.empty()

while True:
    df = get_prices()
    placeholder.table(df)
    st.caption("5秒ごとに更新しています...")
    time.sleep(5)
