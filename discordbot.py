# -*- coding: utf-8 -*-

import discord
from discord.ext import commands
bot = commands.Bot(command_prefix='!')

import datetime
import requests
from bs4 import BeautifulSoup

import pandas as pd
import pickle
from Levenshtein import levenshtein
ls = levenshtein()

# change your access token ---
TOKEN = 'TOKEN'

#client = discord.Client()

# start process ---
#@client.event
@bot.event
async def on_ready():
    now = datetime.datetime.now()
    with open('log.txt', 'a') as f:
        print(now, file=f, end=' ')
        print('login', file=f)

# help ===
@bot.command()
async def cmdhelp(ctx):
    msg = 'Usage:\n\t!<command> [args]\n' \
        + 'Commands:\n\tsplainfo\tGet information of stages for each rules.\n' \
        +            '\tsplabuki\tGet details of the selected weapon.\n' \
        +            '\tsplasmr\tGet informations of Salmon Run.'

    await ctx.send(msg)

# get request from discord ---
@bot.command()
async def splainfo(ctx):
    try:
        # get data ---
        res = requests.get('https://splatoon.caxdb.com/schedule2.cgi')
        # parse data ---
        soup = BeautifulSoup(res.text, 'html.parser')
        all_data = soup.find_all('li')

        # data to dict ---
        data = {}
        for i in range(0, 30, 10):
            data[all_data[i].get_text()] = {all_data[i+1].get_text(): [all_data[i+2].get_text(), all_data[i+3].get_text()], \
                    all_data[i+4].get_text(): [all_data[i+5].get_text(), all_data[i+6].get_text()], \
                    all_data[i+7].get_text(): [all_data[i+8].get_text(), all_data[i+9].get_text()]}

        # select data ---
        now_stage = data[list(data.keys())[0]]
        next_stage = data[list(data.keys())[1]]

        # send data ---
        msg = '【Now!】\n' + str(list(now_stage.keys())[0]) + '→' \
            + str(now_stage[list(now_stage.keys())[0]][0]) + ' ' \
            + str(now_stage[list(now_stage.keys())[0]][1]) + '\n' \
            + str(list(now_stage.keys())[1]) + '→' \
            + str(now_stage[list(now_stage.keys())[1]][0]) + ' ' \
            + str(now_stage[list(now_stage.keys())[1]][1]) + '\n' \
            + str(list(now_stage.keys())[2]) + '→' \
            + str(now_stage[list(now_stage.keys())[2]][0]) + ' ' \
            + str(now_stage[list(now_stage.keys())[2]][1]) + '\n' \
            + '【Next!】\n' + str(list(next_stage.keys())[0]) + '→' \
            + str(next_stage[list(next_stage.keys())[0]][0]) + ' ' \
            + str(next_stage[list(next_stage.keys())[0]][1]) + '\n' \
            + str(list(next_stage.keys())[1]) + '→' \
            + str(next_stage[list(next_stage.keys())[1]][0]) + ' ' \
            + str(next_stage[list(next_stage.keys())[1]][1]) + '\n' \
            + str(list(next_stage.keys())[2]) + '→' \
            + str(next_stage[list(next_stage.keys())[2]][0]) + ' ' \
            + str(next_stage[list(next_stage.keys())[2]][1])

        await ctx.send(msg)
    
    except:
        msg = 'InternalServerError: Sorry, the program of kusaba_bot may have problems.\n' \
            + 'Please contact to administrator of this server.\n' \
            + 'Function named splainfo has problems.'

        await ctx.send(msg)

@bot.command()
async def splabuki(ctx, buki: str):
    try:
        df = pd.read_csv('weapons.csv')
        weapon = list(df['weapon'])
        sub = list(df['sub'])
        sp = list(df['sp'])
        
        with open('ryaku.pkl', 'rb') as pkl:
            ryaku = pickle.load(pkl)
        bubun = [1 if buki in i else 0 for i in weapon]
        msg = ''
        
        if buki in ryaku:
            msg = str(ryaku[buki][0]) + '： ' + str(ryaku[buki][1]) + '・' + str(ryaku[buki][2])

        elif 1 in bubun:
            bubun_index = [i for i, v in enumerate(bubun) if v == 1]
            for i, v in enumerate(bubun_index):
                if i == len(bubun_index) - 1:
                    msg += str(weapon[v]) + '： ' + str(sub[v]) + '・' + str(sp[v])
                else:
                    msg += str(weapon[v]) + '： ' + str(sub[v]) + '・' + str(sp[v]) + '\n'

        else:
            ls_point = list(map(lambda x: ls.culc(buki, x), weapon))
            min_index = [i for i, v in enumerate(ls_point) if v == min(ls_point)]
            for i, v in enumerate(min_index):
                if i == len(min_index) - 1:
                    msg += str(weapon[v]) + '： ' + str(sub[v]) + '・' + str(sp[v])
                else:
                    msg += str(weapon[v]) + '： ' + str(sub[v]) + '・' + str(sp[v]) + '\n'

        await ctx.send(msg)

    except:
        msg = 'InternalServerError: Sorry, the program of kusaba_bot may have problems.\n' \
            + 'Please contact to administrator of this server.\n' \
            + 'Function named splabuki has problems.'

        await ctx.send(msg) 

@bot.command()
async def splasmr(ctx):
    try:
        # get data ---
        res = requests.get('https://splatoon.caxdb.com/splatoon2/coop_schedule2.cgi')
        # parse data ---
        soup = BeautifulSoup(res.text, 'html.parser')
        all_smr = soup.body.ul
        all_smr = all_smr.find_all('li')
        first = all_smr[0:8]
        second = all_smr[8:16]

        first_start, first_end = first[0].text.split('-')
        first_start = str(datetime.date.today().year) + '/' + first_start[:-1]
        first_end = str(datetime.date.today().year) + '/' + first_end[1:]
        first_start_unix = datetime.datetime.strptime(first_start, '%Y/%m/%d %H:%M').timestamp()
        first_end_unix = datetime.datetime.strptime(first_end, '%Y/%m/%d %H:%M').timestamp()
        now_unix = datetime.datetime.now().timestamp()

        if (first_start_unix <= now_unix) and (now_unix < first_end_unix):
            msg = '【Now!】\n' + first[0].text + '\n' + first[1].text + '： ' + first[2].text + '\n' \
                    + first[3].text + '： ' + first[4].text + '・' + first[5].text + '・' + first[6].text \
                    + '・' + first[7].text + '\n' + \
                '【Next!】\n' + second[0].text + '\n' + second[1].text + '： ' + second[2].text + '\n' \
                    + second[3].text + '： ' + second[4].text + '・' + second[5].text + '・' + second[6].text \
                    + '・' + second[7].text
        else:
            msg = '【Next!】\n' + first[0].text + '\n' + first[1].text + '： ' + first[2].text + '\n' \
                    + first[3].text + '： ' + first[4].text + '・' + first[5].text + '・' + first[6].text \
                    + '・' + first[7].text

        await ctx.send(msg)

    except:
        msg = 'InternalServerError: Sorry, the program of kusaba_bot may have problems.\n' \
            + 'Please contact to administrator of this server.\n' \
            + 'Function named splasmr has problems.'

        await ctx.send(msg)

# Botの起動とDiscordサーバーへの接続
bot.run(TOKEN)
