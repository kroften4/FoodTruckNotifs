import os
import discord
import logging
import dotenv
from discord.ext import commands


def run():
    logger = logging.getLogger('discord')
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
    logger.addHandler(handler)
    # logging.basicConfig(filemode='w', filename='discord.log', level=logging.DEBUG, encoding='utf-8')

    dotenv.load_dotenv()
    token = str(os.getenv("DC_TOKEN"))

    activity = discord.Activity(type=discord.ActivityType.playing, name="currently in developing")
    bot = discord.Bot(
        intents=discord.Intents.all(),
        activity=activity, status=discord.Status.online,
        debug_guilds=[1112346351523594250, 854775827711393812]
    )

    cogs_list = [
        # 'zoo',
        'ping',
        # 'recipes',
        'extract-todo',
        'ft_settings',
        'ft-connect-tg'
    ]
    for cog in cogs_list:
        bot.load_extension(f'cogs.{cog}')

    @bot.event
    async def on_ready():
        print(f"Logged in as {bot.user} on discord")
        print("---------")

    @bot.event
    async def on_application_command_error(ctx: discord.ApplicationContext, error: discord.DiscordException):
        if isinstance(error, commands.MissingPermissions):
            await ctx.respond(content="You are missing permissions required to run this command", ephemeral=True)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.respond("I am missing permissions required to run this command", ephemeral=True)
        elif str(error.original) == '403 Forbidden (error code: 50013): Missing Permissions':
            await ctx.respond("I am missing permissions required to run this command (Forbidden)", ephemeral=True)
        elif str(error.original) == '400 Bad Request (error code: 50035): Invalid Form Body\n' \
                                    'In content: Must be 2000 or fewer in length.':
            await ctx.respond("Error: Message length must be 2000 symbols or fewer", ephemeral=True)
        else:
            await ctx.respond(f"An error occured:\n```{error.original}```", ephemeral=True)
            # await ctx.respond("An unexpected error occurred. The necessary information has been sent to the developer",
            #                   ephemeral=True)
            raise error

    bot.run(token)


if __name__ == "__main__":
    run()
