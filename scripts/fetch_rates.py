import requests
import json
from datetime import datetime
import os

def fetch_and_calculate():
    api_key = "48fedcdc4cd48e9a5554963dacbeaee4"
    url = f"https://api.metalpriceapi.com/v1/latest?api_key={api_key}&base=USD&currencies=PKR,XAU"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('success'):
            print(f"API Error: {data.get('error')}")
            return

        rates = data['rates']
        
        # Math provided by user:
        # price_1_ounce_usd = 1 / rates['XAU']
        # price_1_ounce_pkr = price_1_ounce_usd * rates['PKR']
        # price_1_tola_pkr = price_1_ounce_pkr * 0.375
        
        xau_rate = rates['XAU'] # ounces per USD
        pkr_rate = rates['PKR'] # PKR per USD
        
        price_1_ounce_usd = 1 / xau_rate
        price_1_ounce_pkr = price_1_ounce_usd * pkr_rate
        price_1_tola_pkr = price_1_ounce_pkr * 0.375
        
        result = {
            "rate": round(price_1_tola_pkr, 2),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "unit": "PKR / Tola"
        }
        
        # Save to gold_rate.json in the root directory (one level up from scripts/)
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(root_dir, 'gold_rate.json')
        
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=4)
            
        print(f"Successfully updated gold rate: {result['rate']} PKR/Tola")

    except Exception as e:
        print(f"Failed to fetch or calculate rates: {e}")

if __name__ == "__main__":
    fetch_and_calculate()
