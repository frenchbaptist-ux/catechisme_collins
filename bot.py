import telebot
import json
import os
from flask import Flask # <--- AJOUTÉ
from threading import Thread # <--- AJOUTÉ

# --- PARTIE FLASK POUR RENDER & UPTIMEROBOT ---
app = Flask('')

@app.route('/')
def home():
    return "Bot Catechisme en ligne !", 200

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ----------------------------------------------

# Récupération du Token
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# ... (Garde ton code load_data() et handle_message() ici, ils sont parfaits) ...

# Lancement du bot
if __name__ == "__main__":
    print("Démarrage du serveur Flask...")
    keep_alive() # <--- LANCE LE SERVEUR WEB
    
    print("Le bot est en ligne...")
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Le bot a rencontré une erreur : {e}")
