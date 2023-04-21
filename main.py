#! usr/bin/python3
from ast import alias
import asyncio
from time import time
import functions.currency as currency

import json
import discord
import os
import random
from discord.ext import commands, tasks
import aiohttp


# TODO: Info about the hackathon
# TODO: try to make a wordle game

intents = discord.Intents.default()
intents.message_content = True

#####################################################################
"""the basic commands to run the bot on discord"""
#you will need these commands to get the bot to start running

# setting a prefix for the bot. In this case "m." is the prefix. You can customize to whatever you like
client = commands.Bot(command_prefix='m.', intents=intents)

with open('token.txt') as f: 
    token = f.read()


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#######################################################################

# read questions.txt and store it in a list
with open('responses/questions.txt', encoding="utf8") as f:
    questions = f.readlines()

# read roasts.txt and store it in a list
with open('responses/roasts.txt', encoding="utf8") as f:
    roasts = f.readlines()

with open("responses/responses.txt", encoding="utf8") as f:
    responses = f.readlines()

with open("responses/pickupline.txt", encoding="utf8") as f:
    pickuplines = f.readlines()

#######################################################################

# class to add actions to the bot
class actions:
    def slap():
        return random.choice(roasts)

# class to add fun to the bot
class fun:
    def _8ball(question):
        return random.choice(responses)



    def emojifi(word):
        emojis = []
        for s in word.lower():
            if s.isdecimal():
                num2emo = {'0': 'zero', '1': 'one', '2': 'two', '3': 'three', '4': 'four',
                       '5': 'five', '6': 'six', '7': 'seven', '8': 'eight', '9': 'nine'}
                emojis.append(f':{num2emo.get(s)}:')
            elif s.isalpha():
                emojis.append(f':regional_indicator_{s}:')
            else:
                emojis.append(s)
        return ' '.join(emojis)
    
######################################################################

# remove the default help command
client.remove_command("help")

# create a help command
@client.command()
async def help(ctx):
    # create a interface of help command embed
    em = discord.Embed(title="Help", description="List of commands")
    em.add_field(name="m.help", value="```Shows this message```", inline=False)
    em.add_field(name="m.roast", value="```Roasts the user```", inline=False)
    em.add_field(name="m.8ball", value="```Answers your question```", inline=False)
    em.add_field(name="m.balance", value="```Shows your balance```", inline=False)
    em.add_field(name="m.emojify", value="```Emojifies your text```", inline=False)
    em.add_field(name="m.slots", value="```Play slots```", inline=False)
    em.add_field(name="!roast [user]", value="```Roasts the mentioned user```", inline=False)
    em.add_field(name="!tictactoe [user]", value="```Starts a game of Tic Tac Toe with the mentioned user```", inline=False)
    em.set_footer(text="Created by Manoj")

    await ctx.send(embed=em)

# create a hello command
@client.command()
async def hello(ctx):
    await ctx.send("Hey there!")

@client.command()
async def roast(ctx):
    await ctx.send(actions.slap())

@client.command(aliases=['8ball'])
async def ball(ctx, *, question=None):
    if question == None:
        await ctx.send("Ask a question you wish to have the answer for")
        return
    await ctx.reply(fun._8ball(question), mention_author=True)

@client.command()
async def pickupline(ctx):
    await ctx.send(random.choice(pickuplines))



@client.command()
async def emojify(ctx, *, text=None):
    if text == None:
        await ctx.send("Enter the text you want to emojify smh")
        return

    await ctx.send(fun.emojifi(text))


@client.command()
async def balance(ctx):
    temp_money = currency.user_balance(ctx.author)
    em = discord.Embed(title=f"💰 {ctx.author}'s balance 💰")
    em.add_field(name=f"| Bank Balance |",
                 value=f"**Ⓥ** {temp_money}", inline=False)
    await ctx.reply(embed=em)


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

######################################################################
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
            await ctx.send("It is <@" + str(player1.id) + ">'s turn. `Use m.place <number 1 - 9>`.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.Use `m.place <number 1 - 9>`.")
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


######################################################################


@client.command(aliases=['slaps'])
async def slap(ctx, *,  member: discord.Member = None):
    if member == None:
        msg = 'You need to mention a user.'
        await ctx.channel.send(msg)
        return
    
    session = aiohttp.ClientSession()
    search = 'slap'

    search.replace(' ', '+')
    response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=WSBFQtMkVf8HcTMUgDQb5xExXWLe9s0a&limit=10')
    data = json.loads(await response.text())
    random_gif = random.randint(0, 8)
    # await ctx.send(data['data'][random_gif]['images']['original']['url'])
    
    msg = '{}'.format(data['data'][random_gif]['images']['original']['url'])
    embed = discord.Embed(
        title=f" {ctx.author.name} slaps {member.name}", color=ctx.author.color)
    embed.set_image(url=msg)
    await ctx.message.delete()
    await ctx.send(embed=embed)

    await session.close()

@client.event
async def setup_hook():
    await client.tree.sync()
    print(f"Synced slash commands for {client.user}")


@client.command(pass_context=True)
async def giphy(ctx, *, search= None):
    embed = discord.Embed(colour=discord.Colour.blue())
    session = aiohttp.ClientSession()

    if(search == None):
        await ctx.send("What gif do you want to search for?")

    search.replace(' ', '+')
    response = await session.get('http://api.giphy.com/v1/gifs/search?q=' + search + '&api_key=WSBFQtMkVf8HcTMUgDQb5xExXWLe9s0a&limit=10')
    data = json.loads(await response.text())
    random_gif = random.randint(0, 8)
    await ctx.send(data['data'][random_gif]['images']['original']['url'])

    await session.close()

client.run(token)
