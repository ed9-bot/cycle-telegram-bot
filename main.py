import os
from datetime import date
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

TOKEN = os.environ.get("BOT_TOKEN")

user_state = {
    "period_start": None,
    "period_day": None
}

def today_stage():
    if not user_state["period_start"]:
        return "אין לי עדיין מידע. כתבי לי 'התחיל לי מחזור' 🌱"

    days = (date.today() - user_state["period_start"]).days + 1

    if days <= 6:
        return f"🩸 יום {days} לווסת. שקט, ניקוי, תנועה עדינה."
    elif days <= 10:
        return "🌱 אחרי וסת. אנרגיה עולה, זמן לבנות דברים."
    elif days <= 13:
        return "🔥 סביב ביוץ. ביטחון, תקשורת, יוזמה."
    elif days <= 18:
        return "🌫️ לוטאלי מוקדם. דיוק, עריכה, פחות עומס."
    else:
        return "⚠️ יום רגיש. לא לקבל החלטות גדולות. זה הורמונלי, לא אמת."

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()

    if "התחיל" in text:
        user_state["period_start"] = date.today()
        await update.message.reply_text("קיבלתי 🌸 יום 1 נרשם.")
        return

    if "יום" in text:
        try:
            num = int(''.join(filter(str.isdigit, text)))
            user_state["period_start"] = date.today().replace(day=date.today().day - (num - 1))
            await update.message.reply_text(f"עודכן ✔️ יום {num} לווסת.")
            return
        except:
            pass

    if "נגמר" in text:
        await update.message.reply_text("סגור ✔️ עוברים לשלב הבא.")
        return

    if "מה אני היום" in text:
        await update.message.reply_text(today_stage())
        return

    await update.message.reply_text("אני כאן 🌙 כתבי 'מה אני היום?'")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
app.run_polling()
