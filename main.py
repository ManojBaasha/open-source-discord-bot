#! usr/bin/python3
from ast import alias
import asyncio
from time import time
import currency

import json
import discord
import os
import random
from discord.ext import commands, tasks

# TODO: Info about the hackathon
# TODO: try to make a wordle game
# TODO:

intents = discord.Intents.default()
intents.message_content = True


#####################################################################
"""the basic commands to run the bot on discord"""

# setting a prefix for the bot.In this case "m." is the prefix
client = commands.Bot(command_prefix='m.', intents=intents)

with open('token.txt') as f:
    token = f.read()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#######################################################################

# read questions.txt and store it in a list
with open('questions.txt', encoding="utf8") as f:
    questions = f.readlines()

# read roasts.txt and store it in a list
with open('roasts.txt', encoding="utf8") as f:
    roasts = f.readlines()

with open("responses.txt", encoding="utf8") as f:
    responses = f.readlines()

#######################################################################


@client.hybrid_command()
async def hello(ctx):
    await ctx.send("hello")


@client.command()
async def roast(ctx):
    # select a random roast from the list and send it to the channel
    await ctx.send(random.choice(roasts))


@client.command(aliases=['8ball'])
async def ball(ctx, *, question=None):

    if question == None:
        await ctx.send("Ask a question you wish to have the answer for")
        return
    await ctx.reply(f"{random.choice(responses)}", mention_author=False)


@client.command()
async def qotd_setup(ctx):
    while (True):
        await asyncio.sleep(5)
        channel = client.get_channel(1011727237134958722)
        await channel.send(random.choice(questions))


@tasks.loop(seconds=10)
async def test2():
    channel = client.get_channel(1011727237134958722)
    await channel.send('test')


@client.command()
async def balance(ctx):
    temp_money = currency.user_balance(ctx.author)
    await ctx.send(f"Your current balance is {temp_money} SacBucks!")


@client.command()
async def emojify(ctx, *, text=None):
    if text == None:
        await ctx.send("Enter the text you want to emojify smh")
        return
    emojis = []
    for s in text.lower():
        if s.isdecimal():
            num2emo = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
                       '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'}
            emojis.append(f':{num2emo.get(s)}:')
        elif s.isalpha():
            emojis.append(f':regional_indicator_{s}:')
        else:
            emojis.append(s)
    await ctx.send(' '.join(emojis))


@client.command(aliases=["slot"])
@commands.cooldown(1, 3, commands.BucketType.user)
async def slots(ctx, amount=None):

    if amount == None:
        await ctx.send("Please enter the amount")
        return

    bal = currency.user_balance(ctx.author)

    amount = int(amount)
    if amount > bal:
        await ctx.reply("You don't have that much money in your wallet!")
        return
    if amount < 0:
        await ctx.reply("Amount must be positive")
        return

    final = []
    for i in range(3):
        a = random.choice(["🤑", "🪙", "💰"])

        final.append(a)

    if final[1] == final[2] == final[0]:
        currency.add_score(ctx.author, amount*3)
        em = discord.Embed(title="   ".join(
            final), description=f"You Won\n{ctx.author.mention} got **Ⓥ**{amount}x2 SacBucks By Slots :)", color=ctx.author.colour)
    else:
        currency.subtract_score(ctx.author, amount)
        em = discord.Embed(title="   ".join(
            final), description=f"{ctx.author.mention} Lost **Ⓥ**{amount} SacBucks \nBetter luck Next time :(", color=ctx.author.colour)
    await ctx.reply(embed=em)


player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]


@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:"]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn. `Use ?place <number 1 - 9>`.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.Use `?place <number 1 - 9>`.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")


@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send("<a:winner:873059583990595585> " + mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the ?tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players.")


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


@client.command(aliases=['slaps'])
@commands.cooldown(1, 5, commands.BucketType.user)
async def slap(ctx, *,  member: discord.Member = None): 
    if member == None:
        msg = 'You need to mention a user.'
        await ctx.channel.send(msg)
        return

    responses = ["https://cdn.weeb.sh/images/HJKiX1tPW.gif",
                     "https://cdn.weeb.sh/images/rJ4141YDZ.gif",
                     "https://cdn.weeb.sh/images/ByTR7kFwW.gif",
                     "https://cdn.weeb.sh/images/BJgsX1Kv-.gif"]
    randnum = random.randint(0, len(responses)-1)
    msg = '{}'.format(responses[randnum])
    embed = discord.Embed(title=f" {ctx.author.name} slaps {member.name}", color=ctx.author.color)
    embed.set_image(url=msg)
    await ctx.message.delete()
    await ctx.send(embed=embed)


client.run(token)
