import os
import re
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

SOURCE_CHAT = '@Toxic_connection_bot' # حتما یوزرنیم ربات خودت را بگذار

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def run():
    async with client:
        all_configs = []
        # خواندن پیام‌ها
        async for message in client.iter_messages(SOURCE_CHAT, limit=50):
            if message.text:
                # این Regex کلِ رشته‌هایی که با پروتکل‌ها شروع می‌شوند را تا اولین فاصله برمی‌دارد
                found = re.findall(r'(vless|vmess|ss|trojan)://[^\s\n\r]+', message.text)
                if found:
                    # اضافه کردن به لیست
                    for match in re.finditer(r'(vless|vmess|ss|trojan)://[^\s\n\r]+', message.text):
                        all_configs.append(match.group())
        
        # حذف تکراری‌ها
        unique_configs = list(dict.fromkeys(all_configs))
        
        # ذخیره در فایل
        with open("sub.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(unique_configs))

client.loop.run_until_complete(run())
