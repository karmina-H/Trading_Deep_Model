import requests
import time
import csv
import os
from datetime import datetime


MARKET_CODE = "KRW-BTC"  # 조회할 마켓 코드 (예: KRW-BTC, KRW-ETH)
FETCH_INTERVAL_SECONDS = 3  # 데이터 조회 간격 (초 단위, 300초 = 5분)
COUNT_PER_FETCH = 200     # 한 번에 요청할 체결 개수 (업비트 최대 200개)
CSV_FILENAME = f"upbit_{MARKET_CODE}_trades.csv" # 저장할 파일 이름

# --- 변수 ---
# 마지막으로 저장한 체결의 고유 ID를 저장할 변수
# 스크립트가 시작할 때는 0으로 초기화
# last_sequential_id = 0

# CSV 파일 헤더 준비
csv_header = [
    'market', 'trade_date_utc', 'trade_time_utc', 'timestamp', 
    'trade_price', 'trade_volume', 'prev_closing_price', 'change_price', 'ask_bid', 'sequential_id'
]

def main():
    while True:
        last_sequential_id = 0
        try:
            url = f"https://api.bithumb.com/v1/trades/ticks?market={MARKET_CODE}&count={COUNT_PER_FETCH}"
            headers = {"accept": "application/json"}
            response = requests.get(url, headers=headers)
            
            # 응답이 성공적인지 확인 (200 = OK)
            if response.status_code != 200:
                print(f"API 요청 오류: {response.status_code} - {response.text}")
                time.sleep(FETCH_INTERVAL_SECONDS)
                continue # 에러 발생 시 이번 주기는 건너뛰고 다음 주기에 다시 시도

            trades = response.json()
            
            # 2. 새로운 체결 내역 필터링
            new_trades = []
            for trade in trades:
                # API에서 받은 데이터의 고유 ID가 마지막으로 저장한 ID보다 클 경우에만 추가
                if trade['sequential_id'] > last_sequential_id:
                    new_trades.append(trade)

            # 3. 새로운 체결 내역이 있다면 파일에 저장
            if new_trades:
                # API 응답은 최신순이므로, 파일에 시간순으로 저장하기 위해 리스트를 뒤집음
                new_trades.reverse()
                
                # 파일이 이미 존재하는지 확인하여 헤더를 한 번만 쓰도록 함
                file_exists = os.path.exists(CSV_FILENAME)
                
                with open(CSV_FILENAME, mode='a', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=csv_header)
                    
                    if not file_exists:
                        writer.writeheader() # 파일이 없으면 헤더 작성
                    
                    writer.writerows(new_trades) # 새로운 데이터 추가
                
                # 마지막으로 저장된 체결 ID를 최신 값으로 업데이트
                last_sequential_id = new_trades[-1]['sequential_id']
                
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{now}] {len(new_trades)}개의 새로운 체결 내역을 저장했습니다. (Last ID: {last_sequential_id})")

            else:
                now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{now}] 새로운 체결 내역이 없습니다.")

        except Exception as e:
            print(f"오류 발생: {e}")

        # 4. 다음 요청까지 5분 대기
        time.sleep(FETCH_INTERVAL_SECONDS)

if __name__ == '__main__':
    main()