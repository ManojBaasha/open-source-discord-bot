#! usr/bin/python3
import asyncio
from time import time


import discord
import os
import random
from discord.ext import commands, tasks

#TODO: Info about the hackathon 
#TODO: try to make a wordle game
#TODO: 

roasts = ["I'd give you a nasty look but you've already got one",
"If you were going to be two-faced at least make one of them pretty",
"I love what you've done with your hair. How do you get it to come out of the nostrils like that",
"If laughter is the best medicine your face must be curing the world",
"The only way you'll ever get laid is if you crawl up a chicken's ass and wait",
"It looks like your face caught fire and someone tried to put it out with a hammer",
"I'd like to see things from your point of view... but I can't seem to get my head that far up your ass",
"I've seen people like you before but I had to pay admission",
"Scientists say the universe is made up of neutrons protons and electrons. They forgot to mention morons",
"You're so fat you could sell shade",
"Your lips keep moving but all I hear is Blah blah blah",
"Your family tree must be a cactus because everyone on it is a prick",
"You'll never be the man your mother is",
"I'm sorry was I meant to be offended? The only thing offending me is your face",
"Someday you'll go far... and I hope you stay there",
"Which sexual position produces the ugliest children? Ask your mother",
"Stupidity's not a crime so you're free to go",
"If I had a face like yours I'd sue my parents",
"Your doctor called with your colonoscopy results. Good news - they found your head",
"No those pants don't make you look fatter - how could they",
"Save your breath - you'll need it to blow up your date",
"You're not stupid you just have bad luck when thinking",
"If you really want to know about mistakes you should ask your parents",
"Please keep talking. I always yawn when I am interested",
"The zoo called. They're wondering how you got out of your cage",
"Whatever kind of look you were going for you missed",
"I was hoping for a battle of wits but you appear to be unarmed",
"Aww it's so cute when you try to talk about things you don't understand",
"I don't know what makes you so stupid but it really works",
"You are proof that evolution can go in reverse",
"Brains aren't everything. In your case they're nothing",
"I thought of you today It reminded me to take the garbage out",
"You're so ugly when you look in the mirror your reflection looks away",
"I'm sorry I didn't get that - I don't speak idiot",
"Quick - check your face! I just found your nose in my business",
"It's better to let someone think you're stupid than open your mouth and prove it",
"Hey your village called - they want their idiot back",
"Were you born this stupid or did you take lessons",
"I've been called worse by better",
"You're such a beautiful intelligent wonderful person. Oh I'm sorry I thought we were having a lying competition",
"I may love to shop but I'm not buying your bull",
"I'd slap you but I don't want to make your face look any better",
"Calling you an idiot would be an insult to all stupid people",
"I just stepped in something that was smarter than you... and smelled better too",
"You have the right to remain silent because whatever you say will probably be stupid anyway",
"Your so ugly Hello Kitty said goodbye to you",
"Could you take a couple steps back. I'm allergic to idiots",
"Your so big a picture of you would fall off the wall",
"You look like a before picture",
"You know that feeling when you step in gum... that's how i feel looking at you",
"You couldn't find logic if it hit you in the face",
"My phone battery lasts longer than your relationships",
"Oh you’re talking to me. I thought you only talked behind my back",
"Too bad you can’t count jumping to conclusions and running your mouth as exercise",
"If I wanted a bitch I would have bought a dog",
"My business is my business. Unless you’re a thong... get out of my ass",
"It’s a shame you can’t Photoshop your personality",
"Jealousy is a disease. Get well soon",
"When karma comes back to punch you in the face... I want to be there in case it needs help",
"You have more faces than Mount Rushmore",
"Maybe you should eat make-up so you’ll be pretty on the inside too",
"Whoever told you to be yourself gave you really bad advice",
"I thought I had the flu... but then I realized your face makes me sick to my stomach",
"You should try the condom challenge. If your gonna act like a dick then dress like one too",
"I’m jealous of people who don’t know you",
"You sound reasonable… Time to up my medication",
"Please say anything. It’s so cute when you try to talk about things you don’t understand",
"I suggest you do a little soul searching. You might just find one",
"You should try this new brand of chap stick. The brand is Elmer's",
"I'd smack you if it wasn't animal abuse",
"Why is it acceptable for you to be an idiot but not for me to point it out",
"If you’re offended by my opinion... you should hear the ones I keep to myself",
"If you’re going to be a smart ass... first you have to be smart. Otherwise you’re just an ass",
"I’m not an astronomer but I am pretty sure the earth revolves around the sun and not you",
"Keep rolling your eyes. Maybe you’ll find your brain back there",
"No no no. I am listening. It just takes me a minute to process that much stupidity", 
"Sorry... what language are you speaking. Sounds like Bullshit",
"Everyone brings happiness to a room. I do when I enter... you do when you leave",
"You’re the reason I prefer animals to people", 
"You’re not stupid; you just have bad luck when thinking",
"Please... keep talking. I always yawn when I am interested",
"Were you born this stupid or did you take lessons?",
"You have the right to remain silent because whatever you say will probably be stupid anyway",
"Hey you have something on your chin… no… the 3rd one down",
"You’re impossible to underestimate",
"You’re kinda like Rapunzel except instead of letting down your hair... you let down everyone in your life",
"You look like your father would be disappointed in you if he stayed",
"You look like you were bought on the clearance shelf", 
"Take my lowest priority and put yourself beneath it",
"You are a pizza burn on the roof of the world’s mouth",
"People like you are the reason God doesn’t talk to us anymore",
"You’re so dense that light bends around you",
"I don’t have the time or the crayons to explain anything to you",
"You’re not as dumb as you look. That's saying something",
"You’ve got a great body. Too bad there’s no workout routine for a face",
"You’re about as important as a white crayon",
"I fear no man. But your face... it scares me",
"We get straight to the point. We aren't Willy Wonka"]

#####################################################################
"""the basic commands to run the bot on discord"""

client = discord.Client()

client=commands.Bot(command_prefix='m.')#setting a prefix for the bot.In this case "m." is the prefix

with open('token.txt') as f:
    """ using a text file to store the discord bot token"""
    token = f.read()
    
@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

#######################################################################

#read questions.txt and store it in a list
with open('questions.txt', encoding="utf8") as f:
    questions = f.readlines()

@client.command()
async def hello(ctx):
    await ctx.send("hello")

@client.command()
async def roast(ctx):
    #select a random roast from the list and send it to the channel
    await ctx.send(random.choice(roasts))

@client.command()
async def cat(ctx):
    await ctx.send("https://aws.random.cat/meow")

@client.command()
async def ball(ctx, *, question=None):

    if question == None:
        await ctx.send("Please ask a question")
        return
    responses = ["It is certain.",
                 "It is decidedly so.",
                 "Without a doubt.",
                 "Yes - definitely.",
                 "You may rely on it.",
                 "As I see it, yes.",
                 "Most likely.",
                 "Outlook good.",
                 "Yes.",
                 "Signs point to yes.",
                 "Reply hazy, try again.",
                 "Ask again later.",
                 "Better not tell you now.",
                 "Cannot predict now.",
                 "Concentrate and ask again.",
                 "Don't count on it.",
                 "My reply is no.",
                 "My sources say no.",
                 "Outlook not so good.",
                 "Very doubtful."]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

@client.command()
async def qotd_setup(ctx):
    
    while(True):
        #10 second pause
        await asyncio.sleep(5)
        #randomly select a question from the list
        question = random.choice(questions)
        #send the question to the channel
        await ctx.send(question)




#######################################################################

    
client.run(token)