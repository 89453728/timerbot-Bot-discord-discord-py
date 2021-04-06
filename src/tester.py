import discord
from discord.ext import commands
from discord import FFmpegPCMAudio
from discord.utils import get
import datetime
from urllib import  parse,request
import re
from cmd import cmdParse
from loadTB import loadTimerbots
from tima.timeout import timerbot

file_name = "temporizators.tp"
FINAL = "SE ACABO EL TIEMPO DE ESTUDIO, RELAJATE UN RATO CAMPEON!"
STEP = "QUEDAN MINUTOS, ANIMO!"

def timOut(data):
    print("hola mundo")

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
