import os
import requests
from flask import Flask, request
from telegram import Update, Bot

def create_app():
    app = Flask(__name__)
    
    TOKEN = os.environ.get('BOT_TOKEN', '')
    bot = Bot(token=TOKEN)
    
    # Auto-set webhook (sync)
    railway_domain = os.environ.get('RAILWAY_PUBLIC_DOMAIN', '')
    if railway_domain and TOKEN:
        try:
            webhook_url = f"https://{railway_domain}/webhook"
            bot.set_webhook(webhook_url)
            print(f"Webhook set: {webhook_url}")
        except Exception as e:
            print(f"Webhook error: {e}")
    
    @app.route('/')
    def home():
        return {"status": "EIDOLON-77 GOLD BOT ONLINE", "timestamp": "2024"}
    
    @app.route('/webhook', methods=['POST'])
    def webhook():
        try:
            update = Update.de_json(request.get_json(), bot)
            
            if update.message:
                chat_id = update.message.chat_id
                text = update.message.text
                
                # Sync send_message (no async/await)
                if text == '/start':
                    bot.send_message(
                        chat_id, 
                        "🌟 *EIDOLON-77 GOLD BOT*\n\n"
                        "Command:\n"
                        "/analyze - Analisis XAUUSD\n"
                        "/price - Harga terkini\n"
                        "/help - Bantuan",
                        parse_mode='Markdown'
                    )
                
                elif text == '/analyze':
                    bot.send_message(
                        chat_id,
                        "📊 *ANALISIS XAUUSD*\n\n"
                        "💰 Price: `2034.50`\n"
                        "📈 Trend: *BULLISH*\n"
                        "🎯 RSI: 58.3 (Neutral)\n\n"
                        "AI Insight: Momentum positif.",
                        parse_mode='Markdown'
                    )
                
                elif text == '/price':
                    bot.send_message(
                        chat_id,
                        "💰 *XAUUSD*: `2034.50`",
                        parse_mode='Markdown'
                    )
                
                elif text == '/help':
                    bot.send_message(
                        chat_id,
                        "🤖 *BANTUAN*\n\nFREE: 5 analisis/hari\nPRO: Unlimited",
                        parse_mode='Markdown'
                    )
                
                else:
                    bot.send_message(chat_id, "❓ Ketik /help untuk bantuan.")
            
            return 'OK'
        except Exception as e:
            print(f"Error: {e}")
            return 'ERROR', 500
    
    return app
