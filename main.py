import os
import re
from telethon.sync import TelegramClient
from telethon.sessions import StringSession

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# یوزرنیم ربات را اینجا دقیق وارد کن (حتماً با @)
SOURCE_CHAT = '@Toxic_connection_bot' 

client = TelegramClient(StringSession(SESSION_STRING), API_ID, API_HASH)

async def run():
    async with client:
        configs = []
        # خواندن ۵۰ پیام آخر
        async for message in client.iter_messages(SOURCE_CHAT, limit=50):
            if message.text:
                # استخراج لینک‌های vless, vmess, ss, trojan
                found = re.findall(r'(vless://|vmess://|ss://|trojan://)[^\s]+', message.text)
                configs.extend(found)
        
        unique_configs = list(dict.fromkeys(configs))
        with open("sub.txt", "w", encoding="utf-8") as f:
            f.write("\n".join(unique_configs))

client.loop.run_until_complete(run())
