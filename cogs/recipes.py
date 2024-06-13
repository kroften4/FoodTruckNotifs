import discord
from discord.ext import commands
import pandas as pd

# TODO: add specific error handling for this cog
# TODO: check which recipes does user have and based on that evaluate which price will he get for each dish

# LINK = "https://docs.google.com/spreadsheets/d/1-UQCO94V4tZrGYcVZRdwqiltO3Kbk1lGiFX0b8kidwk/edit#gid=0"
SHEET_ID = "1-UQCO94V4tZrGYcVZRdwqiltO3Kbk1lGiFX0b8kidwk"
RECIPES_LEVELS_IN_ORDER = [
    "Exotic",
    "Tier 3",
    "Tier 2",
    "Tier 1",
    "Basic",
    "Secret",
    "Unknown"
]
WORDS_IN_RECIPES_NOT_TO_CAPITALISE = ['with']


def tuple_to_dict(ings: tuple):
    d = {}
    for ing in ings:
        if str(ing) == 'nan':
            continue
        if ing not in d:
            d[ing] = 0
        d[ing] += 1
    return d


def message_to_ingredients(message: str):
    user_ingredients = {}
    request = message.split('\n')
    for line in request:
        # dishes have a price assigned to them: :grey_heart: :bacon: Bacon [40 :dollar: ]
        if ':dollar:' in line or '💵' in line:
            try:
                ingredient = capitalize(' '.join(line.split()[2:-3]))
            except Exception:
                raise Exception(f"Can't get dish name from line <{line}>")
            if '*' in ingredient:
                ingredient = ''.join([symbol for symbol in ingredient if symbol != '*'])
            if ingredient not in user_ingredients:
                user_ingredients[ingredient] = 0
            user_ingredients[ingredient] += 1
        else:
            try:
                ingredient = capitalize(' '.join(line.split()[1:-1]))  # :oliveoil: Olive Oil ×10 -> Olive Oil
            except Exception:
                raise Exception(f"Can't get ingredient name from line <{line}>")
            if '*' in ingredient:
                ingredient = ''.join([symbol for symbol in ingredient if symbol != '*'])
            try:
                amount = int(line.split()[-1][1:])  # :oliveoil: Olive Oil ×10 -> 10
            except Exception:
                raise Exception(f"Can't get ingredient amount from line <{line}>")
            if ingredient not in user_ingredients:
                user_ingredients[ingredient] = 0
            user_ingredients[ingredient] += amount
    return user_ingredients


def ingredients_dict_to_str(ingredients_dict: dict):
    res = (f"{key} x{value}" for key, value in ingredients_dict.items())
    return ', '.join(res)


def capitalize(s: str):
    s = s.split()
    for i, word in enumerate(s):
        if word.lower() in WORDS_IN_RECIPES_NOT_TO_CAPITALISE:
            s[i] = word.lower()
        elif len(word) > 1:
            s[i] = word[0].upper() + word[1:].lower()
        else:
            s[i] = word.upper()
    return ' '.join(s)


class Recipes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.message_command(
        name='Extract recipes',
        description="Print out what you can cook with your ingredients",
        guild_ids=[1112346351523594250, 854775827711393812]
    )
    async def recipes(self, ctx, message):
        await ctx.defer()
        # extract ingredients from the message
        user_ingredients = message_to_ingredients(message.content)

        # get recipes data
        dataframe = pd.read_csv(f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv")
        # TODO: might add tags for each dish soon
        recipes = {}
        for _, name, rarity, *recipe_ingredients in dataframe.itertuples():
            if str(rarity) == "nan":
                rarity = "Unknown"
            recipes[name] = {"rarity": rarity, "ingredients": tuple_to_dict(recipe_ingredients)}

        # collect awailable recipes and sort by rarity
        awailable_recipes = {}
        for name in recipes:
            can_cook = True
            for ingredient, required_amount in recipes[name]["ingredients"].items():
                if ingredient.lower() in map(lambda x: x.lower(), user_ingredients):
                    # TODO: might get an error here. Store recipes in lower and capitalise when needed to display
                    if user_ingredients[capitalize(ingredient)] < required_amount:
                        can_cook = False
                        break
                else:
                    can_cook = False
                    break
            if can_cook and recipes[name]["ingredients"]:
                awailable_recipes[name] = recipes[name]
        awailable_recipes_names_in_order = sorted(
            awailable_recipes.keys(),
            key=lambda key: RECIPES_LEVELS_IN_ORDER.index(awailable_recipes[key]["rarity"])
        )

        # build response message
        content = ""
        for name in awailable_recipes_names_in_order:
            if recipes[name]["rarity"] == "Secret":
                content += (f"||**{name}** ({recipes[name]['rarity']}): "
                            f"{ingredients_dict_to_str(recipes[name]['ingredients'])}||\n")
            else:
                content += (f"**{name}** ({recipes[name]['rarity']}): "
                            f"{ingredients_dict_to_str(recipes[name]['ingredients'])}\n")
        if not content:
            content = "Nothing! You're either broke or sent an invalid message\n"
        content = ("**Apparently you can cook:**\n" + content +
                   "\n*Note that this response was based only on the recipes that "
                   "I've seen and collected in my Google Sheet*")
        await ctx.respond(content)


def setup(bot):
    bot.add_cog(Recipes(bot))
