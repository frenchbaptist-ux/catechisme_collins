import telebot
import json
import os

# Récupération du Token depuis les variables d'environnement Render
TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Chargement du fichier catechisme.json
def load_data():
    file_name = 'catechisme.json' 
    if not os.path.exists(file_name):
        print(f"Erreur : Le fichier {file_name} est introuvable.")
        return {}
    with open(file_name, 'r', encoding='utf-8') as f:
        return json.load(f)

# On charge les données une seule fois au lancement
try:
    data = load_data()
    print("Données du catéchisme chargées avec succès.")
except Exception as e:
    print(f"Erreur lors de la lecture du fichier JSON : {e}")
    data = {}

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()
    chat_type = message.chat.type
    bot_username = "@CollinsOrthodoxe_bot"
    question_id = None

    # 1. Logique de détection : Privé (chiffre seul) vs Groupe (@nom + chiffre)
    if chat_type == 'private':
        if text.isdigit():
            question_id = text
    else:
        if text.startswith(bot_username):
            parts = text.split()
            if len(parts) > 1 and parts[1].isdigit():
                question_id = parts[1]

    # 2. Formatage et envoi de la réponse
    if question_id:
        if question_id in data:
            q = data[question_id]["question"]
            r = data[question_id]["reponse"]
            
            # Nettoyage de la question pour éviter les doublons de numérotation
            clean_q = q
            if q.strip().startswith(f"{question_id}."):
                clean_q = q.split(".", 1)[-1].strip()
            elif q.strip().startswith(question_id):
                clean_q = q.split(question_id, 1)[-1].strip()

            # Construction du message selon ton format souhaité
            # {ID}. {Question} en gras
            # Double saut de ligne
            # Réponse : en gras suivi du texte
            response_text = f"<b>{question_id}. {clean_q}</b>\n\n<b>Réponse :</b>\n{r}"
            
            bot.reply_to(message, response_text, parse_mode="HTML")
        else:
            bot.reply_to(message, "Désolé, cette question n'existe pas (choisissez entre 1 et 149).")

# Lancement du bot avec gestion des erreurs de connexion (Conflict 409)
if __name__ == "__main__":
    print("Le bot est en ligne...")
    try:
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Le bot a rencontré une erreur : {e}")
