import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta


def get_candle_minute(name, minutes, count=1, t_hour=0, t_minute=0): #분봉, 
    '''
    name = 종목이름(KRW-BTC)
    minute = 몇분봉가져올지(1, 3, 5, 10, 15, 30, 60, 240)
    count = 캔들 몇개가져올지(최대200개)
    t_hour,t_minute = 몇시간 몇분전 캔들부터 가져올지
    time = 언제기준으로 가져올지(kst기준시며 default는 가장 최근 캔들, yyyy-MM-dd HH:mm:ss)
    '''
    now = datetime.now()
    # n시간 n분전
    time_ago = now - relativedelta(hours=t_hour, minutes=t_minute)
    start_time = time_ago.strftime('%Y-%m-%d %H:%M:%S')

    url = f"https://api.bithumb.com/v1/candles/minutes/{minutes}?market={name}&to={start_time}&count={count}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    return response.text


def get_candle_day(name, days=0, count=1): #일봉
    '''
    name = 종목이름(KRW-BTC)
    days = 캔들가져오는 시작 날짜(현재로부터 몇일 전부터 시작할지)
    count = 캔들 몇개가져올지(최대200개)
    '''
    now = datetime.now()
    # n시간 n분전
    time_days_ago = now - relativedelta(days=days)
    start_time = time_days_ago.strftime('%Y-%m-%d %H:%M:%S')

    url = f"https://api.bithumb.com/v1/candles/days?market={name}&to={start_time}&count={count}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    return response.text

def get_candle_week(name, days=0, count=1): #주봉
    '''
    name = 종목이름(KRW-BTC)
    days = 캔들가져오는 시작 날짜(현재로부터 몇일 전부터 시작할지)
    count = 캔들 몇개가져올지(최대200개)
    '''
    now = datetime.now()
    # n시간 n분전
    time_days_ago = now - relativedelta(days=days)
    start_time = time_days_ago.strftime('%Y-%m-%d %H:%M:%S')

    url = f"https://api.bithumb.com/v1/candles/weeks?market={name}&to={start_time}&count={count}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    return response.text

def get_candle_month(name, days=0, count=1): #주봉
    '''
    name = 종목이름(KRW-BTC)
    days = 캔들가져오는 시작 날짜(현재로부터 몇일 전부터 시작할지)
    count = 캔들 몇개가져올지(최대200개)
    '''
    now = datetime.now()
    # n시간 n분전
    time_days_ago = now - relativedelta(days=days)
    start_time = time_days_ago.strftime('%Y-%m-%d %H:%M:%S')

    url = f"https://api.bithumb.com/v1/candles/months?market={name}&to={start_time}&count={count}"

    headers = {"accept": "application/json"}

    response = requests.get(url, headers=headers)

    return response.text
