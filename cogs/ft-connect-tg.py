import json
import discord
from discord.ext import commands


class FTConnectTG(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='ft-connect-tg',
        description="Get bot's latency",
    )
    @discord.option(name='code', description='The code you recieved from telegram bot')
    async def ft_connect_tg(self, ctx, code):
        with open("data/users.json", "r") as f_o:
            users_data_from_json = json.load(f_o)
        dc_user_id = str(ctx.author.id)
        if dc_user_id not in users_data_from_json:
            await ctx.respond("You are not registered!")
            return

        with open("data/user_confirmation_codes.json", "r") as f_o:
            code_data_from_json: dict = json.load(f_o)
        if code not in code_data_from_json.values():
            await ctx.respond("You don't have a code or the code is invalid! "
                              "Recieve it from @FoodTruckNotifsBot on telegram via `/code`")
            return
        tg_user_id = list(code_data_from_json.keys())[list(code_data_from_json.values()).index(code)]

        users_data_from_json[dc_user_id]["telegram_id"] = tg_user_id
        with open("data/users.json", "w") as f_o:
            json.dump(users_data_from_json, f_o, indent=4)

        code_data_from_json.pop(tg_user_id)
        with open("data/user_confirmation_codes.json", "w") as f_o:
            json.dump(code_data_from_json, f_o, indent=4)

        await ctx.respond("Connected your telegram id to you!")


def setup(bot):
    bot.add_cog(FTConnectTG(bot))
