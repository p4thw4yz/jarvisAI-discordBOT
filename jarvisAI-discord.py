import discord
import requests
import openai
from discord.ext import commands

DISCORD_TOKEN = "DISCORD_TOKEN"
INVERTER = "SOLAX_INVERTER_MODEL"
SOLAX_TOKENID = "SOLAX_API_TOKEN"
openai.api_key = "CHATGPT_API_TOKEN"

#--------------------------------FUNCTIONS---------------------------------#
def getSolar():
    inverter = requests.get("https://www.eu.solaxcloud.com:9443/proxy/api/getRealtimeInfo.do?tokenId="+SOLAX_TOKENID+"&sn="+INVERTER)
    json_data = inverter.json() ## convert get request to json
    data = json_data['result'] ## Extract results json from get data that was pulled
    return str(data['acpower'])

def getResponseGPT(prompt):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=128,
        n=1,
        stop=None,
        temperature=0.5,
    )
    return str(response.choices[0].text.strip())

#--------------------------------DISCORD_BOT---------------------------------#
intents = discord.Intents.all()
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('Hello'):
        response = ('Hello World!')

    elif ('/solar') in message.content:
        solar = getSolar()
        print(solar)
        response = (solar + ' Watts').strip()

    else:
        response = getResponseGPT(message.content)
        print(response)

    await message.channel.send(response)

client.run(DISCORD_TOKEN)