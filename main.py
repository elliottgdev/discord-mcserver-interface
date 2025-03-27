import discord
from discord.ext import commands
from discord import app_commands

import subprocess
import sys

class Client(commands.Bot):
    async def on_ready(self):
        print(f'Logged on as {self.user}.')

        try:
            guild = discord.Object(id=1179627891634470995)
            synced = await self.tree.sync(guild=guild)
            print(f'Synced {len(synced)} commands to guild {guild.id}')
        except Exception as e:
            print(f'Error: Failed to sync commands; ({e})')
    
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

#all minecraft server code runs here as to not hang the bot
class Server:
    def __init__(self):
        self.cmd = ["java", "-jar", server_jar, "nogui"]
        self.process = None
        self.logger = None
        
        self.log = open("server.log")
        self.log_line_count = len(self.log.readlines())

    def start_server(self):
        print('starting')
        self.process = subprocess.Popen(self.cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
        self.logger = subprocess.Popen(["python3", "server_log.py"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)

    def stop_server(self):
        self.process.communicate(bytes('stop'.encode()))
        self.logger.kill()

    def command(self, command):
        self.process.stdin.write(bytes(f'{command}\n'.encode()))
        self.process.stdin.flush()

intents = discord.Intents.default()
intents.message_content = True
client = Client(command_prefix = "!", intents=intents)

bot_config = {}
with open('botconf.txt') as file:
    bot_config = file.readlines()

api_key = bot_config[0].strip()
guild_id = discord.Object(int(bot_config[1].strip()))
channel = client.get_channel(int(bot_config[2].strip()))
server_jar = bot_config[3].strip()

#server the bot interacts with
server = Server()

#start server
@client.tree.command(name="start", description="Starts server.", guild=guild_id)
async def start_server(interaction: discord.Interaction):
    await interaction.response.send_message('<:minecraft:1353669586356015135> Starting server.')
    server.start_server()

#stop server / ping command
@client.tree.command(name="stop", description="Stops server.", guild=guild_id)
async def stop_running(interaction:discord.Interaction):
    await interaction.response.send_message('<:minecraft:1353669586356015135> Stopping server.')
    server.stop_server()

#command command
@client.tree.command(name="server_command", description="Sends server a command.", guild=guild_id)
async def command_input(interaction: discord.Interaction, param: str):
    await interaction.response.send_message('<:minecraft:1353669586356015135> Sending command to server.')
    server.command(param)

#move bot
@client.tree.command(name="move", description="Moves the bot to a different channel and/or server.", guild=guild_id)
async def command_input(interaction: discord.Interaction, new_guild: str, new_channel: str):
    await interaction.response.send_message('<:minecraft:1353669586356015135> Sending command to server.')
    bot_config[1] = f'{new_guild}\n'
    bot_config[2] = f'{new_channel}\n'
    with open('botconf.txt', 'w') as file:
        file.writelines(bot_config)

#kill bot
@client.tree.command(name="kill", description="Kills the bot. Please close server before killing the bot", guild=guild_id)
async def command_input(interaction: discord.Interaction):
    await interaction.response.send_message('<:minecraft:1353669586356015135> Goodnight.')
    sys.exit()

client.run(api_key)