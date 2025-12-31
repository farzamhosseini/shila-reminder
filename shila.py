import telebot
import time
from datetime import datetime, timedelta
import threading
import os

# ================== تنظیمات بات ==================
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = "-1002656121261"  # اینجا Chat ID گروهت رو بذار
IMAGE_PATH = "reminder_image.jpg"  # مسیر عکس

# تاریخ هدف (فرمت: سال، ماه، روز، ساعت، دقیقه)
TARGET_DATE = datetime(2026, 1, 25, 19, 30)  # مثال: 25 ژانویه 2026 ساعت 19:30

# اینتروال ارسال پیام
# می‌تونی از این فرمت‌ها استفاده کنی:
# برای ساعت: hours=1, hours=2, hours=6, ...
# برای روز: days=1, days=2, days=7, ...
# برای دقیقه: minutes=30, minutes=45, ...
INTERVAL = timedelta(minutes=1)  # هر 30 دقیقه یکبار

# ================================================

bot = telebot.TeleBot(BOT_TOKEN)


def calculate_time_remaining():
    """محاسبه زمان باقی‌مانده تا تاریخ هدف"""
    now = datetime.now()
    remaining = TARGET_DATE - now
    
    if remaining.total_seconds() <= 0:
        return "زمان هدف گذشته است! 🎉"
    
    days = remaining.days
    hours, remainder = divmod(remaining.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    # فرمت پیام
    message = f"داش ناموسن {days} روز و {hours} ساعت و {minutes} دقیقه مونده تا این سکس رو دوباره بکنیم 😭💔"
    
    return message


def send_reminder():
    """ارسال یادآوری به گروه"""
    try:
        caption = calculate_time_remaining()
        
        with open(IMAGE_PATH, 'rb') as photo:
            bot.send_photo(
                chat_id=CHAT_ID,
                photo=photo,
                caption=caption
            )
        
        current_time = datetime.now()
        print(f"✅ پیام ارسال شد: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"   محتوا: {caption}")
        
    except FileNotFoundError:
        print(f"❌ خطا: فایل عکس پیدا نشد: {IMAGE_PATH}")
    except Exception as e:
        print(f"❌ خطا در ارسال پیام: {e}")


def schedule_loop():
    """حلقه زمان‌بندی"""
    # ارسال اولین پیام
    send_reminder()
    
    # حلقه اصلی
    while True:
        # صبر کردن به اندازه interval
        time.sleep(INTERVAL.total_seconds())
        # ارسال پیام بعدی
        send_reminder()


def main():
    """شروع بات"""
    print("🤖 بات یادآوری تلگرام راه‌اندازی شد!")
    print(f"📅 تاریخ هدف: {TARGET_DATE.strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"⏱️  فاصله ارسال: {INTERVAL}")
    print(f"👥 گروه هدف: {CHAT_ID}")
    print(f"🖼️  مسیر عکس: {IMAGE_PATH}")
    print("-" * 50)
    
    # اجرای زمان‌بندی در یک thread جداگانه
    reminder_thread = threading.Thread(target=schedule_loop, daemon=True)
    reminder_thread.start()
    
    # نگه داشتن برنامه
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 بات متوقف شد.")


if __name__ == "__main__":
    main()
