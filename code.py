#import

import random
import discord
from discord.ext import commands
import openai
import requests

#another files for hide token
from config import TOKEN, open_aik, deep_aik





#intents
intents = discord.Intents.default()
intents.message_content = True
intents.presences = True
intents.members = True
intents.voice_states = True
intents.guilds = True
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)







@bot.command()
async def bonjour(ctx):
  await ctx.send(f"bonjour {ctx.author.name} !")


@bot.command(help="dit lui de fermer sa bouche",
             description="le bot vas lui dire de se taire")
async def chut(ctx):
  await ctx.send(f"chut!")


@bot.command()
async def pile(ctx):
  await ctx.send(random.choice(["pile", "face"]))

#met pret dans la commande
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}') 


#autre commande suite
@bot.command()
@commands.has_permissions(manage_messages=True) 
async def supp(ctx, amount: int): 
    if amount <= 1: 
      await ctx.send("Veuillez spécifier un nombre positif de messages à supprimer.") 
      return     
    else:
      deleted = await ctx.channel.purge(limit=amount + 1)
      await ctx.send(f'{len(deleted) - 1} messages supprimés.', delete_after=5)


@bot.command()
async def avatar(ctx, member: discord.Member = None):
  member = member or ctx.author 
  embed = discord.Embed(title=f"Avatar de {member}") 
  embed.set_image(url=member.display_avatar.url)  
  await ctx.send(embed=embed)





#pour openai
OPENAI_API_KEY = open_aik

openai.api_key = OPENAI_API_KEY

@bot.command()
async def generate_image(ctx, *, description):
  try:
    response = openai.Image.create(
      prompt=description,
      n=1,
      size="512x512"
    ) 
    image_url = response['data'][0]['url']
    embed = discord.Embed(title="Image générée")
    embed.set_image(url=image_url)
    await ctx.send(embed=embed) 
  except Exception as e: 
    await ctx.send(f"Erreur en générant l'image : {str(e)}")



@bot.command()
async def gpt(ctx, *, message):
  try:
    url = "https://api.openai.com/v1/chat/completions" 
    headers = {
      "Content-Type": "application/json",
      "Authorization": f"Bearer {OPENAI_API_KEY}" 
    }
    data = {
      "model": "gpt-4o-mini",
      "messages": [
        {"role": "user", "content": message} 
      ] 
    } 
    response = requests.post(url, headers=headers, json=data)
    response_data = response.json()
    bot_reply = response_data['choices'][0]['message']['content'] 
    
    await ctx.send(bot_reply)
  except Exception as e: 
    await ctx.send(f"Erreur :{str(e)}")


#pour copilot
#generateur d'image
DEEPAI_API_KEY = deep_aik

API_BASE_URL = 'https://api.deepai.org/api/alexouilledonuts' # URL de votre API

@bot.command()
async def image(ctx, *, description):
  try:
    response = requests.post(f'{API_BASE_URL}/generate_image', json={'description': description}) 
    data = response.json() 
    image_url = data.get('image_url') 
    if image_url: 
      embed = discord.Embed(title="Image générée")
      embed.set_image(url=image_url) 
      await ctx.send(embed=embed) 
    else:
      await ctx.send("Erreur : aucune image générée.") 
  except Exception as e:
    await ctx.send(f"Erreur : {str(e)}")






bot.run(TOKEN)
