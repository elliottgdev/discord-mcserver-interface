import requests

log = open('server.log')

botconf = open('botconf.txt')
bot_api_token = botconf.read()

BASE_URL = f"https://discord.com/api/v9"
SEND_URL = BASE_URL + "/channels/{id}/messages"
DM_URL = BASE_URL + f"/users/@me/channels"


headers = {
    "Authorization": f"Bot {bot_api_token}",
    "User-Agent": f"DiscordBot"
}

guild_id = 1179627891634470995
dm_channel_id = 1353657476691787857

log_start = len(log.readlines())
#r = requests.post(SEND_URL.format(id=dm_channel_id), headers=headers, json={"content": str(log_start)})

a = log_start

while True:
    b = 0
    
    log = open('server.log')
    for line in log:
        if b >= a:
            #await channel.send('<a:server:1353939826243665931> ' + line.strip())
            print('<a:server:1353939826243665931> ' + line.strip())
            r = requests.post(SEND_URL.format(id=dm_channel_id), headers=headers, json={"content": '<a:server:1353939826243665931> ' + line.strip()})
            a += 1
        b += 1