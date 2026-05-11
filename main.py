import os
import re
from datetime import datetime, timedelta, timezone
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# دریافت اطلاعات از Secrets
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
SOURCE_CHAT = '@Toxic_connection_bot' 

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def run():
    async with client:
        all_configs = []
        
        # تعیین بازه زمانی ۵ روز اخیر (به صورت UTC برای هماهنگی با تلگرام)
        five_days_ago = datetime.now(timezone.utc) - timedelta(days=5)
        
        print("در حال استخراج کانفیگ‌های ۵ روز اخیر...")
        
        # اسکن پیام‌ها بدون محدودیت تعداد (تا زمانی که به ۵ روز پیش برسیم)
        async for message in client.iter_messages(SOURCE_CHAT):
            # اگر پیام قدیمی‌تر از ۵ روز بود، توقف کن
            if message.date < five_days_ago:
                break
            
            if message.text:
                # استخراج لینک‌ها با استفاده از Regex
                for match in re.finditer(r'(vless|vmess|ss|trojan)://[^\s\n\r]+', message.text):
                    all_configs.append(match.group())
        
        # حذف تکراری‌ها
        unique_configs = list(dict.fromkeys(all_configs))
        
        # لیست نهایی شامل تمام موارد ۵ روز اخیر است
        final_list = unique_configs
        
        # محاسبه ساعت تهران برای نمایش در ساب‌لینک
        tehran_time = datetime.utcnow() + timedelta(hours=3, minutes=30)
        now_str = tehran_time.strftime("%H:%M | %Y-%m-%d")
        
        # ساخت کانفیگ نمایشی ساعت
        time_marker = f"vless://ea7553a1-1b63-4511-93c6-6284f6760e7e@1.1.1.1:443?encryption=none&security=none&type=tcp#🕒_Last_Update:_{now_str}"
        
        # گذاشتن ساعت در اولین خط لیست
        final_list.insert(0, time_marker)
        
        # ذخیره در فایل
        with open("sub_78721_config_13740_jbfnbk.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(final_list))
            
        print(f"تعداد {len(final_list) - 1} کانفیگ با موفقیت ذخیره شد.")

client.loop.run_until_complete(run())
