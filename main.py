import os
import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()

def get_usd_try_rate():
   
    url = "https://open.er-api.com/v6/latest/USD"
    try:
        response = requests.get(url)
        data = response.json()
        
        if response.status_code == 200 and data.get("result") == "success":
            return data["rates"]["TRY"]
        else:
            print("API'den veri çekilirken bir sorun oluştu.")
            return None
    except Exception as e:
        print(f"Bağlantı hatası: {e}")
        return None

def send_email_alert(current_rate, target_rate, sender_email, sender_password, receiver_email):
    subject = f"🚨 KUR UYARISI: Dolar {current_rate:.2f} TL Oldu!"
    body = f"""
    Merhaba,
    
    Takip ettiğiniz USD/TRY kuru belirlediğiniz hedef seviyeyi aştı!
    
    Güncel Kur: {current_rate:.2f} TL
    Hedef Kurunuz: {target_rate:.2f} TL
    
    Bu e-posta Currency Alert Bot tarafından otomatik gönderilmiştir.
    """
    
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        print(f"✅ Uyarı e-postası başarıyla gönderildi: {receiver_email}")
        return True
    except Exception as e:
        print(f"❌ E-posta gönderilirken hata oluştu: {e}")
        return False

if __name__ == "__main__":
    SENDER_EMAIL = os.getenv("SENDER_EMAIL")
    SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
    RECEIVER_EMAIL = os.getenv("RECEIVER_EMAIL")
    TARGET_RATE = float(os.getenv("TARGET_RATE", "30.0"))

    print("🔍 Döviz kuru kontrol ediliyor...")
    current_rate = get_usd_try_rate()

    if current_rate:
        print(f"📊 Güncel Kur: {current_rate:.2f} TL | Hedef Kur: {TARGET_RATE:.2f} TL")
        
        if current_rate >= TARGET_RATE:
            print("⚡ Hedef seviye aşıldı! E-posta gönderiliyor...")
            send_email_alert(current_rate, TARGET_RATE, SENDER_EMAIL, SENDER_PASSWORD, RECEIVER_EMAIL)
        else:
            print("ℹ️ Kur henüz hedef seviyeye ulaşmadı. E-posta gönderilmedi.")