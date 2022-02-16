from random import randint
import discord
from discord.ext import commands

from dotenv import load_dotenv

import os
import sys
from os import getenv

load_dotenv()

bot = commands.Bot(command_prefix='!')

@bot.command()
async def hello(ctx):
    await ctx.reply('Hello!')

@bot.command()
async def playWordle(ctx):
    ansFile = open('ans.txt')
    ansList = ansFile.read().split('\n')
    answer = ansList[randint(0, len(ansList))]
    
    guessFile = open('guesses.txt')
    guessList = guessFile.read().split('\n')

    def check(m):
        return m.channel == ctx.channel and m.author == ctx.author

    guesses = 0
    guessed = False

    while guesses < 6 and not guessed:
        # getting guess
        await ctx.send('what is your guess?')
        guesses += 1
        msgFull = await bot.wait_for('message', check=check)
        msg = msgFull.content

        #cleaning guess
        if(len(msg) != 5):
            await ctx.send('Word Must Be 5 Letter Long')
            guesses -= 1
        elif not(msg in guessList):
            await ctx.send('Word Not a Valid Guess')
            guesses -= 1
        else:
            # valid guess
            replyMsg = list('_____')
            tempAns = list(answer)
            for i in range(0,5):
                #checking for greens first
                if msg[i] == answer[i]:
                    replyMsg[i] = 'G'
                    tempAns[i] = '_'
            for i in range(0,5):
                # then checking for yellows
                if (replyMsg[i] == '_' and tempAns.__contains__(msg[i])):
                    replyMsg[i] = 'Y'
                    tempAns[tempAns.index(msg[i])] = '_'
            
            #converting to a displayable message in discord
            realReply = ''
            for i in range(0,5):
                if (replyMsg[i] == 'G'):
                    realReply += ':green_square: '
                elif (replyMsg[i] == 'Y'):
                    realReply += ':yellow_square: '
                else:
                    realReply += ':black_large_square: '
                    
            # sending message
            await ctx.send(realReply)
            if (replyMsg == list('GGGGG')):
                guessed = True
    
    # final message
    if (guessed):
        await ctx.send('Congrats! In only ' + str(guesses) + ' guesses')
    else:
        await ctx.send('The word was ' + str(answer) + '. Better luck next time')
            

bot.run(getenv('TOKEN'))
