import json
import os
import dotenv
import telebot
import random


def generate_code(occupied_codes):
    code = str(random.randint(0, 99999)).zfill(5)
    if code not in occupied_codes:
        return code
    else:
        generate_code(occupied_codes)


def run():
    dotenv.load_dotenv()
    token = str(os.getenv("TG_TOKEN"))
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=['start', 'hello'])
    def start(message: telebot.types.Message):
        bot.reply_to(message, "Hi! Type /code to get the code for discord bot")

    @bot.message_handler(commands=['connect', 'code'])
    def start(message: telebot.types.Message):
        with open("data/user_confirmation_codes.json", "r") as f_o:
            data_from_json = json.load(f_o)
        code = generate_code(data_from_json.values())
        user_id = str(message.from_user.id)
        if user_id in data_from_json:
            bot.send_message(message.chat.id, "Updating your code...")
        data_from_json[user_id] = code
        with open("data/user_confirmation_codes.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4)
        # TODO: start a job which will remove the code from the database after a timeout
        bot.reply_to(
            message,
            f"Your code: `{code}`\n\nSend it to the discord bot via `/ft-connect-tg code: {code}`",
            parse_mode="MarkdownV2"
        )

    print(f"Logged in as {bot.user.username} on telegram")
    print("---------")
    bot.infinity_polling()


if __name__ == "__main__":
    run()
