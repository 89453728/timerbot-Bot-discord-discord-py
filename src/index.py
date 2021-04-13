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
import asyncio
import time
import sys 

sys.setrecursionlimit(6000)
file_name = "temporizators.tp"

FINAL1 = "SE ACABO EL TIEMPO DE TRABAJO, RELAJATE UN RATO CAMPEON!"
STEP1 = "YA QUEDA MENOS, ANIMO!"

FINAL2 = "COMIENZA EL TIEMPO DE TRABAJO, A DARLE DURO!!"
STEP2 = "APROVECHA AL MAXIMO LA SESION!"

URL2 = "https://img.ecartelera.com/noticias/fotos/57200/57221/1.jpg"
URL1 = "http://ohmycool.com/blog/wp-content/uploads/hora-de-la-aventura.jpg"

SOUND = "milei.wav"

awaitToExec = 0
mesgArg = {"step":STEP1,"final":FINAL1,"url":URL1}
ctxGlobal = 0

async def play(voice_audio):
    global ctxGlobal
    guild = ctxGlobal.guild 
    voice_client: discord.VoiceClient = discord.utils.get(bot.voice_clients, guild = guild)
    audio_source = discord.FFmpegPCMAudio(voice_audio)
    await voice_client.voice_connect()
    if not voice_client.is_playing():
        voice_client.play(audio_source,after=None)
    await voice_client.voice_connect()

def timOut (args):
    global awaitToExec
    awaitToExec = 1

async def sendMsg(data):
    print("sended")
    embed = discord.Embed(title = data["final"], description = "Ya es la hora!",
    color=discord.Color.green())

    embed.add_field(name="Chic@s ya ha pasado el tiempo!!", value=data["step"])
    embed.set_image(url=data["url"])
    await ctxGlobal.send(embed=embed)

async def check ():
    global mesgArg
    global awaitToExec
    if (awaitToExec == 1):
        await sendMsg(mesgArg)
        if (mesgArg["step"] == STEP1):
            mesgArg["step"] = STEP2 
            mesgArg["final"] = FINAL2
            mesgArg["url"] = URL2
        else:
            mesgArg["step"] = STEP1
            mesgArg["final"] = FINAL1
            mesgArg["url"] = URL1
        awaitToExec = 0
        await play(SOUND)
    await asyncio.sleep(10)
    await check()

temporizers = []
temporizators = loadTimerbots(file_name)

def timerBotAdder():
    global temporizators 
    global temporizers
    if (len(temporizators) > 0): 
        for i in range(0,len(temporizators)):
            acumulator = 0
            r = cmdParse(temporizators[i])
            temporizers.append({"name":r["name"], "timerbot":timerbot(),"sound":r["sound"]})
            for j in range(0,len(r["temp"])):
                acumulator = acumulator + r["temp"][j]
                # ojo!, timOut es una funcion generica todavia no declarada
                temporizers[i]["timerbot"].add_timeout(acumulator,timOut,{"final":FINAL1,"step":STEP1,"iter":i},"tempo" + str(i))
    else:
        temporizers = []

timerBotAdder()

token = "ODI3NjEwODQ2MTg0MjEwNDUy.YGdiqQ.FvkyLbOgj3Xh8lrPXhKJDVRYLCo"

# command_prefix es el prefijo de los comandos
bot = commands.Bot(command_prefix = "$", description = "command help")

@bot.command() # comando bot (ping pong)
async def ping(ctx): # comando ping
    await ctx.send("pong")


@bot.command()
async def init(ctx):
    global ctxGlobal
    ctxGlobal = ctx

@bot.command() # comando bot (informacion del bot) basicamente elaborar un mensaje con decoracion de texto
async def info(ctx):
    embed=discord.Embed(title="Manual de Comandos", description="aqui se describe brevemente el uso de los distintos comandos. Los comandos vienen predecidos del simbolo $", color=0x6272c6)
    embed.add_field(name="$tempo nombre>10:5: ... :14>sonido", value="añadir un temporizador a la lista de temporizadores. Este se añade sin ser activado. nombre es el nombre que quieres darle para distinguirlo del resto, los tiempos son intervalos en los que ira alternando entre estudio y trabajo y el sonido por ahora no es funcional", inline=False)
    embed.add_field(name="$rmtempo nombre", value="borrar el temporizador nombre de tu lista de temporizadores", inline=False)
    embed.add_field(name="$info", value="ver este mensaje", inline=False)
    embed.add_field(name="$join", value="unirse a un canal de voz (en el que estas incorporado)", inline=False)
    embed.add_field(name="$leave", value="salir del canal de voz", inline=False)
    embed.add_field(name="$start nombre", value="inicia el temporizador de la lista de temporizadores que se llama nombre", inline=False)
    embed.add_field(name="$stop nombre", value="apaga el temporizador de la lista de temporizadores que se llama nombre", inline=False)
    embed.add_field(name="$showtempo nombre", value="muestra la configuracion del temporizador nombre", inline=False)
    embed.add_field(name="$showalltempo", value="muestra todos los temporizadores", inline=False)
    embed.add_field(name="$init", value="comando necesario para iniciar el temporizador", inline=False)
    await ctx.send(embed=embed)

@bot.command() # anadir un nuevo temporizador (con escalas)
async def tempo(ctx,cmd):
    global temporizers
    f = open(file_name,"a")
    print (temporizers)
    if len(temporizers) > 0:
        f.write("\n" + cmd)
    else:
        f.write(cmd)
    f.close()
    r = cmdParse(cmd) # "name", "temp", "sound"
    print(cmd)

    temporizers.append({"name":r["name"], "timerbot":timerbot(),"sound":r["sound"]})
    acumulator = 0

    for j in range(0,len(r["temp"])):
        acumulator = acumulator + r["temp"][j]
        temporizers[len(temporizers)-1]["timerbot"].add_timeout(acumulator,timOut,{"final":FINAL1,"step":STEP1,"iter":len(temporizers)-1},"tempo" + str(len(temporizers)-1))

@bot.command()
async def rmtempo(ctx,name):
    global temporizers
    global temporizators
    global file_name
    f = open(file_name,"r")
    txt = f.read()
    f.close()
    tot = ""
    print(txt)

    txt = txt.split("\n")
    for i in range(0,len(txt)):
        r = cmdParse(txt[i])
        if r["name"] != name:
            if (i == len(txt)-1):
                tot = tot + txt[i]
            else:
                tot = tot + txt[i] + "\n"
        else:
            if i == len(txt) -1:
                tot = tot[0:len(tot)-1]
    f = open(file_name,"w")
    f.write(tot)
    f.close()

    temporizators = loadTimerbots(file_name)
    timerBotAdder()



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
    await sendMsg({"final":FINAL2, "step":STEP2, "url":URL2})

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

    if len(bruteText) > 0:
        temp = bruteText.split("\n")
        r = []
        for i in range(0,len(temp)):
            r.append(cmdParse(temp[i]))
    
    embed = discord.Embed(title="temporizadores ", color=discord.Color.blue())
    
    if len(bruteText) > 0:
        for i in range(0,len(r)):
            embed.add_field(name="nombre: " + r[i]["name"], value=r[i]["temp"], inline=False)
    else:
        embed.add_field(name="No hay temporizadores disponibles " , value="puedes añadir temporizadores con el comando: $tempo nombre_temporizador>intervalo1:intervalo2...>sonido.mp3 (los sonidos todavia no estan disponibles)")

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

bot.loop.create_task(check())
bot.run(token) # ejecucion del bot con el token