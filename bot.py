import telebot
import json
import os
from flask import Flask
from threading import Thread

# 1. Configuration du Token
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 2. Mini-serveur Flask pour Render (Évite le mode veille)
app = Flask('')

@app.route('/')
def home():
    return "Bot Collins Orthodoxe est en ligne !"

def run_flask():
    # Render utilise la variable PORT
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 3. Logique du bot (Chargement de collins.json)
def load_data():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'collins.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@bot.message_handler(func=lambda message: True)
def handle_smart_response(message):
    if not message.text:
        return
    
    text = message.text.strip()
    # On définit le nom du bot pour les groupes
    bot_username = "@CollinsOrthodoxe_bot"
    is_private = message.chat.type == 'private'
    
    raw_num = ""

    # CAS A : En privé -> Chiffre pur (ex: "1")
    if is_private:
        raw_num = text.replace("/", "").strip()
    
    # CAS B : En groupe -> Mention obligatoire (ex: "@CollinsOrthodoxe_bot 1")
    elif bot_username in text:
        raw_num = text.replace(bot_username, "").replace("/", "").strip()
    
    # CAS C : En groupe sans mention -> Silence
    else:
        return

    # Envoi de la réponse si c'est un numéro valide
    if raw_num.isdigit():
        try:
            data = load_data()
            if raw_num in data:
                question = data[raw_num]["question"]
                reponse = data[raw_num]["reponse"]
                # Mise en forme
                texte_final = f"*{raw_num}. {question}*\n\n{reponse}"
                bot.send_message(message.chat.id, texte_final, parse_mode='Markdown')
        except Exception as e:
            print(f"Erreur lecture JSON : {e}")

# 4. Lancement simultané
if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    
    print("Démarrage du bot Collins Orthodoxe...")
    bot.infinity_polling()
