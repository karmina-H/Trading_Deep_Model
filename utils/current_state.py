#즉시 사는거, 예약 구매하는거
import jwt 
import uuid
import hashlib
import time
from urllib.parse import urlencode
import requests

accessKey = ''
secretKey = ''
apiUrl = 'https://api.bithumb.com'

def set_keys():
    with open("Personal_info/key.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith("빗썸 api key"):
                accessKey = line.strip().split(" ")[-1]
            elif line.startswith("빗썸 secret key"):
                secretKey = line.strip().split(" ")[-1]
    
    if accessKey and secretKey:
        return accessKey,secretKey
    else:
        return None

def get_state(name):
    accessKey ,secretKey = set_keys()
    if accessKey is None or secretKey is None:
        print("key error!")
        return None
#'KRW-BTC'
    # Set API parameters
    param = dict( market=name )

    # Generate access token
    query = urlencode(param).encode()
    hash = hashlib.sha512()
    hash.update(query)
    query_hash = hash.hexdigest()
    payload = {
        'access_key': accessKey,
        'nonce': str(uuid.uuid4()),
        'timestamp': round(time.time() * 1000), 
        'query_hash': query_hash,
        'query_hash_alg': 'SHA512',
    }   
    jwt_token = jwt.encode(payload, secretKey)
    authorization_token = 'Bearer {}'.format(jwt_token)
    headers = {
    'Authorization': authorization_token
    }

    try:
        # Call API
        response = requests.get(apiUrl + '/v1/orders/chance', params=param, headers=headers)
        
        buy_min = 0 # 최소 구매 금액
        sell_min = 0 # 최소 매도 금액
        buy_sell_max = 0 # 최대 매수매도 금액
        can_buy_balance = 0 # 매수가능한 매도 금액및 수량 
        can_sell_balance = 0 # 판매가능한 매도 금액및 수량 
        buy_avg = 0 # 평균 매수가
        order_type = None # 주문타입
        isOpen = None # 장중인지 아닌지
        '''
        여기서 추출할 정보 ->
        매수매도 최소금액
        매수매도 최대금액
        계좌잔액
        매수 및 매도 주문가능 금액 및 수량
        매수 및 매도 주문 중 묶여있는 금액 및 수량
        매수평균가
        주문타입 : (limit = 지정가, price = 시장가)
        마켓운영상태 = active일경우 장중
        '''
        if response.status_code==200:
            buy_min = response.json()['market']['bid']['min_total']
            buy_sell_max = response.json()['market']['max_total']
            sell_min = response.json()['market']['ask']['min_total']
            can_sell_balance = response.json()['ask_account']['balance']
            can_buy_balance = response.json()['bid_account']['balance']
            buy_avg = response.json()['bid_account']['avg_buy_price']
            order_type = response.json()['market']['ask_types']
            isOpen = response.json()['market']['state']
            isOpen == 'active'

            market_data = {
            'buy_min': buy_min,
            'buy_sell_max': buy_sell_max,
            'sell_min': sell_min,
            'can_sell_balance': can_sell_balance,
            'can_buy_balance': can_buy_balance,
            'buy_avg': buy_avg,
            'order_type': order_type,
            'isOpen': isOpen}
            '''
            market_data= {'buy_min': '5000', 'buy_sell_max': '1000000000', 'sell_min': '5000', 
            'can_sell_balance': '0', 'can_buy_balance': '5000', 'buy_avg': '0', 'order_type': ['limit', 'market'], 'isOpen': 'active'}
            '''
            return market_data
        
        else:
            print("server status error!")
            return None
        
    except Exception as err:
        # handle exception
        print(err)
    

if __name__ == '__main__':
    d = get_state('KRW-BTC')
    print(d)