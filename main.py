import os
import re
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

# تنظیمات
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")
SOURCE_CHAT = '@Toxic_connection_bot' # یوزرنیم ربات

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def run():
    async with client:
        all_configs = []
        
        # ۱. اسکن ۲۰۰ پیام آخر برای اطمینان از پیدا کردن حداقل ۶۰ کانفیگ
        async for message in client.iter_messages(SOURCE_CHAT, limit=200):
            if message.text:
                for match in re.finditer(r'(vless|vmess|ss|trojan)://[^\s\n\r]+', message.text):
                    all_configs.append(match.group())
        
        # ۲. حذف تکراری‌ها (خیلی مهم برای تمیزی لیست)
        unique_configs = list(dict.fromkeys(all_configs))
        
        # ۳. برش لیست: فقط ۶۰ تای اول را نگه دار (اگر کمتر از ۶۰ تا بود، کلش را نگه دار)
        final_list = unique_configs[:60]
        
        # ۴. ذخیره در فایل
        with open("sub_78721_config_13740_jbfnbk.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(final_list))

client.loop.run_until_complete(run())
