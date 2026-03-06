import telebot
import json
import os

# Remplace par ton vrai Token
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Chargement du catéchisme
def load_data():
    with open('catechisme.json', 'r', encoding='utf-8') as f:
        return json.load(f)

data = load_data()

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()
    chat_type = message.chat.type  # 'private', 'group' ou 'supergroup'
    bot_username = "@CollinsOrthodoxe_bot"

    question_id = None

    if chat_type == 'private':
        # En privé : on accepte le chiffre direct
        if text.isdigit():
            question_id = text
    else:
        # En groupe : on vérifie si le message commence par l'arobase du bot
        if text.startswith(bot_username):
            # On extrait ce qui vient après l'arobase
            parts = text.split()
            if len(parts) > 1 and parts[1].isdigit():
                question_id = parts[1]

    # Si on a trouvé un ID valide, on cherche la réponse
    if question_id:
        if question_id in data:
            q = data[question_id]["question"]
            r = data[question_id]["reponse"]
            response_text = f"<b>Question {question_id} :</b>\n{q}\n\n<b>Réponse :</b>\n{r}"
            bot.reply_to(message, response_text, parse_mode="HTML")
        else:
            bot.reply_to(message, "Désolé, cette question n'existe pas (choisissez entre 1 et 149).")

print("Le bot est en ligne...")
bot.infinity_polling()
