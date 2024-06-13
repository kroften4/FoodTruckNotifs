import discord
from discord.ext import commands
import requests


def format_cooldowns(cooldowns: dict):
    result = ""
    for key, value in cooldowns.items():
        result += f"{key}: <t:{str(value)[:-3]}>\n"  # returns
    return result


class Zoo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name='zoo',
        description="Set/update zoo reminders (spam Colon's servers xdd)",
        guild_ids=[1112346351523594250, 854775827711393812]
    )
    async def zoo(self, ctx):
        await ctx.response.defer()
        url = f"https://gdcolon.com/zoo/api/profile/{ctx.author.id}"
        request = requests.get(url)
        response = request.json()
        if "error" in response:
            await ctx.respond(f"Error: {response['error']}")
            return
        if "API Key" not in response["equippedRelics"]:
            await ctx.respond("You don't have API key equipped! so bad...")
            return
        await ctx.respond(format_cooldowns(response["secretInfo"]["cooldowns"]))


def setup(bot):
    bot.add_cog(Zoo(bot))
