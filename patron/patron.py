import time
import os 
from twitchio.ext import commands

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
    await ctx.channel.send(f"@{ctx.author.name} said go forward.")

@bot.command(name='left')
async def left(ctx):
    await ctx.channel.send(f"@{ctx.author.name} said turn left.")

@bot.command(name='right')
async def right(ctx):
    await ctx.channel.send(f"@{ctx.author.name} said go right.")

# bot.py
if __name__ == "__main__":
    bot.run()
    print('After run.')



