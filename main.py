import requests
import random
import string
import time
import threading
from colorama import Fore, Style, init

init(autoreset=True)

# ===== CONFIG (EDIT THIS ONLY) =====
TARGET_REF = "eae05c144f"   # <-- PUT YOUR REF CODE
USE_PROXY = True            # True / False
THREADS = 5                 # 1–10 recommended

# ==================================

total_success = 0
lock = threading.Lock()

# ===== UI =====
def show_info():
    print(f"{Fore.CYAN}{Style.BRIGHT}" + "═"*60)
    print(f"{Fore.MAGENTA}{Style.BRIGHT}        ⚡ YURIKA AI WAITLIST BOT ⚡")
    print(f"{Fore.CYAN}{Style.BRIGHT}" + "═"*60)
    print(f"{Fore.WHITE}👑 Owner     : {Fore.YELLOW}CryptowithAryanog")
    print(f"{Fore.WHITE}📢 Telegram  : {Fore.GREEN}t.me/cryptowithAryanog")
    print(f"{Fore.CYAN}{Style.BRIGHT}" + "═"*60 + "\n")

# ===== FUNCTIONS =====
def generate_random_email():
    prefix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=random.randint(8, 12)))
    domains = ["@gmail.com", "@outlook.com", "@yahoo.com", "@icloud.com"]
    return f"{prefix}{random.choice(domains)}"

def load_proxies():
    try:
        with open("proxies.txt", "r") as f:
            return [line.strip() for line in f if line.strip()]
    except:
        return []

# ===== WORKER =====
def worker(proxy_list):
    global total_success

    url = "https://www.airdrop.works/api/waitlist"
    branches = ["educator", "builder", "creator", "scout", "diplomat"]

    while True:
        branch = random.choice(branches)
        email = generate_random_email()

        payload = {
            "email": email,
            "primaryBranch": branch,
            "referralCode": TARGET_REF
        }

        headers = {
            "Content-Type": "application/json",
            "User-Agent": f"Mozilla/5.0 Chrome/{random.randint(110,124)}.0.0.0",
            "Origin": "https://www.airdrop.works",
            "Referer": f"https://www.airdrop.works/?ref={TARGET_REF}"
        }

        current_proxy = None
        if USE_PROXY and proxy_list:
            p = random.choice(proxy_list)
            current_proxy = {
                "http": f"http://{p}",
                "https": f"http://{p}"
            }

        print(f"{Fore.BLUE}📦 Sending → {Fore.WHITE}{email} {Fore.BLUE}| {Fore.YELLOW}{branch.upper()}")

        try:
            res = requests.post(url, json=payload, headers=headers, proxies=current_proxy, timeout=12)

            if res.status_code == 200:
                data = res.json()
                with lock:
                    total_success += 1
                    print(f"{Fore.GREEN}✅ Success #{total_success} | Rank: {data.get('rank')}")

                time.sleep(random.uniform(0.5, 2.0))

            elif res.status_code == 429:
                print(f"{Fore.RED}🛑 Rate Limited → Cooling 20s...")
                time.sleep(20)

            else:
                print(f"{Fore.RED}❌ Failed [{res.status_code}]")
                time.sleep(3)

        except Exception as e:
            print(f"{Fore.RED}⚠️ Error: {e}")
            time.sleep(5)

# ===== MAIN =====
show_info()

proxy_list = load_proxies() if USE_PROXY else []

print(f"{Fore.GREEN}🚀 Starting {THREADS} Threads...\n")

threads = []

for i in range(THREADS):
    t = threading.Thread(target=worker, args=(proxy_list,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()
