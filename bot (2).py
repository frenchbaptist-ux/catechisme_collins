import telebot
import json
import os
from flask import Flask
from threading import Thread

# 1. Configuration du Token
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# 2. Mini-serveur Flask pour Render
app = Flask('')

@app.route('/')
def home():
    return "Bot Keach est en ligne !"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

# 3. Logique du bot
def load_data():
    base_path = os.path.dirname(__file__)
    file_path = os.path.join(base_path, 'keach.json')
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

@bot.message_handler(func=lambda message: True)
def handle_mention(message):
    if not message.text:
        return
    
    text = message.text.strip()
    bot_username = "@Keach_bot"
    
    # On vérifie si le bot est mentionné
    if bot_username in text:
        # On extrait le numéro (ex: "@Keach_bot 1" -> "1")
        # On enlève aussi les éventuels "/"
        raw_num = text.replace(bot_username, "").replace("/", "").strip()
        
        if raw_num.isdigit():
            try:
                data = load_data()
                if raw_num in data:
                    question = data[raw_num]["question"]
                    reponse = data[raw_num]["reponse"]
                    texte_final = f"*{raw_num}. {question}*\n\n{reponse}"
                    bot.send_message(message.chat.id, texte_final, parse_mode='Markdown')
            except Exception as e:
                print(f"Erreur : {e}")

# 4. Lancement
if __name__ == "__main__":
    t = Thread(target=run_flask)
    t.start()
    
    print("Bot Keach prêt pour les mentions !")
    bot.infinity_polling()
