import discord
from discord.ext import commands
from discord import app_commands

import subprocess
import asyncio
import multiprocessing
import io

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
        self.cmd = ["java", "-jar", "server/server.jar", "nogui"]
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

#test server
guild_id = discord.Object(id=1179627891634470995)
#bot channel
#channel = client.get_channel(1353657476691787857)

#server the bot interacts with
server = Server()

#start server
@client.tree.command(name="start", description="Starts server.", guild=guild_id)
async def start_server(interaction: discord.Interaction):
    await interaction.response.send_message('<:minecraft:1353669586356015135> Starting server')
    server.start_server()

#stop server / ping command
@client.tree.command(name="stop", description="Stops pinging google", guild=guild_id)
async def stop_running(interaction:discord.Interaction):
    await interaction.response.send_message('<:minecraft:1353669586356015135> Stopping')
    server.stop_server()
    
#test command
@client.tree.command(name="print", description="Parameter Test", guild=guild_id)
async def param_test(interaction: discord.Interaction, param: str):
    await interaction.response.send_message(param)

#command command
@client.tree.command(name="server_command", description="Parameter Test", guild=guild_id)
async def command_input(interaction: discord.Interaction, param: str):
    await interaction.response.send_message('<:minecraft:1353669586356015135> Sending command to server')
    server.command(param)

bot_config = open('botconf.txt')
api_key = bot_config.read()
client.run(api_key)