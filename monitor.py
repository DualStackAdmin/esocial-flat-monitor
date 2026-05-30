import time
import re
import urllib.request
import urllib.parse
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# --- TƏNZİMLƏMƏLƏR ---
# DİQQƏT: Öz Telegram Bot Token və Chat ID-nizi bura yazın
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN_HERE"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID_HERE"
FLAG_FILE = "startup_msg_sent.flag"

# --- LAYİHƏLƏR SİYAHISI ---
PROJECTS = [
    {
        "name": "Ramana",
        "url": "https://ms.sosial.gov.az/flats/?region=Bak%C4%B1+%C5%9F%C9%99h%C9%99ri%2C+Sabun%C3%A7u+rayonu%2C+Ramana+q%C9%99s%C9%99b%C9%99si&project=Ramana+q%C9%99s%C9%99b%C9%99si+-+Yeni+ya%C5%9Fay%C4%B1%C5%9F+kompleksi&flatstatus=nonbooked"
    },
    {
        "name": "Kürdəxanı",
        "url": "https://ms.sosial.gov.az/flats/?region=Bak%C4%B1+%C5%9F%C9%99h%C9%99ri%2C+Sabun%C3%A7u+rayonu%2C+K%C3%BCrd%C9%99xan%C4%B1+q%C9%99s%C9%99b%C9%99si&project=K%C3%BCrd%C9%99xan%C4%B1+q%C9%99s%C9%99b%C9%99si+-+Yeni+ya%C5%9Fay%C4%B1%C5%9F+kompleksi&flatstatus=nonbooked"
    }
]

def get_public_ip():
    try:
        with urllib.request.urlopen('https://api.ipify.org') as response:
            return response.read().decode('utf8')
    except:
        return "Təyin edilə bilmədi"

def send_telegram(message):
    try:
        base_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        params = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
        query_string = urllib.parse.urlencode(params)
        with urllib.request.urlopen(f"{base_url}?{query_string}") as response:
            pass
    except Exception as e:
        print(f"Telegram xətası: {e}")

def check_status():
    print(f"[{datetime.now()}] Yoxlama başladı...")

    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36")

    driver = None
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        for project in PROJECTS:
            proj_name = project["name"]
            proj_url = project["url"]

            try:
                print(f"--- Yoxlanılır: {proj_name} ---")
                driver.get(proj_url)
                time.sleep(10)

                html_source = driver.page_source
                match = re.search(r"Toplam mənzil[^0-9]*(\d+)", html_source)
                timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

                if match:
                    count = int(match.group(1))
                    if count == 0:
                        print(f"{timestamp} | {proj_name}: 0")
                    else:
                        alert_msg = f"🚨 DİQQƏT! {proj_name.upper()} - MƏNZİL TAPILDI!\nSay: {count}\nTarix: {timestamp}\nLink: {proj_url}"
                        print(f"\n{alert_msg}\n")
                        send_telegram(alert_msg)
                else:
                    print(f"{proj_name}: Rəqəm tapılmadı.")

            except Exception as e:
                print(f"{proj_name} xətası: {e}")

            time.sleep(2)

    except Exception as e:
        print(f"Ümumi Xəta: {e}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    flag_path = os.path.join(script_dir, FLAG_FILE)

    if not os.path.exists(flag_path):
        ip_address = get_public_ip()
        msg = f"✅ Monitorinq Bərpa Edildi (Cron Rejimi)!\n🌍 IP: {ip_address}"
        send_telegram(msg)
        with open(flag_path, 'w') as f:
            f.write("Sent")

    check_status()
