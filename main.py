import os
import re
from datetime import datetime, timedelta
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# مقادیر از Secrets خوانده می‌شوند
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
SOURCE_CHAT = '@Toxic_connection_bot' # یوزرنیم ربات منبع را اینجا بگذار

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def run():
    async with client:
        all_configs = []
        async for message in client.iter_messages(SOURCE_CHAT, limit=200):
            if message.text:
                # استخراج تمام لینک‌های کانفیگ
                for match in re.finditer(r'(vless|vmess|ss|trojan)://[^\s\n\r]+', message.text):
                    all_configs.append(match.group())
        
        # حذف تکراری‌ها و انتخاب ۶۰ مورد اول
        unique_configs = list(dict.fromkeys(all_configs))
        final_list = unique_configs[:60]
        
        # --- بخش جادویی: محاسبه زمان به وقت ایران ---
        # سرور گیت‌هاب به وقت UTC است، پس ۳:۳۰ ساعت اضافه می‌کنیم
        ir_time = datetime.utcnow() + timedelta(hours=3, minutes=30)
        timestamp = ir_time.strftime("%H:%M | %Y-%m-%d")
        
        # ساخت یک کانفیگ ظاهری برای نمایش زمان در اپلیکیشن
        info_config = f"vless://update-info@1.1.1.1:443?encryption=none&security=none#🕒_Last_Update:_{timestamp}"
        
        # اضافه کردن این پیام به ابتدای لیست
        final_list.insert(0, info_config)
        
        # ذخیره در فایل (دقت کن نام فایل با تنظیمات گیت‌هاب یکی باشد)
        with open("sub_78721_config_13740_jbdnbk.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(final_list))

client.loop.run_until_complete(run())
