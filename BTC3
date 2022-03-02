import time
import pyupbit

access = ""
secret = ""

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

#    """현재가 조회"""

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        ask_size = (pyupbit.get_orderbook(ticker="KRW-ETH")['total_ask_size'])
        bid_size = (pyupbit.get_orderbook(ticker="KRW-ETH")['total_bid_size']) 
        if ask_size*3 < bid_size:
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order("KRW-ETH", krw*0.9995)
        if ask_size > bid_size*3:
            btc = get_balance("ETH")
            
            if btc > 0.0016:
                upbit.sell_market_order("KRW-ETH", btc*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
