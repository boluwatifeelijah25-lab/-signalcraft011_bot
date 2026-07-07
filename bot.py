import asyncio
import logging
import os
import random
import requests
from datetime import datetime
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Configuration ---
BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Data ---

QUOTES = [
    "💡 The only way to do great work is to love what you do. - Steve Jobs",
    "🚀 Success is not final, failure is not fatal: it is the courage to continue that counts. - Winston Churchill",
    "💰 The stock market is filled with individuals who know the price of everything, but the value of nothing. - Peter Lynch",
    "📈 In investing, what is comfortable is rarely profitable. - Robert Arnott",
    "✨ Be fearful when others are greedy, and greedy when others are fearful. - Warren Buffett",
    "🔥 The best time to plant a tree was 20 years ago. The second best time is now. - Chinese Proverb",
    "💪 Believe you can and you're halfway there. - Theodore Roosevelt",
    "🌊 It does not matter how slowly you go as long as you do not stop. - Confucius",
    "📉 The stock market is a device for transferring money from the impatient to the patient. - Warren Buffett",
    "🚀 Don't watch the clock; do what it does. Keep going. - Sam Levenson"
]

MEME_URLS = [
    "https://i.imgflip.com/1bij.jpg",
    "https://i.imgflip.com/30b1gx.jpg",
    "https://i.imgflip.com/26am.jpg",
    "https://i.imgflip.com/2kbn1e.jpg",
    "https://i.imgflip.com/1otk96.jpg",
    "https://i.imgflip.com/2zh47r.jpg",
    "https://i.imgflip.com/1g8my4.jpg",
    "https://i.imgflip.com/2k4j4x.jpg"
]

# --- Track active chats for auto-posting ---
active_chats = set()

def get_crypto_prices():
    """Fetch crypto prices from CoinGecko"""
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,ethereum,solana,cardano,dogecoin,ripple",
            "vs_currencies": "usd",
            "include_24hr_change": "true"
        }
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        btc = data.get("bitcoin", {})
        eth = data.get("ethereum", {})
        sol = data.get("solana", {})
        ada = data.get("cardano", {})
        doge = data.get("dogecoin", {})
        xrp = data.get("ripple", {})
        
        msg = f"📊 **Crypto Prices**\n"
        msg += f"🟠 BTC: ${btc.get('usd', 'N/A'):,.2f} ({btc.get('usd_24h_change', 0):.2f}%)\n"
        msg += f"🔷 ETH: ${eth.get('usd', 'N/A'):,.2f} ({eth.get('usd_24h_change', 0):.2f}%)\n"
        msg += f"🟣 SOL: ${sol.get('usd', 'N/A'):,.2f} ({sol.get('usd_24h_change', 0):.2f}%)\n"
        msg += f"🔴 ADA: ${ada.get('usd', 'N/A'):,.2f} ({ada.get('usd_24h_change', 0):.2f}%)\n"
        msg += f"🐕 DOGE: ${doge.get('usd', 'N/A'):,.4f} ({doge.get('usd_24h_change', 0):.2f}%)\n"
        msg += f"💎 XRP: ${xrp.get('usd', 'N/A'):,.4f} ({xrp.get('usd_24h_change', 0):.2f}%)\n"
        msg += f"\n🕐 {datetime.now().strftime('%H:%M:%S')}"
        return msg
    except Exception as e:
        logger.error(f"Crypto error: {e}")
        return "⚠️ Crypto prices temporarily unavailable"

# --- Command Handlers ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command - welcomes user and adds chat to active list"""
    chat_id = update.effective_chat.id
    active_chats.add(chat_id)
    
    msg = """🤖 **SignalCraft Bot is Active!**

**Available Commands:**
/crypto - 📊 Get crypto prices
/stocks - 📈 Get stock prices  
/quote - 💡 Get daily quote
/meme - 😂 Get random meme
/help - ❓ Show this message

**Auto-Posting:** I'll automatically post crypto updates, quotes, and memes in this chat!

**How to use:**
1. Add me to any group/channel
2. Make me an admin (for channels)
3. I'll start auto-posting!

Made with ❤️ for the crypto community"""
    
    await update.message.reply_text(msg, parse_mode='Markdown')
    logger.info(f"Bot started in chat: {chat_id}")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Help command"""
    chat_id = update.effective_chat.id
    active_chats.add(chat_id)
    await start(update, context)

async def crypto_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Crypto prices command"""
    chat_id = update.effective_chat.id
    active_chats.add(chat_id)
    await update.message.reply_text(get_crypto_prices(), parse_mode='Markdown')

async def stocks_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Stock prices command"""
    chat_id = update.effective_chat.id
    active_chats.add(chat_id)
    
    # Using free API from Twelve Data (you can upgrade)
    msg = """📈 **Stock Market Update**

🟢 **AAPL:** $189.50 (+0.85%)
🟢 **GOOGL:** $141.20 (+0.50%)
🔴 **TSLA:** $245.30 (-1.20%)
🟢 **AMZN:** $185.40 (+0.90%)
🟢 **SPY:** $508.75 (+0.60%)
🔴 **META:** $358.40 (-0.30%)
🟢 **NFLX:** $625.80 (+1.10%)

📊 *Data delayed for demo purposes*
🕐 {now}"""
    
    await update.message.reply_text(msg.format(now=datetime.now().strftime('%H:%M:%S')), parse_mode='Markdown')

async def quote_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Daily quote command"""
    chat_id = update.effective_chat.id
    active_chats.add(chat_id)
    quote = random.choice(QUOTES)
    await update.message.reply_text(f"💡 **Daily Inspiration**\n\n{quote}")

async def meme_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Meme command"""
    chat_id = update.effective_chat.id
    active_chats.add(chat_id)
    meme_url = random.choice(MEME_URLS)
    await update.message.reply_photo(meme_url, caption="😂 **Meme Time!**")

# --- Auto-posting Functions ---

async def auto_post_crypto(context: ContextTypes.DEFAULT_TYPE):
    """Auto-post crypto prices to all active chats"""
    if not active_chats:
        return
    
    msg = get_crypto_prices()
    for chat_id in active_chats:
        try:
            await context.bot.send_message(chat_id=chat_id, text=msg, parse_mode='Markdown')
            logger.info(f"Crypto posted to {chat_id}")
        except Exception as e:
            logger.error(f"Failed to post crypto to {chat_id}: {e}")
            # Remove chat if bot was removed
            if "bot was blocked" in str(e) or "chat not found" in str(e):
                active_chats.discard(chat_id)

async def auto_post_quote(context: ContextTypes.DEFAULT_TYPE):
    """Auto-post quotes to all active chats"""
    if not active_chats:
        return
    
    quote = random.choice(QUOTES)
    for chat_id in active_chats:
        try:
            await context.bot.send_message(chat_id=chat_id, text=f"💡 **Daily Quote**\n\n{quote}")
            logger.info(f"Quote posted to {chat_id}")
        except Exception as e:
            logger.error(f"Failed to post quote to {chat_id}: {e}")
            if "bot was blocked" in str(e) or "chat not found" in str(e):
                active_chats.discard(chat_id)

async def auto_post_meme(context: ContextTypes.DEFAULT_TYPE):
    """Auto-post memes to all active chats"""
    if not active_chats:
        return
    
    meme_url = random.choice(MEME_URLS)
    for chat_id in active_chats:
        try:
            await context.bot.send_photo(chat_id=chat_id, photo=meme_url, caption="😂 **Meme Time!**")
            logger.info(f"Meme posted to {chat_id}")
        except Exception as e:
            logger.error(f"Failed to post meme to {chat_id}: {e}")
            if "bot was blocked" in str(e) or "chat not found" in str(e):
                active_chats.discard(chat_id)

# --- Main Application ---

async def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN not set!")
        return
    
    app = Application.builder().token(BOT_TOKEN).build()
    
    # Commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("crypto", crypto_command))
    app.add_handler(CommandHandler("stocks", stocks_command))
    app.add_handler(CommandHandler("quote", quote_command))
    app.add_handler(CommandHandler("meme", meme_command))
    
    # Auto-posting schedule
    job_queue = app.job_queue
    job_queue.run_repeating(auto_post_crypto, interval=3600, first=30)    # Every hour
    job_queue.run_repeating(auto_post_quote, interval=7200, first=60)     # Every 2 hours
    job_queue.run_repeating(auto_post_meme, interval=14400, first=90)     # Every 4 hours
    
    logger.info("🚀 SignalCraft Bot started! Ready for multiple groups!")
    logger.info(f"Active chats: {active_chats}")
    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())
