import telebot
import json
import os
from flask import Flask
from threading import Thread

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

# --- LOGIQUE DE CHARGEMENT DES DONNÉES ---
def load_data():
    file_name = 'catechisme.json' 
    if not os.path.exists(file_name):
        print(f"Erreur : Le fichier {file_name} est introuvable.")
        return {}
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)

try:
    data = load_data()
    print(f"Données chargées : {len(data)} questions trouvées.")
except Exception as e:
    print(f"Erreur lecture JSON : {e}")
    data = {}

# --- LOGIQUE DE RÉPONSE ---
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()
    chat_type = message.chat.type
    bot_username = "@CollinsOrthodoxe_bot"
    question_id = None

    if chat_type == 'private':
        if text.isdigit():
            question_id = text
    else:
        if text.startswith(bot_username):
            parts = text.split()
            if len(parts) > 1 and parts[1].isdigit():
                question_id = parts[1]

    if question_id:
        if question_id in data:
            q = data[question_id]["question"]
            r = data[question_id]["reponse"]
            
            clean_q = q
            if q.strip().startswith(f"{question_id}."):
                clean_q = q.split(".", 1)[-1].strip()
            
            response_text = f"<b>{question_id}. {clean_q}</b>\n\n{r}"
            bot.reply_to(message, response_text, parse_mode="HTML")
        else:
            bot.reply_to(message, "Désolé, cette question n'existe pas (choisissez entre 1 et 149).")

# --- LANCEMENT ---
if __name__ == "__main__":
    print("Nettoyage des anciens webhooks...")
    bot.remove_webhook() # <--- Force la bascule vers le nouveau serveur
    
    print("Démarrage du serveur Flask...")
    keep_alive()
    
    print("Le bot est en ligne...")
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Erreur polling : {e}")
