import discord
from ftplib import FTP

hostname = "" # Insert host name (url)
user = "" # Insert username
passwd = "" # Insert password

discordBotToken = "" # Insert discord token

whitelistLocation = "/path/to/file" # Insert location to file relative to the FTP working directory

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def addWhitelist(hash):
    try:
        ftp = FTP(hostname)
        ftp.login(user, passwd)
        
        temp = open("temp", "w")
        temp.write("\n" + hash)
        temp.close()

        temp = open("temp", "rb")
        ftp.storbinary("APPE " + whitelistLocation, temp, 1)
        temp.close()

        temp = open("temp", "w")
        temp.write("")
        temp.close()
        
        ftp.close()
        return True
    except:
        return False
    
    

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('.whitelist'):
        messageArgs = message.content.split(" ")
        if len(messageArgs) == 2:
            if addWhitelist(messageArgs[1]):
                await message.channel.send("Whitelisted!")
            else:
                await message.channel.send("An error occured.")

client.run(discordBotToken)