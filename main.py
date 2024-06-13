import threading
import subprocess
import sys


def run_script(script_name):
    subprocess.run([sys.executable, script_name])


if __name__ == "__main__":
    dc_bot_thread = threading.Thread(target=run_script, args=("dc_bot.py",))
    tg_bot_thread = threading.Thread(target=run_script, args=("tg_bot.py",))

    dc_bot_thread.start()
    tg_bot_thread.start()
    dc_bot_thread.join()
    tg_bot_thread.join()
