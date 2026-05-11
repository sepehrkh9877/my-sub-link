import os
import re
import socket
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone # NEW: اضافه شدن timezone
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# دریافت اطلاعات از Secrets
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
SOURCE_CHAT = '@Toxic_connection_bot'

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

def is_config_alive(link):
    try:
        match = re.search(r'@([^:/]+):(\d+)', link)
        if not match:
            match = re.search(r'//([^:/]+):(\d+)', link)
        
        if match:
            host = match.group(1)
            port = int(match.group(2))
            with socket.create_connection((host, port), timeout=2):
                return link
    except:
        pass
    return None

async def run():
    async with client:
        all_configs = []
        
        # --- NEW: محاسبه تاریخ یک هفته قبل ---
        # چون زمان پیام‌های تلگرام با فرمت UTC است، ما هم از UTC استفاده می‌کنیم
        one_week_ago = datetime.now(timezone.utc) - timedelta(days=7)
        
        print("Scanning messages from the last 7 days...")
        
        # اسکن پیام‌ها (بدون محدودیت تعداد، فقط تا زمانی که به یک هفته پیش برسیم)
        async for message in client.iter_messages(SOURCE_CHAT):
            # اگر پیام قدیمی‌تر از یک هفته بود، حلقه را متوقف کن
            if message.date < one_week_ago:
                break
                
            if message.text:
                for match in re.finditer(r'(vless|vmess|ss|trojan)://[^\s\n\r]+', message.text):
                    all_configs.append(match.group())
        
        # حذف تکراری‌ها
        unique_configs = list(dict.fromkeys(all_configs))
        print(f"Total unique configs found in last 7 days: {len(unique_configs)}")

        # مرحله فیلتر کردن کانفیگ‌های سالم
        print(f"Testing health of configs...")
        active_configs = []
        with ThreadPoolExecutor(max_workers=20) as executor:
            results = executor.map(is_config_alive, unique_configs)
            for res in results:
                if res:
                    active_configs.append(res)
        
        print(f"Final active configs: {len(active_configs)}")
        
        # تهیه لیست نهایی (بدون محدودیت عدد ۶۰، تمام موارد سالم یک هفته اخیر)
        final_list = active_configs
        
        # اضافه کردن ساعت آپدیت
        tehran_time = datetime.utcnow() + timedelta(hours=3, minutes=30)
        now_str = tehran_time.strftime("%H:%M | %Y-%m-%d")
        
        time_marker = f"vless://ea7553a1-1b63-4511-93c6-6284f6760e7e@1.1.1.1:443?encryption=none&security=none&type=tcp#🕒_Last_Update:_{now_str}"
        final_list.insert(0, time_marker)
        
        # ذخیره در فایل
        with open("sub_78721_config_13740_jbfnbk.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(final_list))

client.loop.run_until_complete(run())
