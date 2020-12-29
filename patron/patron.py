import time
import os
import threading
import queue
from twitchio.ext import commands
from statistics import mode

q = queue.Queue()

bot = commands.Bot(
    # set up the bot
    irc_token=os.environ['TMI_TOKEN'],
    #irc_token=token,
    client_id=os.environ['CLIENT_ID'],
    nick=os.environ['BOT_NICK'],
    prefix=os.environ['BOT_PREFIX'],
    initial_channels=[os.environ['CHANNEL']]
)

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
    print(f'New message: {ctx}')

    # make sure the bot ignores itself and the streamer
    # if ctx.author.name.lower() == os.environ['BOT_NICK'].lower():
    #     return

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

def run_twitch_bot():
    bot.run()
    
def process_commands():
    global q
    while True:
        time.sleep(30)
        print(f'Processor waking up')
        if q.empty():
            print("No commands in queue")
        else:
            votes = {}
            while not q.empty():
                (user, vote) = q.get()
                print(f'User: {user} Vote: {vote}')
                #only take the user's first vote
                if user not in votes:
                    votes[user] = vote
            print('Read all votes.')
            winner = mode(list(votes.values()))
            print(f'Winner: {winner}')


# bot.py
if __name__ == "__main__":
    x = threading.Thread(target=run_twitch_bot)
    y = threading.Thread(target=process_commands)
    x.start()
    y.start()



