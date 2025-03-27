import requests

log = open('server.log')

bot_config = {}
with open('botconf.txt') as file:
    bot_config = file.readlines()

api_key = bot_config[0].strip()
guild_id = (int(bot_config[1].strip()))
channel = (int(bot_config[2].strip()))
server_jar = bot_config[3].strip()


BASE_URL = f"https://discord.com/api/v9"
SEND_URL = BASE_URL + "/channels/{id}/messages"
DM_URL = BASE_URL + f"/users/@me/channels"


headers = {
    "Authorization": f"Bot {api_key}",
    "User-Agent": f"DiscordBot"
}

log_start = len(log.readlines())
#r = requests.post(SEND_URL.format(id=dm_channel_id), headers=headers, json={"content": str(log_start)})

latest_log = log_start

while True:
    index = 0
    
    log = open('server.log')
    for line in log:
        if index >= latest_log:
            with open('botconf.txt') as file:
                bot_config = file.readlines()
            guild_id = (int(bot_config[1].strip()))
            channel = (int(bot_config[2].strip()))

            #await channel.send('<a:server:1353939826243665931> ' + line.strip())
            print('<a:server:1353939826243665931> ' + line.strip())
            r = requests.post(SEND_URL.format(id=channel), headers=headers, json={"content": '<a:server:1353939826243665931> ' + line.strip()})
            latest_log += 1
        index += 1