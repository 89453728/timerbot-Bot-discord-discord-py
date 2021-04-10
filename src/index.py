import discord
from discord.ext import commands
from discord.utils import get
from discord import FFmpegPCMAudio
from discord.utils import get
import datetime
import asyncio
from urllib import  parse,request
import re
from cmd import cmdParse
from loadTB import loadTimerbots
from tima.timeout import timerbot
import threading
import os
import asyncio
import time

file_name = "temporizators.tp"
FINAL = "SE ACABO EL TIEMPO DE ESTUDIO, RELAJATE UN RATO CAMPEON!"
STEP = "QUEDAN MINUTOS, ANIMO!"
awaitToExec = 0

ctxGlobal = 0

def timOut (args):
    global awaitToExec
    awaitToExec = 1

async def sendMsg(data):
    print("sended")
    embed = discord.Embed(title = data["final"], description = "Ya es la hora!",
    color=discord.Color.green())

    embed.add_field(name="Chic@s ya ha pasado el tiempo!!", value=data["step"])
    embed.set_image(url="http://ohmycool.com/blog/wp-content/uploads/hora-de-la-aventura.jpg")
    await ctxGlobal.send(embed=embed)

async def check ():
    print("check is running")
    while 1:
        global awaitToExec
        print (">> check " + str(awaitToExec))
        if (awaitToExec == 1):
            await sendMsg({"step":STEP,"final":FINAL})
            awaitToExec = 0
        time.sleep(10)

temporizers = []
temporizators = loadTimerbots(file_name)

def timerBotAdder():
    for i in range(0,len(temporizators)):
        acumulator = 0
        r = cmdParse(temporizators[i])
        temporizers.append({"name":r["name"], "timerbot":timerbot(),"sound":r["sound"]})
        for j in range(0,len(r["temp"])):
            acumulator = acumulator + r["temp"][j]
            # ojo!, timOut es una funcion generica todavia no declarada
            temporizers[i]["timerbot"].add_timeout(acumulator,timOut,{"final":FINAL,"step":STEP,"iter":i},"tempo" + str(i))


timerBotAdder()

token = "ODI3NjEwODQ2MTg0MjEwNDUy.YGdiqQ.nnm2-WgfEMxgSfpJPz-0FUSuAAE"

# command_prefix es el prefijo de los comandos
bot = commands.Bot(command_prefix = "$", description = "command help")

@bot.command() # comando bot (ping pong)
async def ping(ctx): # comando ping
    await ctx.send("pong")

@bot.command() # comando bot suma de dos numeros
async def sum(ctx, numOne: float, numTwo: float): # suma de dos numeros
    await ctx.send(numOne + numTwo)

@bot.command()
async def init(ctx):
    global ctxGlobal
    ctxGlobal = ctx
    await check()

@bot.command() # comando bot (informacion del bot) basicamente elaborar un mensaje con decoracion de texto
async def info(ctx):
    embed = discord.Embed(title = f"{ctx.guild.name}", description = "Lorem Ipsum", timestamp = datetime.datetime.utcnow(),
    color=discord.Color.red())
    embed.add_field(name="server created at",value=f"{ctx.guild.created_at}")
    embed.add_field(name="Server owner", value=f"{ctx.guild.owner}")
    embed.add_field(name="server region",value=f"{ctx.guild.region}")
    embed.add_field(name="server ID",value=f"{ctx.guild.id}")
    embed.set_thumbnail(url="https://miro.medium.com/max/1400/1*FvnpdnrTSQZc_uAGP0GMWg.png")
    await ctx.send(embed = embed)

@bot.command()
async def img1(ctx):
    embed = discord.Embed(title="imagen 1",color=discord.Color.purple())
    embed.set_image(url="https://miro.medium.com/max/1400/1*FvnpdnrTSQZc_uAGP0GMWg.png")
    embed.add_field(name="imagen 1",value="Esta es la imagen uno del bot")
    await ctx.send(embed=embed)

@bot.command()
async def img2(ctx):
    embed = discord.Embed(title="imagen 2",color=discord.Color.purple())
    embed.set_image(url="https://i.pinimg.com/originals/66/89/dc/6689dc331be27e66349ce9a4d15ddff3.gif")
    embed.add_field(name="imagen 2",value="Esta es una imagen del bot")
    await ctx.send(embed=embed)
@bot.command() # anadir un nuevo temporizador (con escalas)
async def tempo(ctx,cmd):
    await init()
    global temporizers
    f = open(file_name,"a")
    f.write("\n" + cmd)
    f.close()
    r = cmdParse(cmd) # "name", "temp", "sound"

    temporizers.append({"name":r["name"], "timerbot":timerbot(),"sound":r["sound"]})
    acumulator = 0

    for j in range(0,len(r["temp"])):
        acumulator = acumulator + r["temp"][j]
        # ojo!, timOut es una funcion generica todavia no declarada
        temporizers[len(temporizers)-1]["timerbot"].add_timeout(acumulator,timOut,{"final":FINAL,"step":STEP,"iter":len(temporizers)-1},"tempo" + str(len(temporizers)-1))

@bot.command()
async def showtempo(ctx,name):
    f = open(file_name,"r")
    bruteText = f.read()
    f.close()

    temp = bruteText.split("\n")
    r = []
    for i in range(0,len(temp)):
        r.append(cmdParse(temp[i]))
    
    for i in range(0,len(r)):
        if r[i]["name"] == name:
            embed = discord.Embed(title="temporizador " + name, color=discord.Color.blue())
            embed.add_field(name="tiempos", value=r[i]["temp"])
        else: 
            continue
    await ctxGlobal.send(embed=embed)

@bot.command()
async def start(ctx,name:str):
    global temporizers
    for i in range (0,len(temporizers)):
        if temporizers[i]["name"] == name:
            temporizers[i]["timerbot"].steamOFF()
            temporizers[i]["timerbot"].clearAllTimeoutCount()
            temporizers[i]["timerbot"].enableAllTimeout()
            temporizers[i]["timerbot"].steamON()

@bot.command()
async def stop(ctx,name:str):
    global temporizers
    for i in range (0,len(temporizers)):
        if temporizers[i]["name"] == name:
            temporizers[i]["timerbot"].steamOFF()
            temporizers[i]["timerbot"].clearAllTimeoutCount()
            temporizers[i]["timerbot"].dissableAllTimeout()

@bot.command()
async def showalltempo(ctx):
    f = open(file_name,"r")
    bruteText = f.read()
    f.close()

    temp = bruteText.split("\n")
    r = []
    for i in range(0,len(temp)):
        r.append(cmdParse(temp[i]))
    
    embed = discord.Embed(title="temporizadores ", color=discord.Color.blue())
    
    for i in range(0,len(r)):
        embed.add_field(name="nombre: " + r[i]["name"], value=r[i]["temp"])
    await ctxGlobal.send(embed=embed)

@bot.command() # conexion a una sala de voz
async def join(ctx):
    channel = ctx.author.voice.channel
    await channel.connect() 
@bot.command() # salir de la sala de voz
async def leave(ctx):
    await ctx.voice_client.disconnect()
# Events
@bot.event # evento de bot en disposicion
async def on_ready():
    # await bot.change_presence(activity = discord.Streaming(name = "tutorials", url = "https://www.twitch.tv/acuntname")) # cambiar estado del bot
    print("mi bot is ready")


bot.run(token) # ejecucion del bot con el token