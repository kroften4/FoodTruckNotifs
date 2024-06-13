import json

import discord
from discord.ext import commands

TODO_TASKS = ('gather', 'research', 'cook', 'greenhouse', 'restock')
WELCOME_MESSAGE = "**Welcome <:Okayeg:1250520866861613056>! Set your preferences in /settings 🥚**\n"
SETUP_DATA = {
    "telegram_id": "unset",
    "settings": {
        "tg_notifs": "false",
        "dc_notifs": "true",
        "greenhouse": "true",
        "restock": "true"
    },
    "reminders": {}
}


def extract_todo_cds(inp: str, opt_out: list):
    out = {}
    inp = inp.split('========================')[1].split('\n')[1:]
    for line in inp:
        for term in TODO_TASKS:
            if term in line and term not in opt_out:
                cd = line.split()[-1][3:-3]
                out.update({term: cd})
    return out


class ExtractTodo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.message_command(
        name='Extract FT todo',
        description="Extract your /todo tasks and set notifications for telegram"
    )
    async def extract_todo(self, ctx, message):
        response = []

        with open("data/users.json", "r") as f_o:
            data_from_json = json.load(f_o)

        user_id = str(ctx.author.id)
        if user_id not in data_from_json:
            data_from_json[user_id] = SETUP_DATA
            response.append(WELCOME_MESSAGE)

        opt_out = []
        if not data_from_json[user_id]["settings"]["greenhouse"]:
            opt_out.append("greenhouse")
        if not data_from_json[user_id]["settings"]["restock"]:
            opt_out.append("restock")

        reminders = extract_todo_cds(message.content, opt_out=opt_out)
        data_from_json[user_id]["reminders"] = reminders

        with open("data/users.json", "w") as f_o:
            json.dump(data_from_json, f_o, indent=4)

        response.append(f"Set notifications for {user_id}:\n{repr(reminders)}")
        await ctx.respond('\n'.join(response), ephemeral=False)


def setup(bot):
    bot.add_cog(ExtractTodo(bot))
