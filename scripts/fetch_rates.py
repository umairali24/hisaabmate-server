import requests
import json
from datetime import datetime
import os

def fetch_and_calculate():
    api_key = "48fedcdc4cd48e9a5554963dacbeaee4"
    # Updated URL to include XAG
    url = f"https://api.metalpriceapi.com/v1/latest?api_key={api_key}&base=USD&currencies=PKR,XAU,XAG"
    
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        
        if not data.get('success'):
            print(f"API Error: {data.get('error')}")
            return

        rates = data['rates']
        pkr_rate = rates['PKR'] # PKR per USD

        # Gold Math (XAU)
        xau_rate = rates['XAU'] # ounces per USD
        price_1_oz_gold_usd = 1 / xau_rate
        price_1_oz_gold_pkr = price_1_oz_gold_usd * pkr_rate
        price_1_tola_gold_pkr = price_1_oz_gold_pkr * 0.375

        # Silver Math (XAG)
        xag_rate = rates['XAG'] # ounces per USD
        price_1_oz_silver_usd = 1 / xag_rate
        price_1_oz_silver_pkr = price_1_oz_silver_usd * pkr_rate
        price_1_tola_silver_pkr = price_1_oz_silver_pkr * 0.375

        # Updated JSON structure
        result = {
            "gold_rate": round(price_1_tola_gold_pkr, 2),
            "silver_rate": round(price_1_tola_silver_pkr, 2),
            "last_updated": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "currency": "PKR"
        }
        
        # Save to gold_rate.json in the root directory
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        output_path = os.path.join(root_dir, 'gold_rate.json')
        
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=4)
            
        print(f"Successfully updated rates: Gold: {result['gold_rate']}, Silver: {result['silver_rate']} PKR/Tola")

    except Exception as e:
        print(f"Failed to fetch or calculate rates: {e}")

if __name__ == "__main__":
    fetch_and_calculate()
