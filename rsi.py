import time
import pyupbit
import pandas as pd
import numpy as np
access = ""          
secret = ""

pd.set_option('display.float_format', lambda x: '%.2f' % x)

def get_balance(ticker):
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

while True:
    try:
        df = pyupbit.get_ohlcv("KRW-ETH", interval="minute1", count=60)
        df['변화량'] = df['close'] - df['close'].shift(1)
        df['상승폭'] = np.where(df['변화량']>=0, df['변화량'], 0)
        df['하락폭'] = np.where(df['변화량'] <0, df['변화량'].abs(), 0)
        df['AU'] = df['상승폭'].ewm(alpha=1/14, min_periods=14).mean()
        df['AD'] = df['하락폭'].ewm(alpha=1/14, min_periods=14).mean()
        df['RSI'] = df['AU'] / (df['AU'] + df['AD']) * 100
        mae = df.iloc[-1]['RSI']

        if mae < 40:
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order("KRW-ETH", krw*0.9995)
        if mae > 50:
            btc = get_balance("ETH")
            if btc > 0.0016:
                upbit.sell_market_order("KRW-ETH", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
