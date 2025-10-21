from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Olá! Envia /predict para receber a previsão de jogo.")

async def predict(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Aqui vais ligar à tua API (exemplo placeholder)
    await update.message.reply_text("⚽ Probabilidade de golo: 74%\n📈 Over 2.5: 61%\n🤝 BTTS: 68%")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("predict", predict))

print("✅ Bot Telegram on-demand está ativo...")
app.run_polling()
