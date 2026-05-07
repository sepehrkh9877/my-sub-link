import os
import re
from datetime import datetime, timedelta
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# دریافت اطلاعات از Secrets
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
SOURCE_CHAT = '@Toxic_connection_bot' # حتما یوزرنیم منبع را اینجا چک کن

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def run():
    async with client:
        all_configs = []
        # اسکن پیام‌ها
        async for message in client.iter_messages(SOURCE_CHAT, limit=200):
            if message.text:
                for match in re.finditer(r'(vless|vmess|ss|trojan)://[^\s\n\r]+', message.text):
                    all_configs.append(match.group())
        
        # حذف تکراری‌ها و انتخاب ۶۰ تای اول
        unique_configs = list(dict.fromkeys(all_configs))
        final_list = unique_configs[:60]
        
        # --- بخش اضافه کردن ساعت (این همان بخشی است که در فایل تو کمه) ---
        tehran_time = datetime.utcnow() + timedelta(hours=3, minutes=30)
        now_str = tehran_time.strftime("%H:%M | %Y-%m-%d")
        
        # ساخت کانفیگ نمایشی ساعت
        time_marker = f"vless://ea7553a1-1b63-4511-93c6-6284f6760e7e@1.1.1.1:443?encryption=none&security=none&type=tcp#🕒_Last_Update:_{now_str}"
        
        # گذاشتن ساعت در اولین خط لیست
        final_list.insert(0, time_marker)
        
        # ذخیره در فایل (مطمئن شو نام فایل اینجا درست باشد)
        with open("sub_78721_config_13740_jbfnbk.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(final_list))

client.loop.run_until_complete(run())
