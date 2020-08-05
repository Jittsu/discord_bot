# -*- coding: utf-8 -*-

import discord
import datetime
import requests
from bs4 import BeautifulSoup

# change your access token ---
TOKEN = 'ACCESS TOKEN'

client = discord.Client()

# start process ---
@client.event
async def on_ready():
    now = datetime.datetime.now()
    with open('log.txt', 'a') as f:
        print(now, file=f, end=' ')
        print('login', file=f)

# get request from discord ---
@client.event
async def on_message(message):
    # ignore bot ---
    if message.author.bot:
        return
    # splatoon2 stage request ---
    if message.content == '!splainfo':
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

        # send now data ---
        await message.channel.send('【Now!】')
        await message.channel.send(str(list(now_stage.keys())[0]) + '→' + \
                str(now_stage[list(now_stage.keys())[0]][0]) + ' ' +  str(now_stage[list(now_stage.keys())[0]][1]))
        await message.channel.send(str(list(now_stage.keys())[1]) + '→' + \
                str(now_stage[list(now_stage.keys())[1]][0]) + ' ' +  str(now_stage[list(now_stage.keys())[1]][1]))
        await message.channel.send(str(list(now_stage.keys())[2]) + '→' + \
                str(now_stage[list(now_stage.keys())[2]][0]) + ' ' +  str(now_stage[list(now_stage.keys())[2]][1]))

        # send next data ---
        await message.channel.send('【Next!】')
        await message.channel.send(str(list(next_stage.keys())[0]) + '→' + \
                str(next_stage[list(next_stage.keys())[0]][0]) + ' ' +  str(next_stage[list(next_stage.keys())[0]][1]))
        await message.channel.send(str(list(next_stage.keys())[1]) + '→' + \
                str(next_stage[list(next_stage.keys())[1]][0]) + ' ' +  str(next_stage[list(next_stage.keys())[1]][1]))
        await message.channel.send(str(list(next_stage.keys())[2]) + '→' + \
                str(next_stage[list(next_stage.keys())[2]][0]) + ' ' +  str(next_stage[list(next_stage.keys())[2]][1]))

# Botの起動とDiscordサーバーへの接続
client.run(TOKEN)
