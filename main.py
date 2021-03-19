import discord
import json
import time
import random
from discord.ext import commands
from discord.ext .commands import has_permissions
from discord.utils import get
from discord import Game, Intents

intents=Intents.default()
intents.members=True

client = commands.Bot(command_prefix='$', intents=intents)
client.remove_command("help")

@client.command()
async def bal(ctx):
  open_account(ctx.author)
  user=ctx.author
  with open("bank.json", "r") as file:
    users = json.load(file)

  quantidade = users[str(user.id)]["carteira"]

  embed=discord.Embed(title=f"{user.name}")
  embed.add_field(name = "carteira", value = quantidade)

  await ctx.send(embed=embed)

def open_account(user: discord.Member):
  with open("bank.json", "r") as file:
    users = json.load(file)
  
  if str(user.id) in users:
    return False
  else:
    users[str(user.id)] = {}
    users[str(user.id)]["carteira"] = 100.0

  with open("bank.json", "w") as file:
    json.dump(users, file)
  return True

@client.command()
@commands.has_permissions(administrator=True)
async def baladd(ctx, user: discord.Member, money):
  with open("bank.json", "r") as file:
    users = json.load(file)
  if str(user.id) in users:
    fmoney = float(money)
    quantidade = users[str(user.id)]["carteira"]
    users[str(user.id)]["carteira"] = fmoney + quantidade
    await ctx.send(f"Dinheiro addicionada a conta de {user.name}.")
  else:
    ctx.send("Este usuario não tem uma conta.")


  with open("bank.json", "w") as file:
    json.dump(users, file)

@client.command()
@commands.has_permissions(administrator=True)
async def balreset(ctx, user: discord.Member):
  with open("bank.json", "r") as file:
    users = json.load(file)
  if str(user.id) in users:
    users[str(user.id)]["carteira"] = 100.0
    with open("bank.json", "w") as file:
      json.dump(users, file)
    await ctx.send(f"$bal Resetado.\nNome: {user.name}\nID: {user.id}")
  else:
    await ctx.send("Esse usuario não tem uma conta.")

@client.command()
async def pay(ctx, user: discord.Member, money):
  author=ctx.author
  with open("bank.json", "r") as file:
    users=json.load(file)
  fmoney=float(money)
  if str(author.id) in users:
    if str(user.id) in users:
      if users[str(author.id)]["carteira"] > fmoney:
        quantidade=users[str(author.id)]["carteira"]
        quantidade_a = users[str(user.id)]["carteira"]
        users[str(author.id)]["carteira"] = quantidade - fmoney
        users[str(user.id)]["carteira"] = quantidade_a + fmoney 
        with open("bank.json", "w") as file:
          json.dump(users, file)
        await ctx.send(f"{money}, mandado para {user.name}!")
      else:
        await ctx.send("Você não tem o dinheiro suficiente para isso.") 
    else:
      await ctx.send(f"{user.name}, não tem uma carteira.")
  else:
    await ctx.send(f"Você não tem uma carteira.") 

client.run(token)