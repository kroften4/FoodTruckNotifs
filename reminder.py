import json
import time
import dotenv
import requests
import os


def run():
    dotenv.load_dotenv()
    tg_token = str(os.getenv("TG_TOKEN"))
    reminder_name_to_text = {
        "cook": "/cook\n\nYour dish is ready",
        "gather": "/gather\n\nTime to gather some ingredients",
        "research": "/research\n\nTime to research a recipe",
        "greenhouse": "/greenhouse\n\nYour plant is ready to be harvested",
        "restock": "/market /library /tree\n\nThe shops have been restocked"
    }

    while True:
        with open("data/users.json", "r") as f_o:
            data_from_json = json.load(f_o)
        for dc_user_id in data_from_json:
            user_reminders = data_from_json[dc_user_id]["reminders"]
            for reminder_name in user_reminders:
                if user_reminders[reminder_name] != "done" and int(user_reminders[reminder_name]) < int(time.time()):
                    remider_text = reminder_name_to_text[reminder_name]
                    tg_user_id = data_from_json[dc_user_id]["telegram_id"]
                    if tg_user_id != "unset":
                        requests.post(
                            f"https://api.telegram.org/bot{tg_token}/sendMessage?chat_id={tg_user_id}&text={remider_text}"
                        )
                    data_from_json[dc_user_id]["reminders"][reminder_name] = "done"

        with open("data/users.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4)
        time.sleep(60)


if __name__ == "__main__":
    run()
