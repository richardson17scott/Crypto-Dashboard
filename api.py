import os
from dotenv import load_dotenv
import requests

load_dotenv()

def get_all_token_prices(token_symbol):
    url = "https://pro-api.coinmarketcap.com/v2/cryptocurrency/quotes/latest"
    
    api_key = os.getenv("CMC_API_KEY")

    
    parameters = {
        'symbol': token_symbol,
        'convert': 'INR'
    }
    
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': api_key,
    }

    response = requests.get(url, params=parameters, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        
        try:
            # CMC returns a list of tokens matching the symbol under data -> SYMBOL
            token_data = data['data'][token_symbol][0]
            
            # 1. Extract the token address (stored inside 'platform')
            platform_info = token_data.get('platform')
            token_address = platform_info.get('token_address') if platform_info else "Native Asset (No Contract)"
            
            # 2. Extract the price in INR
            price_in_inr = token_data['quote']['INR']['price']
            
            # Output
            ''' print(f"Token Address : {token_address}") '''
            return (f"{price_in_inr:,.2f}")
            
        except (KeyError, IndexError):
            print("Error: Could not parse the expected token data from the response.")
    else:
        print(f"API Error {response.status_code}: {response.text}")

if __name__ == "__main__":
    print(get_all_token_prices("JMPT"))