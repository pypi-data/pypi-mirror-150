import sys
from binance.client import Client
from quantml.data.historical import get_data

import os
from pathlib import Path
from dotenv import load_dotenv

dotenv_path = Path('.env')
load_dotenv(dotenv_path=dotenv_path)
API_KEY = os.getenv('API_KEY')
API_SECRET = os.getenv('API_SECRET')

def main():
    if len(sys.argv) > 1:
        arguments = sys.argv[1:]
        if arguments[0] == 'bitcoin':
            asset = 'BTCUSDT'
            start = '10 days ago UTC'
            end = '1 minutes ago UTC'
            interval = Client.KLINE_INTERVAL_5MINUTE
            print(get_data(API_KEY, API_SECRET, asset, start, end, interval))            
    else:
        print('Usage: quantml [command]')

if __name__ == "__main__":
    main()