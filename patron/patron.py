import time
import os
import threading
import queue
import random
from twitchio.ext import commands
from statistics import mode
import paho.mqtt.client as mqtt

q = queue.Queue()
client = mqtt.Client()

host = os.environ['MQ_HOST']
port = int(os.environ['MQ_PORT'])
topic = os.environ['MQ_TOPIC']


bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    #irc_token=token,
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

# ---------- TWITCH ---------

@bot.event
async def event_ready():
    'Called once when the bot goes online.'
    print(f"{os.environ['BOT_NICK']} is online!")
    ws = bot._ws  # this is only needed to send messages within event_ready
    await ws.send_privmsg(os.environ['CHANNEL'], f"/me has landed!")


# bot.py, below event_ready
@bot.event
async def event_message(ctx):
    'Runs every time a message is sent in chat.'
    # make sure the bot ignores itself and the streamer
    if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
        return
    print(f'New message from: {ctx.author.name}', flush=True)



    await bot.handle_commands(ctx)

@bot.command(name='forward')
async def forward(ctx):
    global q
    q.put((ctx.author.name,'FORWARD'))
    await ctx.channel.send(f"@{ctx.author.name} said go forward.")

@bot.command(name='left')
async def left(ctx):
    global q
    q.put((ctx.author.name,'LEFT'))
    await ctx.channel.send(f"@{ctx.author.name} said turn left.")

@bot.command(name='right')
async def right(ctx):
    global q
    q.put((ctx.author.name,'RIGHT'))
    await ctx.channel.send(f"@{ctx.author.name} said go right.")

# ------------- MQTT ------------

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    # client.subscribe(topic)

# --------------- MAIN ------------


def run_twitch_bot():
    bot.run()

def random_choice():
    choices = ['FORWARD','LEFT','RIGHT']
    return random.choice(choices)
    
def process_commands():
    global q
    global client
    while True:
        time.sleep(30)
        print(f'Processor waking up', flush=True)
        # if q.empty():
        #     choice = random_choice()
        #     print(f'No user input.  Rolling dice. . . {choice}')
        #     client.publish(topic, choice)
        if q.empty():
            print("No commands in queue", flush=True)
        else:
            votes = {}
            while not q.empty():
                (user, vote) = q.get()
                print(f'User: {user} Vote: {vote}', flush=True)
                #only take the user's first vote
                if user not in votes:
                    votes[user] = vote
            print('Read all votes.', flush=True)
            winner = mode(list(votes.values()))
            print(f'Winner: {winner}', flush=True)
            client.publish(topic, winner)

def run_messages():
    global client
    client.on_connect = on_connect
    client.connect(host, port, 60)
    client.loop_forever()


# bot.py
if __name__ == "__main__":
    
    x = threading.Thread(target=run_messages)
    y = threading.Thread(target=run_twitch_bot)
    z = threading.Thread(target=process_commands)

    x.start()
    y.start()
    z.start()



