import requests
import threading
import time
import random

# ================= CONFIG =================
TARGET_REF = "eae05c144f"
THREADS = 5
USE_PROXY = True

# ==========================================

success = 0
fail = 0

# Load proxies
def load_proxies():
    try:
        with open("proxies.txt", "r") as f:
            return [p.strip() for p in f if p.strip()]
    except:
        return []

proxies_list = load_proxies()

def get_proxy():
    if USE_PROXY and proxies_list:
        proxy = random.choice(proxies_list)
        return {
            "http": f"http://{proxy}",
            "https": f"http://{proxy}"
        }
    return None

def run():
    global success, fail

    while True:
        try:
            proxy = get_proxy()

            # ====== YOUR REQUEST HERE ======
            url = "https://example.com/api"  # CHANGE THIS
            payload = {
                "referral": TARGET_REF
            }

            r = requests.post(url, json=payload, proxies=proxy, timeout=10)

            if r.status_code == 200:
                success += 1
                print(f"✅ Success: {success}")
            else:
                fail += 1
                print(f"❌ Fail: {fail}")

        except Exception as e:
            fail += 1
            print(f"⚠️ Error: {fail}")

        time.sleep(random.uniform(1, 3))


# Start threads
print("🚀 Bot started...")

for _ in range(THREADS):
    t = threading.Thread(target=run)
    t.start()
