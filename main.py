import requests

def get_usd_try_rate():
    
    url = "https://open.er-api.com/v6/latest/USD"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and data.get("result") == "success":
            usd_try = data["rates"]["TRY"]
            return usd_try
        else:
            print("API'den veri çekilirken bir sorun oluştu.")
            return None
            
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
        return None

if __name__ == "__main__":
    rate = get_usd_try_rate()
    if rate:
        print(f"[TEST] Güncel USD/TRY Kuru: {rate:.2f} TL")