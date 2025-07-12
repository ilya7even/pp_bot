import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
from database import update_pp, get_top_users

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Бот запущен как {bot.user}")

@bot.command()
async def pp(ctx):
    change, length = update_pp(ctx.author.id, ctx.author.name)
    if change is None:
        await ctx.send(f"{ctx.author.mention}, ты уже проверял писю сегодня 😏. Сейчас она {length:.2f} см.")
    else:
        sign = "увеличилась" if change >= 0 else "уменьшилась"
        await ctx.send(f"{ctx.author.mention}, твоя писька {sign} на {abs(change):.2f} см. Текущий размер: {length:.2f} см.")

@bot.command()
async def top(ctx):
    top_list = get_top_users()
    msg = "**🏆 Топ писек сервера:**\n"
    for i, (username, length) in enumerate(top_list, start=1):
        msg += f"{i}. {username}: {length:.2f} см\n"
    await ctx.send(msg)

bot.run(TOKEN)
