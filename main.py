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
        configs_7_days = []      # لیست مخصوص کانفیگ‌های ۷ روز اخیر
        all_unique_configs = []  # لیست کل کانفیگ‌های منحصربه‌فرد (جدیدترین‌ها)
        seen = set()             # برای جلوگیری از ورود کانفیگ تکراری
        
        # تعیین بازه زمانی ۷ روز اخیر (به صورت UTC)
        seven_days_ago = datetime.now(timezone.utc) - timedelta(days=7)
        
        print("در حال استخراج کانفیگ‌ها بر اساس منطق جدید (۷ روز یا حداقل ۷۰ کانفیگ)...")
        
        # اسکن پیام‌ها (تا سقف ۵۰۰ پیام برای اطمینان از پر شدن حد نصاب ۷۰ تایی)
        async for message in client.iter_messages(SOURCE_CHAT, limit=500):
            # شرط خروج: اگر از ۷ روز عقب‌تر رفته باشیم و حداقل ۷۰ کانفیگ پشتیبان هم پر شده باشد، توقف کن
            if message.date < seven_days_ago and len(all_unique_configs) >= 70:
                break
            
            if message.text:
                # استخراج لینک‌ها با استفاده از Regex خودت
                for match in re.finditer(r'(vless|vmess|ss|trojan)://[^\s\n\r]+', message.text):
                    config = match.group()
                    
                    # پاکسازی و بررسی تکراری نبودن (حل مشکل عدم نمایش در v2rayNG)
                    config_clean = config.strip()
                    if config_clean and config_clean not in seen:
                        seen.add(config_clean)
                        all_unique_configs.append(config_clean)
                        
                        # اگر پیام مربوط به ۷ روز اخیر بود، به لیست اصلی هم اضافه شود
                        if message.date >= seven_days_ago:
                            configs_7_days.append(config_clean)
        
        # منطق نهایی: انتخاب لیست بر اساس تعداد
        if len(configs_7_days) >= 70:
            final_list = configs_7_days
            print(f"موفقیت‌آمیز: تعداد {len(final_list)} کانفیگ مربوط به ۷ روز اخیر جمع‌آوری شد.")
        else:
            # انتخاب ۷۰ کانفیگ آخر از کل کانفیگ‌های منحصربه‌فرد پیدا شده
            final_list = all_unique_configs[:70]
            print(f"توجه: کانفیگ‌های ۷ روز اخیر کمتر از ۷۰ تا بود ({len(configs_7_days)} عدد). ۷۰ کانفیگ جدید جایگزین شد.")
        
        # محاسبه ساعت تهران برای نمایش در ساب‌لینک
        tehran_time = datetime.utcnow() + timedelta(hours=3, minutes=30)
        now_str = tehran_time.strftime("%H:%M | %Y-%m-%d")
        
        # ساخت کانفیگ نمایشی ساعت خودت
        time_marker = f"vless://ea7553a1-1b63-4511-93c6-6284f6760e7e@1.1.1.1:443?encryption=none&security=none&type=tcp#🕒_Last_Update:_{now_str}"
        
        # گذاشتن ساعت در اولین خط لیست
        final_list.insert(0, time_marker)
        
        # ذخیره در فایل مخصوص خودت
        with open("sub_78721_config_13740_jbfnbk.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(final_list))
            
        print(f"تعداد {len(final_list) - 1} کانفیگ با موفقیت در فایل مخصوص ذخیره شد.")

client.loop.run_until_complete(run())
