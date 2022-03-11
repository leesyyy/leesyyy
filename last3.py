import time
import pyupbit

access = "6eShE0UrJKvExc8tDOQzDnpwoxQUvFSsNxywGJEx"
secret = "V0LFL8ol8sIkxzzM1IogVIVN7BGxxxawdsdLNPRX"

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
def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")

# 자동매매 시작
while True:
    try:
        ask_size = (pyupbit.get_orderbook(ticker="KRW-BTC")['total_ask_size'])
        bid_size = (pyupbit.get_orderbook(ticker="KRW-BTC")['total_bid_size']) 
        current_price = get_current_price("KRW-ETH")
        avbp = (upbit.get_balances()[1]['avg_buy_price'])
        avk = float(avbp)*1.005
        avks = float(avbp)*0.997
        if ask_size > bid_size*10 and current_price < avks:
            krw = get_balance("KRW")
            if krw > 5000:
                upbit.buy_market_order("KRW-ETH", krw*0.9995)

        if ask_size < bid_size*10 and current_price > avk:
            coin = get_balance("ETH")
            if coin > 0.0016:
                upbit.sell_market_order("KRW-ETH", coin*0.9995)
        time.sleep(1)
    except Exception as e:
        print(e)
        time.sleep(1)
        
