import requests, asyncio, os
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import pytz

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID", "@fx_volumetrade")

bot = Bot(token=TOKEN)
beirut_tz = pytz.timezone('Asia/Beirut')

async def send_gold_price():
    try:
        r = requests.get("https://api.gold-api.com/price/XAU", timeout=10).json()
        price = float(r.get('price', 0))
        msg = f"💰 سعر الذهب الآن\n\nXAU/USD: ${price:.2f}\n\n📊 دعم: {price-15:.2f}\n📈 مقاومة: {price+15:.2f}"
        await bot.send_message(chat_id=CHANNEL_ID, text=msg)
    except Exception as e:
        print(e)

async def send_economic_news():
    msg = "🔥 أهم أخبار السوق اليوم\n\n🥇 الذهب: ترقب بيانات التضخم\n💵 الدولار: DXY حساس\n📅 15:30 CPI - 21:00 محضر الفيدرالي\n\n@fx_volumetrade"
    await bot.send_message(chat_id=CHANNEL_ID, text=msg)

async def market_open_alert(market):
    alerts = {
        "london": "🇬🇧 افتتح سوق لندن الآن - 10:00 صباحاً بتوقيت بيروت",
        "ny": "🇺🇸 افتتح سوق نيويورك الآن - 03:00 عصراً - أقوى وقت للذهب! 🔥",
        "sydney": "🇦🇺 افتتح سوق سيدني - 11:00 مساءً",
        "close": "🔒 أغلق سوق نيويورك - 12:00 ليلاً"
    }
    await bot.send_message(chat_id=CHANNEL_ID, text=alerts.get(market,""))

async def main():
    scheduler = AsyncIOScheduler(timezone=beirut_tz)
    scheduler.add_job(send_gold_price, 'interval', minutes=60)
    scheduler.add_job(send_economic_news, 'cron', hour=9, minute=0)
    scheduler.add_job(market_open_alert, 'cron', hour=23, minute=0, args=["sydney"])
    scheduler.add_job(market_open_alert, 'cron', hour=10, minute=0, args=["london"])
    scheduler.add_job(market_open_alert, 'cron', hour=15, minute=0, args=["ny"])
    scheduler.add_job(market_open_alert, 'cron', hour=0, minute=0, args=["close"])
    scheduler.start()
    await bot.send_message(chat_id=CHANNEL_ID, text="✅ تم تشغيل بوت fx_volumetrade بنجاح")
    while True:
        await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())
