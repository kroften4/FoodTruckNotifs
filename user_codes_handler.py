import json
import time


def run():
    while True:
        with open("data/user_confirmation_codes.json", "r") as f_o:
            data_from_json: dict = json.load(f_o)
        data_updated = data_from_json.copy()
        for tg_user_id in data_from_json:
            timeout = data_from_json[tg_user_id]["timeout"]
            if timeout != "done" and timeout < time.time():
                data_updated.pop(tg_user_id)

        with open("data/user_confirmation_codes.json", "w") as f_o:
            json.dump(data_updated, f_o, indent=4)
        time.sleep(60)


if __name__ == "__main__":
    run()
