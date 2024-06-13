import json

import discord
from discord.ext import commands


def format_settings(d: dict):
    result = []
    for key in d:
        result.append(f"**{key}**: {d[key]}")
    return '\n'.join(result)


class FTSettings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    class SettingsSelect(discord.ui.View):
        @discord.ui.select(
            placeholder="Choose an option...",
            options=[
                discord.SelectOption(
                    emoji="💙",
                    label="tg_notifs"
                ),
                discord.SelectOption(
                    emoji="🎮",
                    label="dc_notifs"
                ),
                discord.SelectOption(
                    emoji="🍃",
                    label="greenhouse"
                ),
                discord.SelectOption(
                    emoji="🛒",
                    label="restock"
                )
            ]
        )
        async def button_callback(self, select, interaction):
            match select.values[0]:
                case "tg_notifs":
                    user_id = str(interaction.user.id)
                    with open("data/users.json", "r") as f_o:
                        data_from_json = json.load(f_o)
                    df = data_from_json[user_id]
                    if df["telegram_id"] == "unset":
                        await interaction.response.send_message("You don't have a connected telegram account!\n"
                                                                "Send @... /start and follow the instructions")
                        return

                    await interaction.response.send_message("should switch tg_notifs option")

    @discord.slash_command(
        name="ft-settings",
        description="Settings for Food Truck related stuff",
        guild_ids=[1112346351523594250, 854775827711393812]
    )
    async def ft_settings(self, ctx):
        with open("data/users.json", "r") as f_o:
            data_from_json = json.load(f_o)
        user_id = str(ctx.author.id)
        if user_id not in data_from_json:
            await ctx.respond("You are not registered <:Okayeg:1250520866861613056>!")
            return
        df = data_from_json[user_id]
        view = self.SettingsSelect()
        await ctx.respond("**Settings**:\n"
                          f"{format_settings(df['settings'])}", view=view)


def setup(bot):
    bot.add_cog(FTSettings(bot))
